"""Integration tests related to article repository's UPDATE operations."""

import uuid

import pytest
import sqlalchemy.ext.asyncio

from src.adapters.articles_repository import SqlAlchemyArticleRepository
from src.domain.exceptions import ArticleModificationError

from .conftest import ServiceClass


class TestModifyArticle:
    @pytest.mark.parametrize(
        ("patch_data", "result"),
        [
            (
                {},
                {"title": "TITLE", "preview": "PREVIEW", "body": "BODY"},
            ),
            (
                {"title": "ANOTHER TITLE"},
                {"title": "ANOTHER TITLE", "preview": "PREVIEW", "body": "BODY"},
            ),
            (
                {"preview": "ANOTHER PREVIEW"},
                {"title": "TITLE", "preview": "ANOTHER PREVIEW", "body": "BODY"},
            ),
            (
                {"body": "ANOTHER BODY"},
                {"title": "TITLE", "preview": "PREVIEW", "body": "ANOTHER BODY"},
            ),
            (
                {"title": "ANOTHER TITLE", "preview": "ANOTHER PREVIEW", "body": "ANOTHER BODY"},
                {"title": "ANOTHER TITLE", "preview": "ANOTHER PREVIEW", "body": "ANOTHER BODY"},
            ),
        ],
    )
    async def test_can_modify_article(
        self,
        patch_data: dict,
        result: dict,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, articles = ServiceClass.create_repository_with_articles(
                session,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )

            retrieved_article = await ServiceClass.update_and_retrieve_article(
                repo,
                {
                    "article_id": articles[0].article_id,  # type: ignore[union-attr]
                    "title": patch_data.get("title"),
                    "preview": patch_data.get("preview"),
                    "body": patch_data.get("body"),
                },
            )

            assert retrieved_article
            assert retrieved_article.title == result["title"]
            assert retrieved_article.preview == result["preview"]
            assert retrieved_article.body == result["body"]
            assert retrieved_article.created_by == articles[0].created_by

    async def test_raises_exception_if_not_found(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo = SqlAlchemyArticleRepository(session)
            article_id = uuid.uuid4()

            with pytest.raises(ArticleModificationError) as exc_info:
                await ServiceClass.update_and_retrieve_article(
                    repo,
                    {
                        "article_id": article_id,
                        "title": "ANOTHER TITLE",
                    },
                )

            assert exc_info.value.args[0] == f"Article with {article_id=} has not been found."
