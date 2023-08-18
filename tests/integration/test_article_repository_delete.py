"""Integration tests related to article repository's DELETE operations."""

import pytest
import uuid

import sqlalchemy.ext.asyncio

from src.adapters.articles_repository import SqlAlchemyArticleRepository
from src.domain import exceptions
from src.domain.model import Article


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
