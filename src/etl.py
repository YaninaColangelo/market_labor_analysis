"""Transformaciones ETL para ofertas laborales."""

from __future__ import annotations

from typing import Any

from src.cleaning import (
    extraer_empresa_meta,
    extraer_herramientas_meta,
    generar_id,
    normalizar_texto,
    separar_titulo_ciudad,
)


def transformar_oferta(oferta_raw: dict[str, Any]) -> dict[str, Any]:
    """Transforma una oferta raw en una oferta limpia y tabular."""
    titulo_raw = oferta_raw.get("titulo") or oferta_raw.get("titulo_puesto", "")
    titulo_puesto, ciudad = separar_titulo_ciudad(titulo_raw)
    metadata = oferta_raw.get("metadata")
    descripcion = normalizar_texto(oferta_raw.get("descripcion", ""))
    requisitos = normalizar_texto(oferta_raw.get("requisitos", ""))

    herramientas = extraer_herramientas_meta(metadata)
    if not requisitos and herramientas:
        requisitos = "; ".join(herramientas)

    oferta_clean = {
        "id_oferta": oferta_raw.get("id_oferta") or generar_id(oferta_raw.get("url", titulo_raw)),
        "fecha_publicacion": oferta_raw.get("fecha_publicacion"),
        "fuente": oferta_raw.get("fuente", "Tecnoempleo"),
        "url": oferta_raw.get("url"),
        "pais": oferta_raw.get("pais", "Espana"),
        "ciudad": normalizar_texto(oferta_raw.get("ciudad") or ciudad),
        "empresa": normalizar_texto(oferta_raw.get("empresa") or extraer_empresa_meta(metadata)),
        "industria": normalizar_texto(oferta_raw.get("industria", "")),
        "titulo_puesto": titulo_puesto,
        "descripcion": descripcion,
        "responsabilidades": normalizar_texto(oferta_raw.get("responsabilidades", "")),
        "requisitos": requisitos,
        "modalidad": normalizar_texto(oferta_raw.get("modalidad", "")),
        "seniority": normalizar_texto(oferta_raw.get("seniority", "")),
        "formacion_requerida": normalizar_texto(oferta_raw.get("formacion_requerida", "")),
    }
    return oferta_clean
