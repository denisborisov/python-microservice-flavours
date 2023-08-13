"""Schemata for CRUD operations."""

import typing
import uuid

from pydantic import BaseModel


class ArticlePost(BaseModel):
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


class Article(ArticlePost):
    article_id: uuid.UUID

    class Config:
        json_schema_extra: typing.ClassVar[dict] = {
            "example": {
                "article_id": uuid.uuid4(),
                "title": "Заголовок статьи",
                "preview": "Небольшое превью, размером с абзац-два, чтобы понять, "
                           "о чём идёт речь в статье.",
                "body": "Содержимое статьи, сколь угодно большое",
                "created_by": 1,
            },
        }
