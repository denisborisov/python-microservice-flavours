"""Unit tests related to handlers."""

from src.domain import commands
from src.domain.events import FlashcardFetchedFromGoogleApi
from src.domain.model import Flashcard
from src.services.message_bus import MessageBus

from ..conftest import handle
from . import conftest


class ServiceClass:
    @staticmethod
    async def create_flashcard_in_repository(
        fake_uow: conftest.FakeUnitOfWork,
        flashcard: Flashcard,
    ) -> None:
        await handle(MessageBus(uow=fake_uow), FlashcardFetchedFromGoogleApi(flashcard))

    @staticmethod
    async def delete_and_retrieve_flashcard(
        fake_uow: conftest.FakeUnitOfWork,
        flashcard: Flashcard,
    ) -> Flashcard | None:
        await handle(
            MessageBus(uow=fake_uow),
            commands.DeleteFlashcard(flashcard.word),
        )
        return await fake_uow.local_flashcard_repository.retrieve_flashcard_by_word(flashcard.word)


class TestEventHandlers:
    async def test_can_create_flashcard_in_local_repo(
        self,
        fake_uow: conftest.FakeUnitOfWork,
    ) -> None:
        flashcard = Flashcard(
            word="WORD",
            definitions=["DEFINITION"],
            synonyms=["SYNONYM"],
            translations=["TRANSLATION"],
            examples=["EXAMPLE"],
        )

        await ServiceClass.create_flashcard_in_repository(fake_uow, flashcard)

        flashcards = await fake_uow.local_flashcard_repository.retrieve_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
        )

        assert fake_uow.committed
        assert flashcards[0].word == "WORD"


class TestCommandHandlers:
    async def test_can_delete_flashcard_from_local_repo(
        self,
        fake_uow: conftest.FakeUnitOfWork,
    ) -> None:
        flashcards: list[
            Flashcard
        ] = conftest.ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"word": "FIRST"},
            {"word": "SECOND"},
        )

        await ServiceClass.delete_and_retrieve_flashcard(fake_uow, flashcards[1])

        flashcards = await fake_uow.local_flashcard_repository.retrieve_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
        )

        assert fake_uow.committed
        assert flashcards[0].word == "FIRST"
