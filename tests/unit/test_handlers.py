"""Unit tests related to handlers."""

from .conftest import FakeUnitOfWork
from ..conftest import handle
from src.domain import commands
from src.services.message_bus import MessageBus


class TestArticleHandlers:
    async def test_can_create_article(self, fake_uow: FakeUnitOfWork) -> None:
        await handle(
            MessageBus(uow=fake_uow),
            commands.CreateArticle("Title", "Preview", "Body", created_by=1),
        )
        articles = await fake_uow.article_repository.retrieve_all_articles()

        assert fake_uow.committed
        assert articles[0].title == "Title"
        assert articles[0].preview == "Preview"
        assert articles[0].body == "Body"
        assert articles[0].created_by == 1
