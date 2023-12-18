"""Integration tests related to unit of work."""

import contextlib
import uuid

import pytest
import sqlalchemy.ext.asyncio
from sqlalchemy import text

from src.domain.exceptions import DatabaseConnectionError
from src.services.unit_of_work import SqlAlchemyUnitOfWork


class ServiceClass:
    class MyError(Exception):
        pass

    @staticmethod
    async def insert_one_article_in_database(
        uow: SqlAlchemyUnitOfWork,
        commit_after_insert: bool,
        generate_exception: bool = False,
    ) -> None:
        await uow._session.execute(  # noqa: SLF001
            text(
                "INSERT INTO articles (article_id, title, preview, body, created_by) "
                "VALUES (:article_id, :title, :preview, :body, :created_by)",
            ),
            {
                "article_id": str(uuid.uuid4()),
                "title": "TITLE",
                "preview": "PREVIEW",
                "body": "BODY",
                "created_by": 1,
            },
        )
        if commit_after_insert:
            await uow.commit()
        if generate_exception:
            raise ServiceClass.MyError


class TestUnitOfWork:
    async def test_saves_changes_on_commit(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await ServiceClass.insert_one_article_in_database(
                uow,
                commit_after_insert=True,
            )

        async with sqlite_session_factory() as new_session:
            articles = await new_session.execute(text("SELECT * FROM articles"))

            assert len(list(articles)) == 1

    async def test_rolls_back_uncommitted_work_by_default(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await ServiceClass.insert_one_article_in_database(
                uow,
                commit_after_insert=False,
            )

        async with sqlite_session_factory() as new_session:
            articles = await new_session.execute(text("SELECT * FROM articles"))

            assert not list(articles)

    async def test_rolls_back_on_error(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        with contextlib.suppress(ServiceClass.MyError):
            async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
                await ServiceClass.insert_one_article_in_database(
                    uow,
                    commit_after_insert=False,
                    generate_exception=True,
                )

        async with sqlite_session_factory() as new_session:
            articles = await new_session.execute(text("SELECT * FROM articles"))

            assert not list(articles)

    async def test_raises_exception_when_commit_on_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await ServiceClass.insert_one_article_in_database(
                uow,
                commit_after_insert=False,
            )

            await uow._session.bind.dispose()  # type: ignore[union-attr] # noqa: SLF001

            with pytest.raises(DatabaseConnectionError):
                await uow.commit()

    async def test_raises_exception_when_rollback_on_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await ServiceClass.insert_one_article_in_database(
                uow,
                commit_after_insert=False,
            )

            await uow._session.bind.dispose()  # type: ignore[union-attr] # noqa: SLF001

            with pytest.raises(DatabaseConnectionError):
                await uow.rollback()
