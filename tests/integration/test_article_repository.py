"""Integration tests related to article repository."""

import uuid

import sqlalchemy.ext.asyncio

from src.adapters.articles_repository import SqlAlchemyArticleRepository
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
