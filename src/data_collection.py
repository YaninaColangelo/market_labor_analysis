"""Funciones base para recoleccion y consolidacion de ofertas laborales."""

from pathlib import Path

import pandas as pd

from src.utils import DATA_RAW, read_csv, save_csv


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


RAW_DATASET_PATH = DATA_RAW / "ofertas_brutas.csv"


def create_empty_raw_template(output_path: str | Path = DATA_RAW / "ofertas_brutas.csv") -> pd.DataFrame:
    """Crea una plantilla de carga manual para ofertas laborales."""
    df = pd.DataFrame(columns=RAW_COLUMNS)
    save_csv(df, output_path)
    return df


def load_raw_dataset(input_path: str | Path = RAW_DATASET_PATH) -> pd.DataFrame:
    """Carga el dataset raw o devuelve una estructura vacia compatible."""
    input_path = Path(input_path)
    if not input_path.exists():
        return pd.DataFrame(columns=RAW_COLUMNS)
    return read_csv(input_path)


def save_raw_dataset(df: pd.DataFrame, output_path: str | Path = RAW_DATASET_PATH) -> None:
    """Guarda el dataset raw usando la convencion del proyecto."""
    save_csv(df, output_path)


def append_offer(offers: pd.DataFrame, offer: dict) -> pd.DataFrame:
    """Agrega una oferta cargada manualmente respetando el esquema base."""
    missing_offer_columns = [column for column in RAW_COLUMNS if column not in offer]
    if missing_offer_columns:
        raise ValueError(f"Faltan campos obligatorios en la oferta: {missing_offer_columns}")

    missing_dataset_columns = [column for column in RAW_COLUMNS if column not in offers.columns]
    if missing_dataset_columns:
        raise ValueError(f"Faltan columnas obligatorias en el dataset raw: {missing_dataset_columns}")

    offer_row = pd.DataFrame([offer], columns=RAW_COLUMNS)
    return pd.concat([offers[RAW_COLUMNS], offer_row], ignore_index=True)


def append_manual_offer(offers: pd.DataFrame, offer: dict) -> pd.DataFrame:
    """Mantiene compatibilidad con el nombre usado previamente."""
    return append_offer(offers, offer)
