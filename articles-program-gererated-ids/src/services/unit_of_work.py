"""Unit of work."""

import abc
import types
import typing

import dependency_injector.wiring
import sqlalchemy.ext.asyncio
import typing_extensions
from sqlalchemy.exc import OperationalError

from .. import adapters
from ..containers.session_factory import SessionFactoryContainer
from ..domain.exceptions import DatabaseConnectionError


class AbstractUnitOfWork(typing.Protocol):
    article_repository: adapters.articles_repository.AbstractArticleRepository

    async def __aenter__(self) -> typing_extensions.Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        await self.rollback()
        return None

    async def commit(self) -> None:
        await self._commit()

    async def rollback(self) -> None:
        await self._rollback()

    def collect_new_events(self) -> typing.Generator:
        repositories: list[adapters.articles_repository.AbstractArticleRepository] = [
            self.article_repository,
        ]

        for one_repository in repositories:
            for entity in one_repository.seen:
                while entity.events:
                    yield entity.events.pop(0)

    @abc.abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    @dependency_injector.wiring.inject
    def __init__(
        self,
        session_factory: sqlalchemy.ext.asyncio.async_sessionmaker = (
            dependency_injector.wiring.Provide[SessionFactoryContainer.session_factory]
        ),
    ) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> typing_extensions.Self:
        await super().__aenter__()
        self._session: sqlalchemy.ext.asyncio.AsyncSession = self._session_factory()
        self.article_repository = adapters.articles_repository.SqlAlchemyArticleRepository(
            self._session,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.close()
        return None

    async def _commit(self) -> None:
        try:
            await self._session.commit()
        except OperationalError as ex:
            raise DatabaseConnectionError from ex

    async def _rollback(self) -> None:
        self._session.expunge_all()
        try:
            await self._session.rollback()
        except OperationalError as ex:
            raise DatabaseConnectionError from ex
