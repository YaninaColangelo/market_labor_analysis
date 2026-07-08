"""Conector para ofertas publicadas en Tecnoempleo."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup

from src.cleaning import generar_id, normalizar_texto


BASE_URL = "https://www.tecnoempleo.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def descargar_html(url: str, timeout: int = 20) -> str:
    """Descarga el HTML de una oferta."""
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def _primer_texto(soup: BeautifulSoup, selectores: list[str]) -> str:
    for selector in selectores:
        elemento = soup.select_one(selector)
        if elemento:
            texto = normalizar_texto(elemento.get_text(" ", strip=True))
            if texto:
                return texto
    return ""


def _textos(soup: BeautifulSoup, selectores: list[str]) -> list[str]:
    textos: list[str] = []
    for selector in selectores:
        for elemento in soup.select(selector):
            texto = normalizar_texto(elemento.get_text(" ", strip=True))
            if texto and texto not in textos:
                textos.append(texto)
    return textos


def _meta_content(soup: BeautifulSoup, **attrs: str) -> str:
    elemento = soup.find("meta", attrs=attrs)
    if not elemento:
        return ""
    return normalizar_texto(elemento.get("content", ""))


def _metadata(soup: BeautifulSoup) -> list[str]:
    textos: list[str] = []
    metadatos = [
        ("titulo_meta", _meta_content(soup, property="og:title")),
        ("descripcion_meta", _meta_content(soup, name="description")),
        ("url_meta", _meta_content(soup, property="og:url")),
    ]
    for clave, valor in metadatos:
        if valor:
            textos.append(f"{clave}: {valor}")

    textos.extend(
        _textos(
            soup,
            [
                ".card li",
                ".mb-3 li",
                ".detalle-oferta li",
                ".job-detail li",
                ".list-unstyled li",
                "dl",
                "table tr",
            ],
        )
    )
    return list(dict.fromkeys(textos))


def _texto_por_etiqueta(soup: BeautifulSoup, etiquetas: tuple[str, ...]) -> str:
    textos = _textos(soup, ["li", "p", "div", "span", "td", "th"])
    for texto in textos:
        texto_lower = texto.lower()
        for etiqueta in etiquetas:
            etiqueta_lower = etiqueta.lower()
            if texto_lower.startswith(etiqueta_lower):
                if ":" in texto:
                    return normalizar_texto(texto.split(":", 1)[-1])
                return normalizar_texto(texto[len(etiqueta) :])
    return ""


def _descripcion_completa(soup: BeautifulSoup) -> str:
    return _primer_texto(
        soup,
        [
            "#job-description",
            ".job-description",
            ".detalle-oferta",
            ".oferta-descripcion",
            "[itemprop='description']",
            "article",
            "main",
        ],
    )


def construir_oferta_raw(html: str, url: str) -> dict[str, Any]:
    """Construye un diccionario raw a partir del HTML de la oferta."""
    soup = BeautifulSoup(html, "html.parser")

    titulo = (
        _meta_content(soup, property="og:title")
        or _primer_texto(
            soup,
            [
                "h1",
                ".fs-4",
                ".font-weight-bold",
                ".titulo-oferta",
                "[data-testid='job-title']",
                "[itemprop='title']",
            ],
        )
    )
    descripcion = _meta_content(soup, name="description") or _descripcion_completa(soup)
    detalle = _descripcion_completa(soup)
    metadata = _metadata(soup)

    oferta_raw = {
        "id_oferta": generar_id(url),
        "fecha_publicacion": _texto_por_etiqueta(soup, ("publicado:", "fecha:", "fecha publicacion:")),
        "fuente": "Tecnoempleo",
        "url": url,
        "pais": "Espana",
        "titulo": titulo,
        "descripcion": descripcion,
        "responsabilidades": detalle if detalle and detalle != descripcion else "",
        "empresa": _texto_por_etiqueta(soup, ("empresa:", "compania:", "cliente final:")),
        "industria": _texto_por_etiqueta(soup, ("sector:", "categoria:", "industria:")),
        "modalidad": _texto_por_etiqueta(soup, ("modalidad:", "teletrabajo:")),
        "seniority": _texto_por_etiqueta(soup, ("experiencia:", "nivel:", "seniority:")),
        "formacion_requerida": _texto_por_etiqueta(
            soup,
            ("formacion:", "estudios minimos:", "titulacion:"),
        ),
        "metadata": metadata,
    }
    return oferta_raw


def obtener_oferta(url: str) -> dict[str, Any]:
    """Descarga una oferta de Tecnoempleo y devuelve oferta_raw."""
    html = descargar_html(url)
    return construir_oferta_raw(html, url)


def buscar_ofertas(query: str, limit: int = 20, base_url: str = BASE_URL) -> list[str]:
    """Busca URLs de ofertas en Tecnoempleo para una consulta simple."""
    search_url = f"{base_url}/ofertas-trabajo/?te={quote_plus(query)}"
    html = descargar_html(search_url)
    soup = BeautifulSoup(html, "html.parser")

    urls: list[str] = []
    for link in soup.select("a[href]"):
        href = link.get("href", "")
        absolute_url = urljoin(base_url, href)
        if "/oferta" in absolute_url or "/rf-" in absolute_url:
            if absolute_url not in urls:
                urls.append(absolute_url)
        if len(urls) >= limit:
            break

    return urls
