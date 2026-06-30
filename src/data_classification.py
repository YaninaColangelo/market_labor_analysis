"""Clasificacion inicial de necesidades, competencias y herramientas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.utils import DATA_PROCESSED, contains_any, read_csv, save_csv


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


NECESIDAD_RULES = [
    Rule("Seguimiento de indicadores y performance", ("indicadores", "kpi", "performance", "ventas", "margenes")),
    Rule("Soporte a la toma de decisiones", ("decision", "decisiones", "recomendaciones", "estrategia")),
    Rule("Automatizacion y eficiencia operativa", ("automatizacion", "eficiencia", "optimizar", "automatizar")),
    Rule("Conocimiento de clientes usuarios o mercado", ("clientes", "usuarios", "mercado", "segmentacion")),
    Rule("Control de gestion y reporting ejecutivo", ("control de gestion", "gerencia", "reportes mensuales", "direccion")),
    Rule("Mejora de procesos internos", ("procesos", "operaciones", "desviaciones", "servicio")),
    Rule("Gobernanza calidad y disponibilidad de datos", ("calidad", "validar", "documentar", "limpiar bases")),
]

COMPETENCIA_RULES = [
    Rule("analisis de negocio", ("negocio", "comercial", "metricas", "indicadores")),
    Rule("visualizacion y reporting", ("dashboard", "tablero", "power bi", "tableau", "reportes")),
    Rule("calidad de datos", ("calidad", "validar", "limpiar", "definiciones")),
    Rule("comunicacion con stakeholders", ("stakeholders", "presentar", "comunicar", "gerencia")),
    Rule("automatizacion", ("automatizacion", "python", "integrar datos")),
]

HERRAMIENTA_RULES = [
    Rule("SQL", ("sql",)),
    Rule("Python", ("python",)),
    Rule("Power BI", ("power bi",)),
    Rule("Tableau", ("tableau",)),
    Rule("Excel", ("excel",)),
    Rule("Looker", ("looker",)),
    Rule("dbt", ("dbt",)),
    Rule("BigQuery", ("bigquery",)),
]


def classify_first_match(text: str, rules: list[Rule], default: str = "No clasificado") -> str:
    """Devuelve la primera categoria que coincide con el texto."""
    for rule in rules:
        if contains_any(text, rule.keywords):
            return rule.label
    return default


def classify_multiple(text: str, rules: list[Rule]) -> str:
    """Devuelve etiquetas multiples separadas por punto y coma."""
    labels = [rule.label for rule in rules if contains_any(text, rule.keywords)]
    return "; ".join(dict.fromkeys(labels)) if labels else "No especificado"


def classify_offers(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega variables de clasificacion orientadas a valor organizacional."""
    classified = df.copy()
    text = classified.get("texto_analisis", pd.Series([""] * len(classified))).fillna("")

    classified["necesidad_organizacional"] = text.map(
        lambda value: classify_first_match(value, NECESIDAD_RULES)
    )
    classified["competencias_requeridas"] = text.map(lambda value: classify_multiple(value, COMPETENCIA_RULES))
    classified["herramientas_mencionadas"] = text.map(lambda value: classify_multiple(value, HERRAMIENTA_RULES))

    return classified


def run_classification(
    input_path: str | Path = DATA_PROCESSED / "ofertas_limpias.csv",
    output_path: str | Path = DATA_PROCESSED / "ofertas_clasificadas.csv",
) -> pd.DataFrame:
    """Ejecuta la clasificacion inicial y guarda el dataset procesado."""
    df = read_csv(input_path)
    classified = classify_offers(df)
    save_csv(classified, output_path)
    return classified
