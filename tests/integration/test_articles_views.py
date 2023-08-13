"""Integration tests related to article views."""

import typing
import uuid

from ..conftest import handle
from src.domain.commands import CreateArticle
from src.services.message_bus import MessageBus
from src.views import articles

if typing.TYPE_CHECKING:
    from src.domain.model import Article


class TestArticlesViews:
    async def test_fetch_article_by_id_view(self, sqlite_bus: MessageBus) -> None:
        await handle(
            sqlite_bus, CreateArticle(
                "First Title", "First Preview", "First Body", created_by=1,
            ),
        )
        article_id = await handle(
            sqlite_bus, CreateArticle(
                "Second Title", "Second Preview", "Second Body", created_by=2,
            ),
        )

        fetched_article: Article | None = await articles.fetch_article_by_id(
            article_id,
            sqlite_bus.uow,
        )

        assert fetched_article
        assert isinstance(fetched_article.article_id, uuid.UUID)
        assert fetched_article.title == "Second Title"
        assert fetched_article.preview == "Second Preview"
        assert fetched_article.body == "Second Body"
        assert fetched_article.created_by == 2  # noqa: PLR2004

    async def test_fetch_all_articles_view(self, sqlite_bus: MessageBus) -> None:
        await handle(
            sqlite_bus, CreateArticle(
                "First Title", "First Preview", "First Body", created_by=1,
            ),
        )
        await handle(
            sqlite_bus, CreateArticle(
                "Second Title", "Second Preview", "Second Body", created_by=2,
            ),
        )

        fetched_articles: list[Article] = await articles.fetch_all_articles(sqlite_bus.uow)

        assert isinstance(fetched_articles[0].article_id, uuid.UUID)
        assert fetched_articles[0].title == "First Title"
        assert fetched_articles[0].preview == "First Preview"
        assert fetched_articles[0].body == "First Body"
        assert fetched_articles[0].created_by == 1

        assert isinstance(fetched_articles[1].article_id, uuid.UUID)
        assert fetched_articles[1].title == "Second Title"
        assert fetched_articles[1].preview == "Second Preview"
        assert fetched_articles[1].body == "Second Body"
        assert fetched_articles[1].created_by == 2  # noqa: PLR2004
