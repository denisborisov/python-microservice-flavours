"""Integration tests related to article repository's CREATE operations."""

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
