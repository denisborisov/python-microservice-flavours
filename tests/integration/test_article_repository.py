"""Integration tests related to article repository."""

import pytest
import uuid

import sqlalchemy.ext.asyncio

from src.adapters.articles_repository import SqlAlchemyArticleRepository
from src.domain import exceptions
from src.domain.model import Article


class TestCreateArticle:
    async def test_can_create_article(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article = Article("Title", "Preview", "Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article)

            assert article in repo.session.new
            assert article in repo.seen


class TestRetrieveArticleById:
    async def test_can_retrieve_article_by_id(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article = Article("Title", "Preview", "Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article)
            retrieved_article = await repo.retrieve_article_by_id(article.article_id)

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
        article = Article("Title", "Preview", "Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article)

            await session.bind.dispose()
            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_article = await repo.retrieve_article_by_id(article.article_id)
                assert not retrieved_article
                assert retrieved_article not in repo.seen


class TestRetrieveAllArticles:
    async def test_can_retrieve_all_articles(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article_1 = Article("First Title", "First Preview", "First Body", created_by=1)
        article_2 = Article("Second Title", "Second Preview", "Second Body", created_by=2)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article_1)
            repo.create_article(article_2)
            retrieved_articles = await repo.retrieve_all_articles()

            assert retrieved_articles == [article_1, article_2]
            assert repo.seen == {article_1, article_2}

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
        article_1 = Article("First Title", "First Preview", "First Body", created_by=1)
        article_2 = Article("Second Title", "Second Preview", "Second Body", created_by=2)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article_1)
            repo.create_article(article_2)

            await session.bind.dispose()
            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_articles = await repo.retrieve_all_articles()
                assert not retrieved_articles

            assert repo.seen == {article_1, article_2}


class TestRetrieveAllArticlesOfUser:
    async def test_can_retrieve_all_articles_of_user(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article_1 = Article("First Title", "First Preview", "First Body", created_by=1)
        article_2 = Article("Second Title", "Second Preview", "Second Body", created_by=2)
        article_3 = Article("Third Title", "Third Preview", "Third Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article_1)
            repo.create_article(article_2)
            repo.create_article(article_3)
            retrieved_articles = await repo.retrieve_all_articles(created_by=1)

            assert retrieved_articles == [article_1, article_3]
            assert repo.seen == {article_1, article_2, article_3}

    async def test_cannot_retrieve_all_articles_of_user_from_empty_repo(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article_1 = Article("First Title", "First Preview", "First Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article_1)
            retrieved_articles = await repo.retrieve_all_articles(created_by=2)

            assert retrieved_articles == []
            assert repo.seen == {article_1}

    async def test_cannot_retrieve_all_articles_of_user_from_disconnected_database(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article_1 = Article("First Title", "First Preview", "First Body", created_by=1)
        article_2 = Article("Second Title", "Second Preview", "Second Body", created_by=2)
        article_3 = Article("Third Title", "Third Preview", "Third Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article_1)
            repo.create_article(article_2)
            repo.create_article(article_3)

            await session.bind.dispose()
            with pytest.raises(exceptions.DatabaseConnectionError):  # noqa: PT012
                retrieved_articles = await repo.retrieve_all_articles(created_by=1)
                assert not retrieved_articles

            assert repo.seen == {article_1, article_2, article_3}


class TestDeleteArticle:
    async def test_can_delete_article(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article = Article("Title", "Preview", "Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article)
            session.commit()

            await repo.delete_article(article.article_id)
            assert not repo.seen

    async def test_raises_exception_if_not_found(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            article_id = uuid.uuid4()
            with pytest.raises(exceptions.ArticleDeletionError) as exc_info:
                await repo.delete_article(article_id)
            assert exc_info.value.args[0] == f"No such article with {article_id=}."
