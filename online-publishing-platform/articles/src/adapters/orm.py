"""Mapping between domain model and SQLAlchemy ORM."""

import sqlalchemy.orm
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    title: sqlalchemy.orm.Mapped[str]
    body: sqlalchemy.orm.Mapped[str]
