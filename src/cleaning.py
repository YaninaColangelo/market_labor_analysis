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
    """Separa titulo y ciudad cuando una fuente los presenta en un mismo texto."""
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


def extraer_valor_meta(metadata: Any, etiquetas: tuple[str, ...]) -> str:
    """Extrae un valor desde metadata usando etiquetas conocidas."""
    for item in _metadata_como_lista(metadata):
        texto = normalizar_texto(item)
        texto_lower = texto.lower()

        for etiqueta in etiquetas:
            etiqueta_lower = etiqueta.lower()
            if texto_lower.startswith(etiqueta_lower):
                if ":" in texto:
                    return normalizar_texto(texto.split(":", 1)[-1])
                return normalizar_texto(texto[len(etiqueta) :])

    return ""


def extraer_empresa_meta(metadata: Any) -> str:
    """Extrae la empresa desde metadatos raw cuando esta disponible."""
    return extraer_valor_meta(metadata, ("empresa:", "compania:", "compania", "cliente final:"))


def extraer_modalidad_meta(metadata: Any) -> str:
    """Extrae modalidad laboral desde metadata cuando esta disponible."""
    valor = extraer_valor_meta(metadata, ("modalidad:", "teletrabajo:", "tipo jornada:"))
    if valor:
        return valor

    texto = " ".join(_metadata_como_lista(metadata)).lower()
    for modalidad in ("remoto", "hibrido", "híbrido", "presencial"):
        if modalidad in texto:
            return "Hibrido" if modalidad == "híbrido" else modalidad.capitalize()

    return ""


def extraer_seniority_meta(metadata: Any) -> str:
    """Extrae seniority o experiencia desde metadata cuando esta disponible."""
    valor = extraer_valor_meta(metadata, ("seniority:", "experiencia:", "nivel:"))
    if valor:
        return valor

    texto = " ".join(_metadata_como_lista(metadata)).lower()
    patrones = (
        ("Junior", r"\b(junior|jr)\b"),
        ("Semi Senior", r"\b(semi senior|semisenior|ssr)\b"),
        ("Senior", r"\b(senior|sr)\b"),
    )
    for etiqueta, patron in patrones:
        if re.search(patron, texto):
            return etiqueta

    return ""


def extraer_fecha_meta(metadata: Any) -> str:
    """Extrae fecha de publicacion desde metadata cuando esta disponible."""
    return extraer_valor_meta(metadata, ("fecha publicacion:", "fecha de publicacion:", "publicado:"))


def extraer_fuente_meta(metadata: Any) -> str:
    """Extrae la fuente desde metadata cuando esta disponible."""
    return extraer_valor_meta(metadata, ("fuente:", "portal:", "sitio:", "source:"))


def extraer_pais_meta(metadata: Any) -> str:
    """Extrae el pais desde metadata cuando esta disponible."""
    return extraer_valor_meta(metadata, ("pais:", "country:"))


def extraer_responsabilidades_meta(metadata: Any) -> str:
    """Extrae responsabilidades o detalle de la oferta desde metadata cuando existe."""
    return extraer_valor_meta(
        metadata,
        (
            "responsabilidades:",
            "funciones:",
            "tareas:",
            "detalle:",
            "descripcion oferta:",
        ),
    )


def extraer_formacion_meta(metadata: Any) -> str:
    """Extrae formacion requerida desde metadata cuando esta disponible."""
    return extraer_valor_meta(
        metadata,
        (
            "formacion:",
            "formacion requerida:",
            "estudios minimos:",
            "estudios mínimos:",
            "titulacion:",
            "titulación:",
        ),
    )


def extraer_industria_meta(metadata: Any) -> str:
    """Extrae industria o sector desde metadata cuando esta disponible."""
    return extraer_valor_meta(metadata, ("industria:", "sector:", "categoria:", "categoría:"))


def extraer_herramientas_meta(metadata: Any) -> list[str]:
    """Identifica herramientas tecnicas mencionadas en los metadatos."""
    texto = " ".join(_metadata_como_lista(metadata)).lower()
    herramientas: list[str] = []

    for herramienta in HERRAMIENTAS_CONOCIDAS:
        patron = r"\b" + re.escape(herramienta.lower()) + r"\b"
        if re.search(patron, texto) and herramienta not in herramientas:
            herramientas.append(herramienta)

    return herramientas
