"""Transformaciones ETL para ofertas laborales."""

from __future__ import annotations

from typing import Any

from src.cleaning import (
    extraer_empresa_meta,
    extraer_fecha_meta,
    extraer_formacion_meta,
    extraer_fuente_meta,
    extraer_herramientas_meta,
    extraer_industria_meta,
    extraer_modalidad_meta,
    extraer_pais_meta,
    extraer_responsabilidades_meta,
    extraer_seniority_meta,
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
    responsabilidades = normalizar_texto(
        oferta_raw.get("responsabilidades") or extraer_responsabilidades_meta(metadata)
    )
    requisitos = normalizar_texto(oferta_raw.get("requisitos", ""))

    herramientas = extraer_herramientas_meta(metadata)
    if not requisitos and herramientas:
        requisitos = "; ".join(herramientas)

    oferta_clean = {
        "id_oferta": oferta_raw.get("id_oferta") or generar_id(oferta_raw.get("url", titulo_raw)),
        "fecha_publicacion": oferta_raw.get("fecha_publicacion") or extraer_fecha_meta(metadata),
        "fuente": normalizar_texto(oferta_raw.get("fuente") or extraer_fuente_meta(metadata)),
        "url": oferta_raw.get("url"),
        "pais": normalizar_texto(oferta_raw.get("pais") or extraer_pais_meta(metadata)),
        "ciudad": normalizar_texto(oferta_raw.get("ciudad") or ciudad),
        "empresa": normalizar_texto(oferta_raw.get("empresa") or extraer_empresa_meta(metadata)),
        "industria": normalizar_texto(oferta_raw.get("industria") or extraer_industria_meta(metadata)),
        "titulo_puesto": titulo_puesto,
        "descripcion": descripcion,
        "responsabilidades": responsabilidades,
        "requisitos": requisitos,
        "modalidad": normalizar_texto(oferta_raw.get("modalidad") or extraer_modalidad_meta(metadata)),
        "seniority": normalizar_texto(oferta_raw.get("seniority") or extraer_seniority_meta(metadata)),
        "formacion_requerida": normalizar_texto(
            oferta_raw.get("formacion_requerida") or extraer_formacion_meta(metadata)
        ),
    }
    return oferta_clean
