"""Unit tests related to views."""

import asyncio
import typing

if typing.TYPE_CHECKING:
    from src.domain.model import Flashcard

from .. import conftest
from .conftest import ServiceClass
from src import views
from src.services.message_bus import MessageBus
from src.services.unit_of_work import AbstractUnitOfWork


class TestFetchFlashcardByWordView:
    async def test_can_fetch_flashcard_by_word_from_local_repo(self, fake_bus: MessageBus) -> None:
        flashcards = ServiceClass.create_local_repository_with_flashcards(
            fake_bus.uow,
            {"prefix": "FIRST"},
            {"prefix": "SECOND"},
        )

        fetched_flashcard = await views.flashcards.fetch_flashcard_by_word(
            flashcards[0].word,
            bus=fake_bus,
        )

        assert fetched_flashcard == flashcards[0]

    async def test_can_fetch_flashcard_by_word_from_google_repo(
        self,
        fake_bus: MessageBus,
    ) -> None:
        ServiceClass.create_local_repository_with_flashcards(
            fake_bus.uow,
            {"prefix": "FIRST_"},
            {"prefix": "SECOND_"},
        )
        google_repo, flashcards = conftest.ServiceClass.create_google_repository_with_flashcards()
        fake_bus.uow.google_flashcard_repository = google_repo

        flashcard_from_google: Flashcard | None = await views.flashcards.fetch_flashcard_by_word(
            "WORD",
            bus=fake_bus,
        )

        assert flashcard_from_google

    async def test_cannot_fetch_flashcard_by_nonexistent_word_from_google_repo(
        self,
        fake_bus: MessageBus,
    ) -> None:
        ServiceClass.create_local_repository_with_flashcards(
            fake_bus.uow,
            {"prefix": "FIRST_"},
            {"prefix": "SECOND_"},
        )
        google_repo, flashcards = conftest.ServiceClass.create_google_repository_with_flashcards()
        fake_bus.uow.google_flashcard_repository = google_repo

        flashcard_from_google: Flashcard | None = await views.flashcards.fetch_flashcard_by_word(
            "NO_SUCH_WORD",
            bus=fake_bus,
        )

        assert not flashcard_from_google

    async def test_create_local_flashcard_after_fetching_from_google(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"prefix": "FIRST_"},
            {"prefix": "SECOND_"},
        )
        google_repo, _ = conftest.ServiceClass.create_google_repository_with_flashcards()
        fake_uow.google_flashcard_repository = google_repo

        flashcard_from_google: Flashcard | None = await views.flashcards.fetch_flashcard_by_word(
            "CUP",
            bus=MessageBus(uow=fake_uow),
        )

        await asyncio.sleep(0)
        local_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert flashcard_from_google in local_flashcards

    async def test_cannot_fetch_flashcard_with_nonexistent_word(
        self,
        fake_bus: MessageBus,
    ) -> None:
        fetched_flashcard: Flashcard | None = await views.flashcards.fetch_flashcard_by_word(
            "NO_SUCH_WORD",
            bus=fake_bus,
        )

        assert not fetched_flashcard


class TestFetchAllFlashcardsView:
    async def test_can_fetch_all_flashcards(self, fake_uow: AbstractUnitOfWork) -> None:
        flashcards = ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"prefix": "FIRST"},
            {"prefix": "SECOND"},
        )

        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert flashcards[0] in fetched_flashcards
        assert flashcards[1] in fetched_flashcards

    async def test_can_fetch_all_flashcards_using_regex(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        flashcards = ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"prefix": "FIRST_A"},
            {"prefix": "FIRST_BB"},
            {"prefix": "SECOND_A"},
            {"prefix": "SECOND_BB"},
        )

        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression="^FIRST",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert flashcards[0] in fetched_flashcards
        assert flashcards[1] in fetched_flashcards

    async def test_can_fetch_all_flashcards_hiding_fields(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"word": "WORD"},
        )

        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=False,
            with_synonyms=False,
            with_translations=False,
            with_examples=False,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert getattr(fetched_flashcards[0], "definitions", None) is None
        assert getattr(fetched_flashcards[0], "synonyms", None) is None
        assert getattr(fetched_flashcards[0], "translations", None) is None
        assert getattr(fetched_flashcards[0], "examples", None) is None

    async def test_can_fetch_all_flashcards_sorted(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        flashcards = ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"word": "Z"},
            {"word": "Y"},
            {"word": "A"},
            {"word": "B"},
        )

        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert fetched_flashcards == [
            flashcards[2],
            flashcards[3],
            flashcards[1],
            flashcards[0],
        ]

    async def test_can_fetch_all_flashcards_going_after_a_word(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        flashcards = ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"word": "WORD_A"},
            {"word": "WORD_BB"},
            {"word": "WORD_CCC"},
            {"word": "WORD_DDDD"},
        )

        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="WORD_BB",
            limit=2,
            uow=fake_uow,
        )

        assert fetched_flashcards == [
            flashcards[2],
            flashcards[3],
        ]

    async def test_can_fetch_all_flashcards_with_limit(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        flashcards = ServiceClass.create_local_repository_with_flashcards(
            fake_uow,
            {"word": "WORD_1"},
            {"word": "WORD_2"},
            {"word": "WORD_3"},
            {"word": "WORD_4"},
            {"word": "WORD_5"},
            {"word": "WORD_6"},
        )

        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert fetched_flashcards == [
            flashcards[0],
            flashcards[1],
            flashcards[2],
            flashcards[3],
        ]

    async def test_cannot_fetch_flashcards_from_empty_repo(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        fetched_flashcards: list[Flashcard] = await views.flashcards.fetch_all_flashcards(
            regular_expression=".",
            with_definitions=True,
            with_synonyms=True,
            with_translations=True,
            with_examples=True,
            last_retrieved_word="",
            limit=4,
            uow=fake_uow,
        )

        assert not fetched_flashcards
        assert isinstance(fetched_flashcards, list)
