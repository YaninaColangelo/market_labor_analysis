"""Creacion de variables analiticas para interpretar el mercado laboral."""

import pandas as pd


def add_business_orientation_score(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula un puntaje simple de orientacion a negocio entre 1 y 5."""
    output = df.copy()
    text = output.get("texto_analisis", pd.Series([""] * len(output))).fillna("").str.lower()

    business_terms = [
        "negocio",
        "decision",
        "decisiones",
        "indicadores",
        "kpi",
        "gerencia",
        "clientes",
        "ventas",
        "procesos",
        "recomendaciones",
    ]

    counts = text.map(lambda value: sum(term in value for term in business_terms))
    output["nivel_orientacion_negocio"] = counts.clip(lower=1, upper=5)
    return output


def add_market_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa ofertas por pais y seniority para facilitar comparaciones."""
    output = df.copy()
    output["segmento_mercado"] = (
        output.get("pais", "No especificado").astype(str)
        + " - "
        + output.get("seniority", "No especificado").astype(str)
    )
    return output
