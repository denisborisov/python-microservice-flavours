"""Integration tests related to unit of work."""

import contextlib
import pytest
import uuid

from sqlalchemy import text
import sqlalchemy.ext.asyncio

from src.domain.exceptions import DatabaseConnectionError
from src.services.unit_of_work import SqlAlchemyUnitOfWork


async def insert_article(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    title: str,
    preview: str,
    body: str,
    created_by: int,
) -> None:
    await session.execute(
        text(
            "INSERT INTO articles (article_id, title, preview, body, created_by) "
            "VALUES (:article_id, :title, :preview, :body, :created_by)",
        ),
        {
            "article_id": str(uuid.uuid4()),
            "title": title,
            "preview": preview,
            "body": body,
            "created_by": created_by,
        },
    )


class TestUnitOfWork:
    async def test_saves_changes_on_commit(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await insert_article(
                uow._session,  # noqa: SLF001
                "Title",
                "Preview",
                "Body",
                created_by=1,
            )
            await uow.commit()

        async with sqlite_session_factory() as new_session:
            articles = await new_session.execute(text("SELECT * FROM articles"))
            assert len(list(articles)) == 1

    async def test_rolls_back_uncommitted_work_by_default(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await insert_article(
                uow._session,  # noqa: SLF001
                "Title",
                "Preview",
                "Body",
                created_by=1,
            )

        async with sqlite_session_factory() as new_session:
            articles = await new_session.execute(text("SELECT * FROM articles"))
            assert not list(articles)

    async def test_rolls_back_on_error(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        class MyError(Exception):
            pass

        with contextlib.suppress(MyError):
            async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
                await insert_article(
                    uow._session,  # noqa: SLF001
                    "Title",
                    "Preview",
                    "Body",
                    created_by=1,
                )
                raise MyError

        async with sqlite_session_factory() as new_session:
            articles = await new_session.execute(text("SELECT * FROM articles"))
            assert not list(articles)

    async def test_raises_exception_when_commit_on_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await insert_article(
                uow._session,  # noqa: SLF001
                "Title",
                "Preview",
                "Body",
                created_by=1,
            )
            await uow._session.bind.dispose()  # type: ignore[union-attr] # noqa: SLF001
            with pytest.raises(DatabaseConnectionError):
                await uow.commit()

    async def test_raises_exception_when_rollback_on_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory) as uow:
            await insert_article(
                uow._session,  # noqa: SLF001
                "Title",
                "Preview",
                "Body",
                created_by=1,
            )
            await uow._session.bind.dispose()  # type: ignore[union-attr] # noqa: SLF001
            with pytest.raises(DatabaseConnectionError):
                await uow.rollback()
