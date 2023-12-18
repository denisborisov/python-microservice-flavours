"""Domain model."""

import typing
import uuid


if typing.TYPE_CHECKING:
    from . import events


class Article:
    def __init__(self, title: str, preview: str, body: str, created_by: int) -> None:
        self.article_id = uuid.uuid4()
        self.title = title
        self.preview = preview
        self.body = body
        self.created_by = created_by
        self.events: list[events.Event] = []

    def __hash__(self) -> int:
        return hash(self.article_id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.article_id == other.article_id
        raise NotImplementedError
