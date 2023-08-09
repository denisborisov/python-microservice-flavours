"""Fixtures related to e2e tests."""

import pytest
import typing

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
import sqlalchemy.ext.asyncio

from src.main import app
from src.services import unit_of_work
from src.services.http_client import HttpxClient
from src.services.message_bus import MessageBus


@pytest.fixture
def httpx_client() -> HttpxClient:
    return HttpxClient()


@pytest.fixture
def sqlite_uow(
    httpx_client: HttpxClient,
    sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker
) -> unit_of_work.AbstractUnitOfWork:
    return unit_of_work.SqlAlchemyUnitOfWork(http_client=httpx_client, session_factory=sqlite_session_factory)


@pytest.fixture
def sqlite_bus(sqlite_uow: unit_of_work.AbstractUnitOfWork) -> MessageBus:
    return MessageBus(uow=sqlite_uow)


@pytest.fixture
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
        async with AsyncClient(app=app, base_url="http://test") as client, LifespanManager(app):
            yield client
