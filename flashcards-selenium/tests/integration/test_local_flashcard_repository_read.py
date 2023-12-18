"""Integration tests related to local flashcard repository's READ operations."""

import pytest
import sqlalchemy.ext.asyncio
from src.adapters.local_flashcard_repository import SqlAlchemyFlashcardRepository
from src.domain import exceptions

from .conftest import ServiceClass


class TestRetrieveFlashcardByWord:
    async def test_can_retrieve_flashcard_by_word(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            retrieved_flashcard = await repo.retrieve_flashcard_by_word(
                flashcards[0].word,
            )

            assert retrieved_flashcard == flashcards[0]
            assert retrieved_flashcard in repo.seen

    async def test_cannot_retrieve_flashcard_by_nonesxistent_word(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyFlashcardRepository(session)

            retrieved_flashcard = await repo.retrieve_flashcard_by_word("WORD")

            assert retrieved_flashcard is None
            assert retrieved_flashcard not in repo.seen

    async def test_cannot_retrieve_flashcard_by_word_from_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            await session.bind.dispose()

            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_flashcard = await repo.retrieve_flashcard_by_word(
                    flashcards[0].word,
                )

                assert not retrieved_flashcard
                assert retrieved_flashcard not in repo.seen


class TestRetrieveAllFlashcards:
    async def test_can_retrieve_all_flashcards(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "FIRST WORD"},
                {"word": "SECOND WORD"},
            )

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=True,
                with_synonyms=True,
                with_translations=True,
                with_examples=True,
                last_retrieved_word="",
                limit=4,
            )

            assert retrieved_flashcards == flashcards
            assert repo.seen == set(flashcards)

    async def test_can_fetch_all_flashcards_using_regex(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"prefix": "FIRST_A"},
                {"prefix": "FIRST_BB"},
                {"prefix": "SECOND_A"},
                {"prefix": "SECOND_BB"},
            )

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=True,
                with_synonyms=True,
                with_translations=True,
                with_examples=True,
                last_retrieved_word="",
                limit=4,
            )

            assert flashcards[0] in retrieved_flashcards
            assert flashcards[1] in retrieved_flashcards

    async def test_can_fetch_all_flashcards_hiding_fields(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            await session.commit()

        async with sqlite_session_factory() as session:
            repo = SqlAlchemyFlashcardRepository(session)

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=False,
                with_synonyms=False,
                with_translations=False,
                with_examples=False,
                last_retrieved_word="",
                limit=4,
            )

            assert getattr(retrieved_flashcards[0], "definitions", None) is None
            assert getattr(retrieved_flashcards[0], "synonyms", None) is None
            assert getattr(retrieved_flashcards[0], "translations", None) is None
            assert getattr(retrieved_flashcards[0], "examples", None) is None

    async def test_can_fetch_all_flashcards_sorted(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "Z"},
                {"word": "Y"},
                {"word": "A"},
                {"word": "B"},
            )

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=True,
                with_synonyms=True,
                with_translations=True,
                with_examples=True,
                last_retrieved_word="",
                limit=4,
            )

            assert retrieved_flashcards == [
                flashcards[2],
                flashcards[3],
                flashcards[1],
                flashcards[0],
            ]

    async def test_can_fetch_all_flashcards_going_after_a_word(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD_A"},
                {"word": "WORD_BB"},
                {"word": "WORD_CCC"},
                {"word": "WORD_DDDD"},
            )

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=True,
                with_synonyms=True,
                with_translations=True,
                with_examples=True,
                last_retrieved_word="WORD_BB",
                limit=4,
            )

            assert retrieved_flashcards == [
                flashcards[2],
                flashcards[3],
            ]

    async def test_can_fetch_all_flashcards_with_limit(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD_1"},
                {"word": "WORD_2"},
                {"word": "WORD_3"},
                {"word": "WORD_4"},
                {"word": "WORD_5"},
                {"word": "WORD_6"},
            )

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=True,
                with_synonyms=True,
                with_translations=True,
                with_examples=True,
                last_retrieved_word="",
                limit=4,
            )

            assert retrieved_flashcards == [
                flashcards[0],
                flashcards[1],
                flashcards[2],
                flashcards[3],
            ]

    async def test_cannot_retrieve_all_flashcards_from_empty_repo(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyFlashcardRepository(session)

            retrieved_flashcards = await repo.retrieve_all_flashcards(
                regular_expression=".",
                with_definitions=True,
                with_synonyms=True,
                with_translations=True,
                with_examples=True,
                last_retrieved_word="",
                limit=4,
            )

            assert retrieved_flashcards == []
            assert repo.seen == set()

    async def test_cannot_retrieve_all_flashcards_from_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "FIRST WORD"},
                {"word": "SECOND WORD"},
            )

            await session.bind.dispose()

            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_flashcards = await repo.retrieve_all_flashcards(
                    regular_expression=".",
                    with_definitions=True,
                    with_synonyms=True,
                    with_translations=True,
                    with_examples=True,
                    last_retrieved_word="",
                    limit=4,
                )
                assert not retrieved_flashcards

            assert repo.seen == set(flashcards)
