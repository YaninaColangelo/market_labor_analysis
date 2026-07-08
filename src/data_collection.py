"""Funciones base para recoleccion y consolidacion de ofertas laborales."""

from pathlib import Path
import re

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
ID_OFERTA_PATTERN = re.compile(r"^OF-(\d+)$")


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


def validate_raw_schema(offers: pd.DataFrame) -> None:
    """Valida que el dataset raw tenga las columnas obligatorias."""
    missing_dataset_columns = [column for column in RAW_COLUMNS if column not in offers.columns]
    if missing_dataset_columns:
        raise ValueError(f"Faltan columnas obligatorias en el dataset raw: {missing_dataset_columns}")


def normalize_offer_to_raw_schema(offer: dict) -> dict:
    """Ordena y completa una oferta segun el esquema raw."""
    return {column: offer.get(column) for column in RAW_COLUMNS}


def next_offer_id(offers: pd.DataFrame, prefix: str = "OF", width: int = 3) -> str:
    """Genera el siguiente id incremental del dataset raw."""
    if "id_oferta" not in offers.columns or offers.empty:
        return f"{prefix}-{1:0{width}d}"

    pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$")

    numbers = (
        offers["id_oferta"]
        .dropna()
        .astype(str)
        .str.extract(pattern)[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if numbers.empty else numbers.max() + 1
    return f"{prefix}-{next_number:0{width}d}"


def assign_offer_id(offers: pd.DataFrame, offer: dict, overwrite: bool = False) -> dict:
    """Asigna id incremental si la oferta no tiene id o si se pide sobrescribirlo."""
    offer = offer.copy()

    if overwrite or not offer.get("id_oferta"):
        offer["id_oferta"] = next_offer_id(offers)

    return offer


def append_offer(offers: pd.DataFrame, offer: dict, assign_id: bool = True) -> pd.DataFrame:
    """Agrega una oferta respetando el esquema base."""
    validate_raw_schema(offers)

    offer = normalize_offer_to_raw_schema(offer)

    if assign_id:
        offer = assign_offer_id(offers, offer)

    offer_row = pd.DataFrame([offer], columns=RAW_COLUMNS)
    return pd.concat([offers[RAW_COLUMNS], offer_row], ignore_index=True)


def append_offers(offers: pd.DataFrame, new_offers: list[dict], assign_id: bool = True) -> pd.DataFrame:
    """Agrega multiples ofertas, reemplazando previamente las URLs repetidas."""
    updated = offers.copy()
    validate_raw_schema(updated)

    for offer in new_offers:
        normalized_offer = normalize_offer_to_raw_schema(offer)
        url = normalized_offer.get("url")
        if url:
            updated = updated[updated["url"] != url].copy()

        updated = append_offer(updated, normalized_offer, assign_id=assign_id)

    return updated


def append_manual_offer(offers: pd.DataFrame, offer: dict) -> pd.DataFrame:
    """Mantiene compatibilidad con el nombre usado previamente."""
    return append_offer(offers, offer)
