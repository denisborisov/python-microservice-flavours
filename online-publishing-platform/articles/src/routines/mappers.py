"""Routines related to mappers."""

import sqlalchemy.orm

from ..adapters import orm
from ..domain import model


mapper_registry = sqlalchemy.orm.registry()


def start_mappers() -> None:
    mapper_registry.map_imperatively(
        model.Article,
        orm.Article.__table__,
    )


def stop_mappers() -> None:
    mapper_registry.dispose()
