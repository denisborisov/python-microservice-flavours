"""Fixtures related to unit tests."""

import asyncio
from dataclasses import dataclass
import re

import pytest

from .. import conftest
from src.adapters.local_flashcard_repository import AbstractLocalFlashcardRepository
from src.adapters.google_flashcard_repository import GoogleFlashcardRepository
from src.domain import model
from src.domain.commands import Command
from src.domain.events import Event
from src.services.message_bus import MessageBus
from src.services.unit_of_work import AbstractUnitOfWork


class FakeLocalFlashcardRepository(AbstractLocalFlashcardRepository):
    def __init__(self) -> None:
        self.flashcards: list[model.Flashcard] = []
        self.seen: set[model.Flashcard] = set()

    def _create_flashcard(self, flashcard: model.Flashcard) -> None:
        self.flashcards.append(flashcard)

    async def _retrieve_flashcard_by_word(self, word: str) -> model.Flashcard | None:
        if filtered_flashcards := [
            one_flashcard for one_flashcard in self.flashcards if one_flashcard.word == word
        ]:
            return filtered_flashcards[0]
        return None

    async def _retrieve_all_flashcards(  # noqa: PLR0913
        self,
        regular_expression: str,
        with_definitions: bool,
        with_synonyms: bool,
        with_translations: bool,
        with_examples: bool,
        last_retrieved_word: str,
        limit: int,
    ) -> list[model.Flashcard]:
        flashcards = [
            flashcard
            for flashcard in self.flashcards
            if re.search(regular_expression, flashcard.word)
            and flashcard.word > last_retrieved_word
        ][:limit]
        if not with_definitions:
            for one_flashcard in flashcards:
                del one_flashcard.definitions
        if not with_synonyms:
            for one_flashcard in flashcards:
                del one_flashcard.synonyms
        if not with_translations:
            for one_flashcard in flashcards:
                del one_flashcard.translations
        if not with_examples:
            for one_flashcard in flashcards:
                del one_flashcard.examples
        return sorted(flashcards)

    async def _delete_flashcard(self, flashcard: model.Flashcard) -> None:
        self.flashcards.remove(flashcard)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.local_flashcard_repository = FakeLocalFlashcardRepository()
        self.google_flashcard_repository = GoogleFlashcardRepository(
            web_scraper=conftest.FakeWebScraper(),
        )
        self.committed = False

    async def _commit(self) -> None:
        self.committed = True

    async def _rollback(self) -> None:
        pass


@dataclass
class CreateFlashcardWithTwoEvents(Command):
    first_event: Event
    second_event: Event


@dataclass
class SayHello(Event):
    message: str


@dataclass
class SendTwoEmails(Event):
    message: str


@dataclass
class SleepEvent(Event):
    seconds: float


async def say_hello(
    event: SayHello,
    _: AbstractUnitOfWork,
) -> None:
    print(f"{event.message}")  # noqa: T201


async def send_first_email(
    event: SendTwoEmails,
    _: AbstractUnitOfWork,
) -> None:
    print(f"{event.message}")  # noqa: T201


async def send_second_email(
    event: SendTwoEmails,
    _: AbstractUnitOfWork,
) -> None:
    print(f"{event.message}")  # noqa: T201


async def sleep_for(
    event: SleepEvent,
    _: AbstractUnitOfWork,
) -> None:
    print(".", end="")  # noqa: T201
    await asyncio.sleep(event.seconds)


event_handlers = {
    SayHello: [say_hello],
    SendTwoEmails: [send_first_email, send_second_email],
    SleepEvent: [sleep_for],
}


async def create_flashcard_with_two_events(
    cmd: CreateFlashcardWithTwoEvents,
    uow: AbstractUnitOfWork,
) -> None:
    flashcard = model.Flashcard(
        word="WORD",
        definitions=["FIRST DEFINITION", "SECOND DEFINITION"],
        synonyms=["FIRST SYNONYM", "SECOND SYNONYM"],
        translations=["FIRST TRANSLATION", "SECOND TRANSLATION"],
        examples=["FIRST EXAMPLE", "SECOND EXAMPLE"],
    )
    flashcard.events = [cmd.first_event, cmd.second_event]
    uow.local_flashcard_repository.create_flashcard(flashcard)


command_handlers = {
    CreateFlashcardWithTwoEvents: create_flashcard_with_two_events,
}


@pytest.fixture()
def fake_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture()
def fake_bus(fake_uow: AbstractUnitOfWork) -> MessageBus:
    bus = MessageBus(uow=fake_uow)
    bus._command_handlers = command_handlers  # type: ignore[assignment]  # noqa: SLF001
    bus._event_handlers = event_handlers  # type: ignore[assignment]  # noqa: SLF001
    return bus


async def handle(fake_bus: MessageBus, command: Command) -> None:
    fake_bus.start_process_events()
    await fake_bus.handle(command)
    await fake_bus.stop_process_events()


class ServiceClass:
    @staticmethod
    def create_local_repository_with_flashcards(
        fake_uow: AbstractUnitOfWork,
        *flashcards_data: dict,
    ) -> list[model.Flashcard]:
        flashcards: list[model.Flashcard] = []
        for one_dict in flashcards_data:
            one_flashcard = conftest.ServiceClass.get_default_flashcard(one_dict)
            flashcards.append(one_flashcard)
            fake_uow.local_flashcard_repository.create_flashcard(one_flashcard)

        return flashcards
