"""Integration tests related to article repository's CREATE operations."""

import sqlalchemy.ext.asyncio

from .conftest import ServiceClass


class TestCreateArticle:
    async def test_can_create_article(
        self,
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

            assert articles[0] in repo.session.new
            assert articles[0] in repo.seen
