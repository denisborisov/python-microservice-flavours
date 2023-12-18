"""Unit of work."""

import abc
import contextvars
import types
import typing

import dependency_injector.wiring
import sqlalchemy.ext.asyncio
import typing_extensions
from sqlalchemy.exc import OperationalError

from ..adapters import google_flashcard_repository, local_flashcard_repository
from ..containers.google_flashcard_repository import GoogleFlashcardRepositoryContainer
from ..containers.session_factory import SessionFactoryContainer
from ..domain.exceptions import DatabaseConnectionError


class AbstractUnitOfWork(typing.Protocol):
    local_flashcard_repository: local_flashcard_repository.AbstractLocalFlashcardRepository
    google_flashcard_repository: google_flashcard_repository.AbstractGoogleFlashcardRepository

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
        repositories: list[
            local_flashcard_repository.AbstractLocalFlashcardRepository
            | google_flashcard_repository.AbstractGoogleFlashcardRepository
        ] = [
            self.local_flashcard_repository,
            self.google_flashcard_repository,
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
        session_factory: sqlalchemy.ext.asyncio.async_sessionmaker = dependency_injector.wiring.Provide[  # noqa: E501
            SessionFactoryContainer.session_factory
        ],
        google_flashcard_repository: google_flashcard_repository.AbstractGoogleFlashcardRepository = dependency_injector.wiring.Provide[  # noqa: E501
            GoogleFlashcardRepositoryContainer.google_flashcard_repository
        ],
    ) -> None:
        self._session_factory = session_factory
        self._session: contextvars.ContextVar[
            sqlalchemy.ext.asyncio.AsyncSession
        ] = contextvars.ContextVar("session")
        self.google_flashcard_repository = google_flashcard_repository

    async def __aenter__(self) -> typing_extensions.Self:
        await super().__aenter__()
        self._session.set(self._session_factory())
        self.local_flashcard_repository = local_flashcard_repository.SqlAlchemyFlashcardRepository(
            self._session.get(),
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.get().close()
        return None

    async def _commit(self) -> None:
        try:
            await self._session.get().commit()
        except OperationalError as ex:
            raise DatabaseConnectionError from ex

    async def _rollback(self) -> None:
        self._session.get().expunge_all()
        try:
            await self._session.get().rollback()
        except OperationalError as ex:
            raise DatabaseConnectionError from ex
