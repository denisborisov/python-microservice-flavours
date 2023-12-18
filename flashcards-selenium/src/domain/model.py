"""Domain model."""

import functools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import events


@functools.total_ordering
class Flashcard:
    def __init__(  # noqa: PLR0913
        self,
        word: str,
        definitions: list[str],
        synonyms: list[str],
        translations: list[str],
        examples: list[str],
    ) -> None:
        self.word = word
        self.definitions = definitions
        self.synonyms = synonyms
        self.translations = translations
        self.examples = examples
        self.events: list[events.Event] = []

    def __hash__(self) -> int:
        return hash(self.word)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.word == other.word
        raise NotImplementedError

    def __le__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.word <= other.word
        raise NotImplementedError
