"""Unit tests related to views."""

import uuid

from src.domain.model import Article
from src.services.unit_of_work import AbstractUnitOfWork
from src import views


class TestFetchArticleByIdView:
    async def test_can_fetch_article_by_id(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = (
            Article("First Title", "First Preview", "First Body", created_by=1),
            Article("Second Title", "Second Preview", "Second Body", created_by=2),
        )
        fake_uow.article_repository.create_article(articles[0])
        fake_uow.article_repository.create_article(articles[1])

        fetched_article = await views.articles.fetch_article_by_id(
            articles[1].article_id, uow=fake_uow,
        )

        assert fetched_article == articles[1]

    async def test_cannot_fetch_article_with_nonexistent_id(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        article = Article("First Title", "First Preview", "First Body", created_by=1)
        fake_uow.article_repository.create_article(article)

        fetched_article: Article | None = await views.articles.fetch_article_by_id(
            uuid.uuid4(),
            fake_uow,
        )

        assert not fetched_article


class TestFetchAllArticlesView:
    async def test_can_fetch_all_articles(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = (
            Article("First Title", "First Preview", "First Body", created_by=1),
            Article("Second Title", "Second Preview", "Second Body", created_by=2),
        )
        fake_uow.article_repository.create_article(articles[0])
        fake_uow.article_repository.create_article(articles[1])

        fetched_articles: list[Article] = await views.articles.fetch_all_articles(fake_uow)

        assert articles[0] in fetched_articles
        assert articles[1] in fetched_articles

    async def test_cannot_fetch_articles_from_empty_repo(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        fetched_articles: list[Article] = await views.articles.fetch_all_articles(fake_uow)

        assert not fetched_articles
        assert isinstance(fetched_articles, list)


class TestFetchAllArticlesOfUserView:
    async def test_fetch_all_articles_of_user(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = (
            Article("First Title", "First Preview", "First Body", created_by=1),
            Article("Second Title", "Second Preview", "Second Body", created_by=2),
            Article("Third Title", "Third Preview", "Third Body", created_by=1),
        )
        fake_uow.article_repository.create_article(articles[0])
        fake_uow.article_repository.create_article(articles[1])
        fake_uow.article_repository.create_article(articles[2])

        fetched_articles: list[Article] = await views.articles.fetch_all_articles(
            fake_uow,
            created_by=1,
        )

        assert articles[0] in fetched_articles
        assert articles[2] in fetched_articles

    async def test_cannot_fetch_all_articles_of_nonexistent_user(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        article = Article("First Title", "First Preview", "First Body", created_by=1)
        fake_uow.article_repository.create_article(article)

        fetched_articles: list[Article] = await views.articles.fetch_all_articles(
            fake_uow,
            created_by=2,
        )

        assert not fetched_articles
        assert isinstance(fetched_articles, list)
