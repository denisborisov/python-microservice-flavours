"""Domain model."""

import typing

if typing.TYPE_CHECKING:
    from . import events


class Article:
    def __init__(self, title: str, preview: str, body: str, created_by: int) -> None:
        self.article_id: int
        self.title = title
        self.preview = preview
        self.body = body
        self.created_by = created_by
        self.events: list[events.Event] = []

    def __hash__(self) -> int:
        return hash((self.title, self.preview, self.body, self.created_by))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.title, self.preview, self.body, self.created_by) == \
                       (other.title, other.preview, other.body, other.created_by)
        raise NotImplementedError
