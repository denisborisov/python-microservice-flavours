"""Database engine."""

import sqlalchemy.ext.asyncio

from ..settings import AppSettings


def get_database_engine() -> sqlalchemy.ext.asyncio.AsyncEngine:
    return sqlalchemy.ext.asyncio.create_async_engine(
        AppSettings.postgres_dsn,
        echo=True,
    )
