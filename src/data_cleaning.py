"""Limpieza y normalizacion inicial de ofertas laborales."""

from pathlib import Path

import pandas as pd

from src.utils import DATA_PROCESSED, DATA_RAW, normalize_text, read_csv, save_csv


def clean_offers(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza campos principales sin alterar el texto fuente relevante."""
    cleaned = df.copy()

    text_columns = [
        "pais",
        "ciudad",
        "empresa",
        "industria",
        "titulo_puesto",
        "modalidad",
        "seniority",
    ]

    for column in text_columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip()

    if "fecha_publicacion" in cleaned.columns:
        cleaned["fecha_publicacion"] = pd.to_datetime(cleaned["fecha_publicacion"], errors="coerce")

    searchable_columns = ["descripcion", "responsabilidades", "requisitos"]
    cleaned["texto_analisis"] = (
        cleaned[[col for col in searchable_columns if col in cleaned.columns]]
        .fillna("")
        .agg(" ".join, axis=1)
        .map(normalize_text)
    )

    return cleaned


def run_cleaning(
    input_path: str | Path = DATA_RAW / "ofertas_brutas.csv",
    output_path: str | Path = DATA_PROCESSED / "ofertas_limpias.csv",
) -> pd.DataFrame:
    """Ejecuta la limpieza base y guarda el resultado."""
    df = read_csv(input_path)
    cleaned = clean_offers(df)
    save_csv(cleaned, output_path)
    return cleaned


if __name__ == "__main__":
    result = run_cleaning()
    print(f"Ofertas limpias generadas: {len(result)}")
