"""Integration tests related to local flashcard repository's CREATE operations."""

import sqlalchemy.ext.asyncio

from .conftest import ServiceClass


class TestCreateFlashcard:
    async def test_can_create_flashcard(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, flashcards = ServiceClass.create_local_repository_with_flashcards(
                session,
                {"word": "WORD"},
            )

            assert flashcards[0] in repo.session.new
            assert flashcards[0] in repo.seen
