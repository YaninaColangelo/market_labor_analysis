"""Utilidades compartidas del proyecto."""

from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Lee un CSV usando UTF-8 y devuelve un DataFrame."""
    return pd.read_csv(path, encoding=kwargs.pop("encoding", "utf-8"), **kwargs)


def save_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Guarda un DataFrame en CSV creando la carpeta destino si no existe."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")


def normalize_text(value: object) -> str:
    """Normaliza texto para busquedas simples y reglas de clasificacion."""
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    """Indica si un texto contiene alguna palabra o frase de una lista."""
    normalized = normalize_text(text)
    return any(keyword.lower() in normalized for keyword in keywords)
