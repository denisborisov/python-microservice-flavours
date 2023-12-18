"""Fixtures related to e2e tests."""

import typing

import httpx
import pytest
import sqlalchemy.ext.asyncio
from asgi_lifespan import LifespanManager

from .. import conftest
from src.domain.model import Flashcard
from src.main import app
from src.services import unit_of_work
from src.services.message_bus import MessageBus


@pytest.fixture()
def sqlite_uow(
    sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
) -> unit_of_work.AbstractUnitOfWork:
    return unit_of_work.SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory)


@pytest.fixture()
async def async_client(
    in_memory_sqlite_db: sqlalchemy.ext.asyncio.AsyncEngine,
    sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    sqlite_uow: unit_of_work.AbstractUnitOfWork,
    sqlite_bus: MessageBus,
) -> typing.AsyncGenerator:
    with (
        getattr(app, "database_engine_container").database_engine.override(in_memory_sqlite_db),
        getattr(app, "session_factory_container").session_factory.override(sqlite_session_factory),
        getattr(app, "unit_of_work_container").sql_alchemy_unit_of_work.override(sqlite_uow),
        getattr(app, "message_bus_container").message_bus.override(sqlite_bus),
    ):
        async with httpx.AsyncClient(
            app=app,
            base_url="http://test",
        ) as client, LifespanManager(app):
            yield client


class ServiceClass:
    @staticmethod
    async def create_flashcards_in_local_repo(
        async_client: httpx.AsyncClient,
        *flashcard_data: dict,
    ) -> list[Flashcard]:
        app_unit_of_work = getattr(
            async_client._transport,  # noqa: SLF001
            "app",
        ).unit_of_work_container.sql_alchemy_unit_of_work

        async with app_unit_of_work() as uow:
            _, flashcards = await conftest.ServiceClass.create_local_repository_with_flashcards(
                uow,
                *flashcard_data,
            )
            await uow.commit()

        return flashcards

    @staticmethod
    async def delete_flashcard_and_fetch_all(
        async_client: httpx.AsyncClient,
        word: str,
    ) -> tuple[httpx.Response, httpx.Response]:
        delete_response = await async_client.delete(f"/api/flashcards/{word}")
        fetchall_response = await async_client.get(
            "/api/flashcards",
            params={
                "regular_expression": ".",
                "with_definitions": True,
                "with_synonyms": True,
                "with_translations": True,
                "with_examples": True,
                "last_retrieved_word": "",
                "limit": 100,
            },
        )
        return delete_response, fetchall_response
