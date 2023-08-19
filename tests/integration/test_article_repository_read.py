"""Integration tests related to article repository's READ operations."""

import pytest
import uuid

import sqlalchemy.ext.asyncio

from .conftest import ServiceClass
from src.adapters.articles_repository import SqlAlchemyArticleRepository
from src.domain import exceptions


class TestRetrieveArticleById:
    async def test_can_retrieve_article_by_id(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, article = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )

            retrieved_article = await repo.retrieve_article_by_id(
                article.article_id,  # type: ignore[union-attr]
            )

            assert retrieved_article == article
            assert retrieved_article in repo.seen

    async def test_cannot_retrieve_article_by_nonesxistent_id(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)

            retrieved_article = await repo.retrieve_article_by_id(uuid.uuid4())

            assert retrieved_article is None
            assert retrieved_article not in repo.seen

    async def test_cannot_retrieve_article_by_id_from_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, article = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )

            await session.bind.dispose()

            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_article = await repo.retrieve_article_by_id(
                    article.article_id,  # type: ignore[union-attr]
                )

                assert not retrieved_article
                assert retrieved_article not in repo.seen


class TestRetrieveAllArticles:
    async def test_can_retrieve_all_articles(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, articles = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "FIRST TITLE",
                    "preview": "FIRST PREVIEW",
                    "body": "FIRST BODY",
                    "created_by": 1,
                },
                {
                    "title": "SECOND TITLE",
                    "preview": "SECOND PREVIEW",
                    "body": "SECOND BODY",
                    "created_by": 2,
                },
            )

            retrieved_articles = await repo.retrieve_all_articles()

            assert retrieved_articles == articles
            assert repo.seen == set(articles)  # type: ignore[arg-type]

    async def test_cannot_retrieve_all_articles_from_empty_repo(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)

            retrieved_articles = await repo.retrieve_all_articles()

            assert retrieved_articles == []
            assert repo.seen == set()

    async def test_cannot_retrieve_all_articles_from_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, articles = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "FIRST TITLE",
                    "preview": "FIRST PREVIEW",
                    "body": "FIRST BODY",
                    "created_by": 1,
                },
                {
                    "title": "SECOND TITLE",
                    "preview": "SECOND PREVIEW",
                    "body": "SECOND BODY",
                    "created_by": 2,
                },
            )

            await session.bind.dispose()

            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_articles = await repo.retrieve_all_articles()
                assert not retrieved_articles

            assert repo.seen == set(articles)  # type: ignore[arg-type]


class TestRetrieveAllArticlesOfUser:
    async def test_can_retrieve_all_articles_of_user(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, articles = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "FIRST TITLE",
                    "preview": "FIRST PREVIEW",
                    "body": "FIRST BODY",
                    "created_by": 1,
                },
                {
                    "title": "SECOND TITLE",
                    "preview": "SECOND PREVIEW",
                    "body": "SECOND BODY",
                    "created_by": 2,
                },
                {
                    "title": "THIRD TITLE",
                    "preview": "THIRD PREVIEW",
                    "body": "THIRD BODY",
                    "created_by": 1,
                },
            )

            retrieved_articles = await repo.retrieve_all_articles(created_by=1)

            assert retrieved_articles == [articles[0], articles[2]]  # type: ignore[index]
            assert repo.seen == set(articles)  # type: ignore[arg-type]

    async def test_cannot_retrieve_all_articles_of_user_from_empty_repo(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, article = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )

            retrieved_articles = await repo.retrieve_all_articles(created_by=2)

            assert retrieved_articles == []
            assert repo.seen == {article}

    async def test_cannot_retrieve_all_articles_of_user_from_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, articles = ServiceClass.create_repository_with_one_article(
                session,
                {
                    "title": "FIRST TITLE",
                    "preview": "FIRST PREVIEW",
                    "body": "FIRST BODY",
                    "created_by": 1,
                },
                {
                    "title": "SECOND TITLE",
                    "preview": "SECOND PREVIEW",
                    "body": "SECOND BODY",
                    "created_by": 2,
                },
                {
                    "title": "THIRD TITLE",
                    "preview": "THIRD PREVIEW",
                    "body": "THIRD BODY",
                    "created_by": 1,
                },
            )

            await session.bind.dispose()

            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_articles = await repo.retrieve_all_articles(created_by=1)
                assert not retrieved_articles

            assert repo.seen == set(articles)  # type: ignore[arg-type]
