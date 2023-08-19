"""Integration tests related to article repository's UPDATE operations."""

import pytest
import uuid

import sqlalchemy.ext.asyncio

from src.adapters.articles_repository import SqlAlchemyArticleRepository
from src.domain.exceptions import ArticleModificationError
from src.domain.model import Article


class TestModifyArticle:
    @pytest.mark.parametrize(
        ("patch_data", "result"),
        [
            (
                {},
                {"title": "Title", "preview": "Preview", "body": "Body"},
            ),
            (
                {"title": "Another Title"},
                {"title": "Another Title", "preview": "Preview", "body": "Body"},
            ),
            (
                {"preview": "Another Preview"},
                {"title": "Title", "preview": "Another Preview", "body": "Body"},
            ),
            (
                {"body": "Another Body"},
                {"title": "Title", "preview": "Preview", "body": "Another Body"},
            ),
            (
                {"title": "Another Title", "preview": "Another Preview", "body": "Another Body"},
                {"title": "Another Title", "preview": "Another Preview", "body": "Another Body"},
            ),
        ],
    )
    async def test_can_modify_article(
        self,
        patch_data: dict,
        result: dict,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        article = Article("Title", "Preview", "Body", created_by=1)
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            repo.create_article(article)

            patch_data["article_id"] = article.article_id
            await repo.update_article(
                article_id=patch_data["article_id"],
                title=patch_data.get("title"),
                preview=patch_data.get("preview"),
                body=patch_data.get("body"),
            )
            retrieved_article = await repo.retrieve_article_by_id(article.article_id)

            assert retrieved_article
            assert retrieved_article.title == result["title"]
            assert retrieved_article.preview == result["preview"]
            assert retrieved_article.body == result["body"]
            assert retrieved_article.created_by == article.created_by

    async def test_raises_exception_if_not_found(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            article_id = uuid.uuid4()
            patch_data: dict = {"article_id": article_id, "title": "Another Title"}
            with pytest.raises(ArticleModificationError) as exc_info:
                await repo.update_article(
                    article_id=patch_data["article_id"],
                    title=patch_data.get("title"),
                    preview=patch_data.get("preview"),
                    body=patch_data.get("body"),
                )
            assert exc_info.value.args[0] == f"Article with {article_id=} has not been found."
