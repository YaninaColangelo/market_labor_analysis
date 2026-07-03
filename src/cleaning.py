"""Funciones reutilizables para limpiar ofertas laborales."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any


HERRAMIENTAS_CONOCIDAS = [
    "SQL",
    "Python",
    "Excel",
    "Power BI",
    "Tableau",
    "Looker",
    "Qlik",
    "R",
    "SAS",
    "Spark",
    "Databricks",
    "Snowflake",
    "BigQuery",
    "Azure",
    "AWS",
    "Google Cloud",
    "Git",
]


def normalizar_texto(valor: object) -> str:
    """Normaliza texto para comparaciones y campos analiticos."""
    if valor is None:
        return ""

    texto = str(valor).strip()
    texto = unicodedata.normalize("NFKC", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def generar_id(valor: object) -> str:
    """Genera un id estable para una oferta a partir de su URL o contenido."""
    texto = normalizar_texto(valor).lower()
    digest = hashlib.sha1(texto.encode("utf-8")).hexdigest()[:12]
    return f"TEC-{digest}"


def separar_titulo_ciudad(titulo: object) -> tuple[str, str]:
    """Separa titulo y ciudad cuando Tecnoempleo los presenta en un mismo texto."""
    texto = normalizar_texto(titulo)
    if not texto:
        return "", ""

    patrones = [
        r"^(?P<titulo>.+?)\s+-\s+(?P<ciudad>[^-]+)$",
        r"^(?P<titulo>.+?)\s+\|\s+(?P<ciudad>[^|]+)$",
        r"^(?P<titulo>.+?)\s+en\s+(?P<ciudad>[^,]+)$",
    ]
    for patron in patrones:
        coincidencia = re.match(patron, texto, flags=re.IGNORECASE)
        if coincidencia:
            return (
                normalizar_texto(coincidencia.group("titulo")),
                normalizar_texto(coincidencia.group("ciudad")),
            )

    return texto, ""


def _metadata_como_lista(metadata: Any) -> list[str]:
    if metadata is None:
        return []
    if isinstance(metadata, dict):
        return [f"{clave}: {valor}" for clave, valor in metadata.items()]
    if isinstance(metadata, (list, tuple, set)):
        return [normalizar_texto(item) for item in metadata if normalizar_texto(item)]
    return [normalizar_texto(metadata)]


def extraer_empresa_meta(metadata: Any) -> str:
    """Extrae la empresa desde metadatos raw cuando esta disponible."""
    for item in _metadata_como_lista(metadata):
        texto = normalizar_texto(item)
        texto_lower = texto.lower()
        for etiqueta in ["empresa:", "compania:", "compania", "cliente final:"]:
            if texto_lower.startswith(etiqueta):
                return normalizar_texto(texto.split(":", 1)[-1])
    return ""


def extraer_herramientas_meta(metadata: Any) -> list[str]:
    """Identifica herramientas tecnicas mencionadas en los metadatos."""
    texto = " ".join(_metadata_como_lista(metadata)).lower()
    herramientas: list[str] = []

    for herramienta in HERRAMIENTAS_CONOCIDAS:
        patron = r"\b" + re.escape(herramienta.lower()) + r"\b"
        if re.search(patron, texto) and herramienta not in herramientas:
            herramientas.append(herramienta)

    return herramientas

