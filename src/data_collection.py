"""Funciones base para recoleccion y consolidacion de ofertas laborales."""

from pathlib import Path

import pandas as pd

from src.utils import DATA_RAW, save_csv


RAW_COLUMNS = [
    "id_oferta",
    "fecha_publicacion",
    "fuente",
    "url",
    "pais",
    "ciudad",
    "empresa",
    "industria",
    "titulo_puesto",
    "descripcion",
    "responsabilidades",
    "requisitos",
    "modalidad",
    "seniority",
    "formacion_requerida",
]


def create_empty_raw_template(output_path: str | Path = DATA_RAW / "ofertas_brutas.csv") -> pd.DataFrame:
    """Crea una plantilla de carga manual para ofertas laborales."""
    df = pd.DataFrame(columns=RAW_COLUMNS)
    save_csv(df, output_path)
    return df


def append_manual_offer(offers: pd.DataFrame, offer: dict) -> pd.DataFrame:
    """Agrega una oferta cargada manualmente respetando el esquema base."""
    missing_columns = [column for column in RAW_COLUMNS if column not in offer]
    if missing_columns:
        raise ValueError(f"Faltan campos obligatorios: {missing_columns}")
    return pd.concat([offers, pd.DataFrame([offer], columns=RAW_COLUMNS)], ignore_index=True)
