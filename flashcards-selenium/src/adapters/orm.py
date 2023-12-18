"""Mapping between domain model and SQLAlchemy ORM."""

import sqlalchemy.orm
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    pass


class Flashcard(Base):
    __tablename__ = "flashcards"

    word: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(primary_key=True)
    details: sqlalchemy.orm.Mapped[dict[str, list[str]]] = sqlalchemy.orm.mapped_column(
        type_=sqlalchemy.JSON,
    )
