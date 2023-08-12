"""Unit tests related to views."""

from src.domain import model
from src.services.unit_of_work import AbstractUnitOfWork
from src import views


def create_articles(uow: AbstractUnitOfWork, *articles: model.Article) -> list[model.Article]:
    for one_article in articles:
        uow.article_repository.create_article(one_article)
    return list(articles)


class TestArticlesViews:
    async def test_can_fetch_article_by_id(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = create_articles(
            fake_uow,
            model.Article("First Title", "First Preview", "First Body", created_by=1),
            model.Article("Second Title", "Second Preview", "Second Body", created_by=2),
        )
        assert articles[0] == await views.articles.fetch_article_by_id(
            article_id=articles[0].article_id, uow=fake_uow,
        )
        assert articles[1] == await views.articles.fetch_article_by_id(
            article_id=articles[1].article_id, uow=fake_uow,
        )

    async def test_can_fetch_all_articles(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = create_articles(
            fake_uow,
            model.Article("First Title", "First Preview", "First Body", created_by=1),
            model.Article("Second Title", "Second Preview", "Second Body", created_by=2),
        )
        assert set(articles) == set(await views.articles.fetch_all_articles(fake_uow))
