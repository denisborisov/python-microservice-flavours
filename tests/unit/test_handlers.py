"""Unit tests related to handlers."""

from .conftest import FakeUnitOfWork
from ..conftest import handle
from src.domain import commands
from src.services.message_bus import MessageBus


class TestArticleHandlers:
    async def test_can_create_article(self, fake_uow: FakeUnitOfWork) -> None:
        article_id = await handle(
            MessageBus(uow=fake_uow),
            commands.CreateArticle("Title", "Preview", "Body", created_by=1),
        )
        articles = await fake_uow.article_repository.retrieve_all_articles()

        assert fake_uow.committed
        assert articles[0].article_id == article_id
        assert articles[0].title == "Title"
        assert articles[0].preview == "Preview"
        assert articles[0].body == "Body"
        assert articles[0].created_by == 1

    async def test_can_delete_article(self, fake_uow: FakeUnitOfWork) -> None:
        first_article_id = await handle(
            MessageBus(uow=fake_uow),
            commands.CreateArticle("First Title", "First Preview", "First Body", created_by=1),
        )
        second_article_id = await handle(
            MessageBus(uow=fake_uow),
            commands.CreateArticle("Second Title", "Second Preview", "Second Body", created_by=2),
        )

        await handle(
            MessageBus(uow=fake_uow),
            commands.DeleteArticle(first_article_id),
        )

        articles = await fake_uow.article_repository.retrieve_all_articles()

        assert fake_uow.committed
        assert articles[0].article_id == second_article_id
        assert articles[0].title == "Second Title"
        assert articles[0].preview == "Second Preview"
        assert articles[0].body == "Second Body"
        assert articles[0].created_by == 2  # noqa: PLR2004
