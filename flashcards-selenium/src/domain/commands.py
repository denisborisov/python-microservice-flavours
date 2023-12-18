"""Commands."""

from dataclasses import dataclass

from .messages import Message


class Command(Message):
    pass


@dataclass
class DeleteFlashcard(Command):
    word: str
