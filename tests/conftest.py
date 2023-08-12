"""General fixtures."""

import pytest
import types
import typing
import typing_extensions

import sqlalchemy.ext.asyncio

from src.adapters.orm import Base
from src.domain.commands import Command
from src.services import unit_of_work
from src.services.http_client import AbstractHttpClient
from src.services.message_bus import MessageBus
from src.services.unit_of_work import AbstractUnitOfWork


class FakeHttpClient(AbstractHttpClient):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
        self.raises_exception_once = False

    async def __aenter__(self) -> typing_extensions.Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        return None

    async def post(self, url: str, headers: dict, params: dict) -> typing.Any:  # noqa: ARG002
        return self.Response({})

    async def get(self, url: str) -> typing.Any:  # noqa: ARG002
        if self.raises_exception_once:
            self.raises_exception_once = False
            raise self.FakeHttpClientError
        return self.Response({})

    class Response:
        def __init__(self, message: dict) -> None:
            self.message = message

        def json(self) -> dict:
            return self.message

    class FakeHttpClientError(Exception):
        pass


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
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory)
    uow.http_client = FakeHttpClient(uow)
    return uow


@pytest.fixture()
def sqlite_bus(sqlite_uow: unit_of_work.AbstractUnitOfWork) -> MessageBus:
    return MessageBus(uow=sqlite_uow)


async def handle(message_bus: MessageBus, command: Command) -> typing.Any:
    message_bus.start_process_events()
    result = await message_bus.handle(command)
    await message_bus.stop_process_events()
    return result
