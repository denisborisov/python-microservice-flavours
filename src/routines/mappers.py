"""Routines related to mappers."""

import sqlalchemy
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


@sqlalchemy.event.listens_for(model.Article, "load")
def receive_load(article: model.Article, _: sqlalchemy.orm.QueryContext) -> None:
    article.events = []
