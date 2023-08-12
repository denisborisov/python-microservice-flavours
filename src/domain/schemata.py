"""Schemata for CRUD operations."""

import typing

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    preview: str
    body: str
    created_by: int

    class Config:
        json_schema_extra: typing.ClassVar[dict] = {
            "example": {
                "title": "Заголовок статьи",
                "preview": "Небольшое превью, размером с абзац-два, чтобы понять, "
                           "о чём идёт речь в статье.",
                "body": "Содержимое статьи, сколь угодно большое",
                "created_by": 1,
            },
        }


class Article(ArticleCreate):
    article_id: int

    class Config:
        json_schema_extra: typing.ClassVar[dict] = {
            "example": {
                "article_id": 1,
                "title": "Заголовок статьи",
                "preview": "Небольшое превью, размером с абзац-два, чтобы понять, "
                           "о чём идёт речь в статье.",
                "body": "Содержимое статьи, сколь угодно большое",
                "created_by": 1,
            },
        }
