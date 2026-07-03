"""Conector para ofertas publicadas en Tecnoempleo."""

from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from src.cleaning import generar_id


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
            texto = elemento.get_text(" ", strip=True)
            if texto:
                return texto
    return ""


def _meta_content(soup: BeautifulSoup, **attrs: str) -> str:
    elemento = soup.find("meta", attrs=attrs)
    if not elemento:
        return ""
    return elemento.get("content", "").strip()


def _metadata(soup: BeautifulSoup) -> list[str]:
    textos: list[str] = []
    metadatos = [
        ("titulo_meta", _meta_content(soup, property="og:title")),
        ("descripcion_meta", _meta_content(soup, name="description")),
    ]
    for clave, valor in metadatos:
        if valor:
            textos.append(f"{clave}: {valor}")

    for selector in [".card li", ".mb-3 li", ".detalle-oferta li", ".job-detail li"]:
        for elemento in soup.select(selector):
            texto = elemento.get_text(" ", strip=True)
            if texto and texto not in textos:
                textos.append(texto)
    return textos


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
            ],
        )
    )
    descripcion = (
        _meta_content(soup, name="description")
        or _primer_texto(
            soup,
            [
                "#job-description",
                ".job-description",
                ".detalle-oferta",
                ".oferta-descripcion",
                "article",
                "main",
            ],
        )
    )

    oferta_raw = {
        "id_oferta": generar_id(url),
        "fuente": "Tecnoempleo",
        "url": url,
        "titulo": titulo,
        "descripcion": descripcion,
        "metadata": _metadata(soup),
    }
    return oferta_raw


def obtener_oferta(url: str) -> dict[str, Any]:
    """Descarga una oferta de Tecnoempleo y devuelve oferta_raw."""
    html = descargar_html(url)
    return construir_oferta_raw(html, url)
