"""Fixtures related to e2e tests."""

import typing
import uuid

import httpx
import pytest
import sqlalchemy.ext.asyncio
from asgi_lifespan import LifespanManager

from src.main import app
from src.services import unit_of_work
from src.services.message_bus import MessageBus


@pytest.fixture()
def sqlite_uow(
    sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
) -> unit_of_work.AbstractUnitOfWork:
    return unit_of_work.SqlAlchemyUnitOfWork(
        session_factory=sqlite_session_factory,
    )


@pytest.fixture()
def sqlite_bus(sqlite_uow: unit_of_work.AbstractUnitOfWork) -> MessageBus:
    return MessageBus(uow=sqlite_uow)


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
    async def create_articles(
        async_client: httpx.AsyncClient,
        *article_data: dict,
    ) -> list[typing.Any]:
        json_responses: list[dict] = []
        for article in article_data:
            response = await async_client.post("/api/articles", json=article)
            json_responses.append(response.json())
        return json_responses

    @staticmethod
    async def update_article(
        async_client: httpx.AsyncClient,
        article_data: dict,
    ) -> httpx.Response:
        return await async_client.patch(
            f"/api/articles/{article_data['article_id']}",
            json=article_data,
        )

    @staticmethod
    async def delete_article_and_fetch_all(
        async_client: httpx.AsyncClient,
        article_id: str | uuid.UUID,
    ) -> tuple[httpx.Response, httpx.Response]:
        delete_response = await async_client.delete(f"/api/articles/{article_id}")
        fetchall_response = await async_client.get("/api/articles")
        return delete_response, fetchall_response
