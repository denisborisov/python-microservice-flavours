"""Fixtures related to integration tests."""

import typing

import pytest
import sqlalchemy.ext.asyncio

from .. import conftest
from src.adapters.local_flashcard_repository import SqlAlchemyFlashcardRepository
from src.domain.model import Flashcard
from src.routines import mappers


@pytest.fixture(scope="module", autouse=True)
def _use_mappers() -> typing.Generator:
    mappers.start_mappers()
    yield
    mappers.stop_mappers()


class ServiceClass:
    @staticmethod
    def create_local_repository_with_flashcards(
        session: sqlalchemy.ext.asyncio.AsyncSession,
        *flashcard_data: dict,
    ) -> tuple[SqlAlchemyFlashcardRepository, list[Flashcard]]:
        local_repo = SqlAlchemyFlashcardRepository(session)

        flashcards: list[Flashcard] = []

        for one_dict in flashcard_data:
            flashcard = conftest.ServiceClass.get_default_flashcard(one_dict)
            flashcards.append(flashcard)
            local_repo.create_flashcard(flashcard)

        return local_repo, flashcards
