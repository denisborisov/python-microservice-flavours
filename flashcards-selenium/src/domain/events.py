"""Events."""

from dataclasses import dataclass

from . import exceptions
from .messages import Message
from .model import Flashcard


class Event(Message):
    pass


@dataclass
class FlashcardFetchedFromGoogleApi(Event):
    flashcard: Flashcard

    def __post_init__(self) -> None:
        self.flashcard.word = self.flashcard.word.strip()
        if not self.flashcard.word:
            raise exceptions.FlashcardCreationError(
                "Cannot create an flashcard for an empty word.",
            )
