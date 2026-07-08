"""Conector para ofertas publicadas en Tecnoempleo."""

from __future__ import annotations

import json
import re
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


def _normalizar_fecha(fecha: str) -> str:
    fecha = normalizar_texto(fecha)
    match = re.search(r"\b(\d{2})/(\d{2})/(\d{4})\b", fecha)
    if match:
        dia, mes, anio = match.groups()
        return f"{anio}-{mes}-{dia}"
    return fecha


def _normalizar_herramientas(texto: str) -> str:
    reemplazos = {
        "power bi": "Power BI",
        "sql server": "SQL Server",
        "python": "Python",
        "excel": "Excel",
        "tableau": "Tableau",
        "etl": "ETL",
        "sql": "SQL",
    }
    texto = normalizar_texto(texto)
    if not texto:
        return ""

    herramientas: list[str] = []
    for parte in re.split(r"[,;/|]+", texto):
        item = normalizar_texto(parte)
        if not item:
            continue
        item_normalizado = reemplazos.get(item.lower(), item)
        if item_normalizado not in herramientas:
            herramientas.append(item_normalizado)

    return "; ".join(herramientas)


def _metadata(soup: BeautifulSoup) -> list[str]:
    textos: list[str] = []
    metadatos = [
        ("titulo_html", _primer_texto(soup, ["title"])),
        ("titulo_meta", _meta_content(soup, property="og:title")),
        ("descripcion_meta", _meta_content(soup, name="description")),
        ("descripcion_og", _meta_content(soup, property="og:description")),
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


def _json_ld_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        items = [data]
        graph = data.get("@graph")
        if isinstance(graph, list):
            items.extend(item for item in graph if isinstance(item, dict))
        return items
    if isinstance(data, list):
        return [item for value in data for item in _json_ld_items(value)]
    return []


def _extraer_json_ld_jobposting(soup: BeautifulSoup) -> dict[str, Any]:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        contenido = script.string or script.get_text()
        if not contenido:
            continue
        try:
            data = json.loads(contenido)
        except json.JSONDecodeError:
            continue

        for item in _json_ld_items(data):
            tipo = item.get("@type")
            tipos = tipo if isinstance(tipo, list) else [tipo]
            if "JobPosting" not in tipos:
                continue

            organizacion = item.get("hiringOrganization") or {}
            ubicacion = item.get("jobLocation") or {}
            if isinstance(ubicacion, list):
                ubicacion = ubicacion[0] if ubicacion else {}
            direccion = ubicacion.get("address") if isinstance(ubicacion, dict) else {}
            direccion = direccion or {}

            return {
                "titulo": normalizar_texto(item.get("title", "")),
                "descripcion": normalizar_texto(item.get("description", "")),
                "fecha_publicacion": _normalizar_fecha(item.get("datePosted", "")),
                "empresa": normalizar_texto(organizacion.get("name", "")),
                "ciudad": normalizar_texto(direccion.get("addressLocality", "")),
                "pais": normalizar_texto(direccion.get("addressCountry", "")),
                "modalidad": normalizar_texto(item.get("employmentType", "")),
                "metadata": [f"json_ld_{clave}: {valor}" for clave, valor in item.items() if valor],
            }
    return {}


def _extraer_meta_tecnoempleo(soup: BeautifulSoup) -> dict[str, str]:
    textos = [
        _meta_content(soup, name="description"),
        _meta_content(soup, property="og:description"),
        _primer_texto(soup, ["title"]),
    ]
    campos: dict[str, str] = {}

    for texto in textos:
        if not texto:
            continue

        fecha = _normalizar_fecha(texto)
        if fecha != texto:
            campos.setdefault("fecha_publicacion", fecha)

        patron = (
            r"Oferta de Empleo\s+"
            r"(?P<titulo>.+?)\s+en\s+"
            r"(?P<ciudad>[^,]+),\s+"
            r"(?P<empresa>.+?)\s+-\s+Tecnoempleo\.com"
            r"(?:\s+con conocimientos\s+(?P<herramientas>.+))?"
        )
        match = re.search(patron, texto, flags=re.IGNORECASE)
        if not match:
            continue

        campos.setdefault("titulo", normalizar_texto(match.group("titulo")))
        campos.setdefault("ciudad", normalizar_texto(match.group("ciudad")))
        campos.setdefault("empresa", normalizar_texto(match.group("empresa")))
        herramientas = match.group("herramientas")
        if herramientas:
            campos.setdefault("requisitos", _normalizar_herramientas(herramientas))

    return campos


def _segmentar_detalle_tecnoempleo(detalle: str) -> dict[str, str]:
    detalle = normalizar_texto(detalle)
    if not detalle:
        return {}

    encabezados = [
        "Descripción de la empresa",
        "Descripción del empleo",
        "Requisitos",
        "Información adicional",
    ]
    posiciones = []
    for encabezado in encabezados:
        match = re.search(re.escape(encabezado), detalle, flags=re.IGNORECASE)
        if match:
            posiciones.append((match.start(), match.end(), encabezado))

    if not posiciones:
        return {"cuerpo_completo": detalle}

    posiciones.sort()
    secciones: dict[str, str] = {"cuerpo_completo": detalle}
    claves = {
        "Descripción de la empresa": "descripcion_empresa",
        "Descripción del empleo": "descripcion_empleo",
        "Requisitos": "requisitos",
        "Información adicional": "informacion_adicional",
    }

    for index, (_, fin, encabezado) in enumerate(posiciones):
        siguiente_inicio = posiciones[index + 1][0] if index + 1 < len(posiciones) else len(detalle)
        contenido = normalizar_texto(detalle[fin:siguiente_inicio])
        if contenido:
            secciones[claves[encabezado]] = contenido

    return secciones


def _extraer_modalidad_texto(texto: str) -> str:
    texto_lower = normalizar_texto(texto).lower()
    patrones = (
        ("Presencialidad flexible", "Presencialidad flexible"),
        ("Hibrido", "hibrido"),
        ("Hibrido", "híbrido"),
        ("Remoto", "remoto"),
        ("Presencial", "presencial"),
    )
    for valor, patron in patrones:
        if patron in texto_lower:
            return valor
    return ""


def _extraer_industria_texto(texto: str) -> str:
    texto = normalizar_texto(texto)
    match = re.search(r"\bsector\s+([a-záéíóúñ ]+?)(?:\.|,|;|$)", texto, flags=re.IGNORECASE)
    if match:
        return normalizar_texto(f"sector {match.group(1)}")
    return ""


def _extraer_experiencia_metadata(metadata: list[str]) -> str:
    for item in metadata:
        match = re.search(r"\b(\d+\s+años?)\s+Experiencia\b", item, flags=re.IGNORECASE)
        if match:
            return normalizar_texto(match.group(1))
    return ""


def _extraer_requisitos_metadata(metadata: list[str]) -> str:
    for item in metadata:
        if re.search(r"\b(power bi|sql|etl|python|excel|tableau)\b", item, flags=re.IGNORECASE):
            return _normalizar_herramientas(item)
    return ""


def construir_oferta_raw(html: str, url: str) -> dict[str, Any]:
    """Construye un diccionario raw a partir del HTML de la oferta."""
    soup = BeautifulSoup(html, "html.parser")

    json_ld = _extraer_json_ld_jobposting(soup)
    meta = _extraer_meta_tecnoempleo(soup)
    detalle = _descripcion_completa(soup)
    secciones = _segmentar_detalle_tecnoempleo(detalle)
    metadata = _metadata(soup)
    descripcion_empleo = secciones.get("descripcion_empleo", "")

    titulo = (
        json_ld.get("titulo")
        or meta.get("titulo")
        or _meta_content(soup, property="og:title")
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
    descripcion = descripcion_empleo or json_ld.get("descripcion") or _meta_content(soup, name="description")
    requisitos = secciones.get("requisitos") or meta.get("requisitos") or _extraer_requisitos_metadata(metadata)
    cuerpo_completo = secciones.get("cuerpo_completo", "")
    if cuerpo_completo:
        metadata.append(f"cuerpo_completo: {cuerpo_completo}")

    oferta_raw = {
        "id_oferta": generar_id(url),
        "fecha_publicacion": json_ld.get("fecha_publicacion")
        or meta.get("fecha_publicacion")
        or _texto_por_etiqueta(soup, ("publicado:", "fecha:", "fecha publicacion:")),
        "fuente": "Tecnoempleo",
        "url": url,
        "pais": json_ld.get("pais") or "Espana",
        "titulo": titulo,
        "descripcion": descripcion,
        "responsabilidades": descripcion_empleo,
        "requisitos": requisitos,
        "ciudad": json_ld.get("ciudad") or meta.get("ciudad"),
        "empresa": json_ld.get("empresa") or meta.get("empresa") or _texto_por_etiqueta(
            soup,
            ("empresa:", "compania:", "cliente final:"),
        ),
        "industria": _texto_por_etiqueta(soup, ("sector:", "categoria:", "industria:"))
        or _extraer_industria_texto(descripcion_empleo),
        "modalidad": _texto_por_etiqueta(soup, ("modalidad:", "teletrabajo:"))
        or _extraer_modalidad_texto(descripcion_empleo),
        "seniority": _texto_por_etiqueta(soup, ("experiencia:", "nivel:", "seniority:"))
        or _extraer_experiencia_metadata(metadata),
        "formacion_requerida": _texto_por_etiqueta(
            soup,
            ("formacion:", "estudios minimos:", "titulacion:"),
        ),
        "metadata": metadata + json_ld.get("metadata", []),
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
