"""Domain model."""

import typing

from . import events


class Article:
    def __init__(self, title: str, body: str):
        id: int
        self.title = title
        self.body = body
        self.events: list[events.Event] = []

    def __hash__(self) -> int:
        return hash((self.title, self.body))
    
    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, self.__class__):
            return (self.title, self.body) == (other.title, other.body)
        else:
            raise NotImplementedError
