"""Unit tests related to views."""

from src.domain import model
from src.services.unit_of_work import AbstractUnitOfWork
from src import views


class TestArticlesViews:
    async def test_can_fetch_article_by_id(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = (
            model.Article("First Title", "First Preview", "First Body", created_by=1),
            model.Article("Second Title", "Second Preview", "Second Body", created_by=2),
        )
        fake_uow.article_repository.create_article(articles[0])
        fake_uow.article_repository.create_article(articles[1])

        assert articles[0] == await views.articles.fetch_article_by_id(
            articles[0].article_id, uow=fake_uow,
        )
        assert articles[1] == await views.articles.fetch_article_by_id(
            articles[1].article_id, uow=fake_uow,
        )

    async def test_can_fetch_all_articles(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = (
            model.Article("First Title", "First Preview", "First Body", created_by=1),
            model.Article("Second Title", "Second Preview", "Second Body", created_by=2),
        )
        fake_uow.article_repository.create_article(articles[0])
        fake_uow.article_repository.create_article(articles[1])

        assert set(articles) == set(await views.articles.fetch_all_articles(fake_uow))
