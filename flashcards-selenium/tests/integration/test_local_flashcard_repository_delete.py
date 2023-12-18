"""Integration tests related to local flashcard repository's DELETE operations."""

import pytest
import sqlalchemy.ext.asyncio
from src.adapters.local_flashcard_repository import SqlAlchemyFlashcardRepository
from src.domain import exceptions

from .conftest import ServiceClass


class TestDeleteFlashcard:
    async def test_can_delete_flashcard(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            await repo.delete_flashcard(flashcards[0].word)

            assert not repo.seen

    async def test_raises_exception_if_not_found(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyFlashcardRepository(session)
            word = "WORD"

            with pytest.raises(exceptions.FlashcardDeletionError) as exc_info:
                await repo.delete_flashcard(word)

            assert exc_info.value.args[0] == f"No such flashcard for {word=}."
