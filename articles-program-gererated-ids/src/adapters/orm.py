"""Mapping between domain model and SQLAlchemy ORM."""

import uuid

import sqlalchemy.orm
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"

    article_id: sqlalchemy.orm.Mapped[uuid.UUID] = sqlalchemy.orm.mapped_column(primary_key=True)
    title: sqlalchemy.orm.Mapped[str]
    preview: sqlalchemy.orm.Mapped[str]
    body: sqlalchemy.orm.Mapped[str]
    created_by: sqlalchemy.orm.Mapped[int]
