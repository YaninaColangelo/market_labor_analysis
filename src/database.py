"""Funciones de persistencia en MySQL."""

from __future__ import annotations

import os
import re
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL


DEFAULT_TABLE = "ofertas"


def _validar_nombre_tabla(table_name: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table_name):
        raise ValueError("Nombre de tabla invalido.")
    return table_name


def crear_engine_mysql(database_url: str | None = None) -> Engine:
    """Crea una conexion SQLAlchemy para MySQL."""
    load_dotenv()
    url = database_url or os.getenv("MYSQL_DATABASE_URL")

    if not url:
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "")
        host = os.getenv("MYSQL_HOST", "localhost")
        port = os.getenv("MYSQL_PORT", "3306")
        database = os.getenv("MYSQL_DATABASE", "market_labor_analysis")
        url = URL.create(
            "mysql+pymysql",
            username=user,
            password=password or None,
            host=host,
            port=int(port),
            database=database,
        )

    return create_engine(url)


def cargar_mysql(
    df: pd.DataFrame,
    table_name: str = DEFAULT_TABLE,
    engine: Engine | None = None,
    if_exists: str = "append",
    **to_sql_kwargs: Any,
) -> int:
    """Inserta un DataFrame en MySQL y devuelve la cantidad de filas enviadas."""
    if df.empty:
        return 0

    connection = engine or crear_engine_mysql()
    table_name = _validar_nombre_tabla(table_name)
    df.to_sql(
        name=table_name,
        con=connection,
        if_exists=if_exists,
        index=False,
        **to_sql_kwargs,
    )
    return len(df)


def leer_ofertas(
    table_name: str = DEFAULT_TABLE,
    engine: Engine | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    """Lee ofertas almacenadas en MySQL."""
    connection = engine or crear_engine_mysql()
    table_name = _validar_nombre_tabla(table_name)
    query = f"SELECT * FROM {table_name}"
    params: dict[str, Any] = {}

    if limit is not None:
        query += " LIMIT :limit"
        params["limit"] = limit

    return pd.read_sql(text(query), connection, params=params)
