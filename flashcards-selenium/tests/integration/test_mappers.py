"""Integration tests related to mappers."""

import sqlalchemy.ext.asyncio
from src.adapters import orm
from src.domain import model
from src.routines import mappers

from .conftest import ServiceClass
from src.adapters.local_flashcard_repository import SqlAlchemyFlashcardRepository


class TestMappers:
    def test_imperative_mapping_starts_well(self) -> None:
        expected_result = {
            (model.Flashcard, orm.Flashcard.__table__),
        }

        resulted_mappers = list(mappers.mapper_registry.mappers)

        assert len(resulted_mappers) == 1
        assert (resulted_mappers[0].class_, resulted_mappers[0].local_table) in expected_result

    def test_imperative_mapping_stops_well(self) -> None:
        mappers.stop_mappers()

        resulted_mappers = list(mappers.mapper_registry.mappers)

        assert not resulted_mappers

        mappers.start_mappers()

    async def test_attributes_modified_on_load(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, _ = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            await session.commit()

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

            assert getattr(retrieved_flashcards[0], "events", None) is not None
            assert getattr(retrieved_flashcards[0], "details", None) is None

    async def test_attributes_hidden_on_load(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, _ = ServiceClass.create_local_repository_with_flashcards(
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

    async def test_details_appear_on_flush(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            _, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            await session.flush()

            assert getattr(flashcards[0], "details", None) is not None
