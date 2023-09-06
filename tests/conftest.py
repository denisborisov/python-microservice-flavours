"""General fixtures."""

import typing

import pytest
import sqlalchemy.ext.asyncio

from src.adapters.orm import Base
from src.domain.commands import Command
from src.services import unit_of_work
from src.services.message_bus import MessageBus


@pytest.fixture()
async def in_memory_sqlite_db() -> typing.AsyncGenerator:
    engine = sqlalchemy.ext.asyncio.create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture()
def sqlite_session_factory(
    in_memory_sqlite_db: sqlalchemy.ext.asyncio.AsyncEngine,
) -> sqlalchemy.ext.asyncio.async_sessionmaker:
    return sqlalchemy.ext.asyncio.async_sessionmaker(
        bind=in_memory_sqlite_db,
        expire_on_commit=False,
    )


@pytest.fixture()
def sqlite_uow(
    sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
) -> unit_of_work.AbstractUnitOfWork:
    return unit_of_work.SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory)


@pytest.fixture()
def sqlite_bus(sqlite_uow: unit_of_work.AbstractUnitOfWork) -> MessageBus:
    return MessageBus(uow=sqlite_uow)


async def handle(message_bus: MessageBus, command: Command) -> typing.Any:
    message_bus.start_process_events()
    result = await message_bus.handle(command)
    await message_bus.stop_process_events()
    return result
