"""Commands."""

import typing
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
