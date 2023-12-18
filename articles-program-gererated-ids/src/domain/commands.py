"""Commands."""

import typing
import uuid
from dataclasses import dataclass

from . import exceptions


class Command(typing.Protocol):
    pass


@dataclass
class CreateArticle(Command):
    title: str
    preview: str
    body: str
    created_by: int

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.preview = self.preview.strip()
        self.body = self.body.strip()
        if not self.title:
            raise exceptions.ArticleCreationError("Cannot create an article with an empty title.")
        if not self.preview:
            raise exceptions.ArticleCreationError(
                "Cannot create an article with an empty preview.",
            )
        if not self.body:
            raise exceptions.ArticleCreationError("Cannot create an article with an empty body.")


@dataclass
class UpdateArticle(Command):
    article_id: uuid.UUID
    title: str | None
    preview: str | None
    body: str | None

    def __post_init__(self) -> None:
        if self.title:
            self.title = self.title.strip()
            if not self.title:
                raise exceptions.ArticleModificationError(
                    "Cannot update an article with an empty title.",
                )
        if self.preview:
            self.preview = self.preview.strip()
            if not self.preview:
                raise exceptions.ArticleModificationError(
                    "Cannot update an article with an empty preview.",
                )
        if self.body:
            self.body = self.body.strip()
            if not self.body:
                raise exceptions.ArticleModificationError(
                    "Cannot update an article with an empty body.",
                )


@dataclass
class DeleteArticle(Command):
    article_id: uuid.UUID
