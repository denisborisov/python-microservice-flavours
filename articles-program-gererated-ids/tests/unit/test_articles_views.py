"""Unit tests related to views."""

import uuid

from src import views
from src.domain.model import Article
from src.services.unit_of_work import AbstractUnitOfWork


class ServiceClass:
    @staticmethod
    def create_articles_in_repository(
        fake_uow: AbstractUnitOfWork,
        *article_data: dict,
    ) -> list[Article]:
        articles: list[Article] = []
        for one_dict in article_data:
            article = Article(
                one_dict["title"],
                one_dict["preview"],
                one_dict["body"],
                one_dict["created_by"],
            )
            articles.append(article)
            fake_uow.article_repository.create_article(article)
        return articles


class TestFetchArticleByIdView:
    async def test_can_fetch_article_by_id(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = ServiceClass.create_articles_in_repository(
            fake_uow,
            {
                "title": "FIRST TITLE",
                "preview": "FIRST PREVIEW",
                "body": "FIRST BODY",
                "created_by": 1,
            },
            {
                "title": "SECOND TITLE",
                "preview": "SECOND PREVIEW",
                "body": "SECOND BODY",
                "created_by": 2,
            },
        )

        fetched_article = await views.articles.fetch_article_by_id(
            articles[0].article_id,
            uow=fake_uow,
        )

        assert fetched_article == articles[0]

    async def test_cannot_fetch_article_with_nonexistent_id(
        self,
        fake_uow: AbstractUnitOfWork,
    ) -> None:
        ServiceClass.create_articles_in_repository(
            fake_uow,
            {
                "title": "FIRST TITLE",
                "preview": "FIRST PREVIEW",
                "body": "FIRST BODY",
                "created_by": 1,
            },
        )

        fetched_article: Article | None = await views.articles.fetch_article_by_id(
            uuid.uuid4(),
            fake_uow,
        )

        assert not fetched_article


class TestFetchAllArticlesView:
    async def test_can_fetch_all_articles(self, fake_uow: AbstractUnitOfWork) -> None:
        articles = ServiceClass.create_articles_in_repository(
            fake_uow,
            {
                "title": "FIRST TITLE",
                "preview": "FIRST PREVIEW",
                "body": "FIRST BODY",
                "created_by": 1,
            },
            {
                "title": "SECOND TITLE",
                "preview": "SECOND PREVIEW",
                "body": "SECOND BODY",
                "created_by": 2,
            },
        )

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
        articles = ServiceClass.create_articles_in_repository(
            fake_uow,
            {
                "title": "FIRST TITLE",
                "preview": "FIRST PREVIEW",
                "body": "FIRST BODY",
                "created_by": 1,
            },
            {
                "title": "SECOND TITLE",
                "preview": "SECOND PREVIEW",
                "body": "SECOND BODY",
                "created_by": 2,
            },
            {
                "title": "THIRD TITLE",
                "preview": "THIRD PREVIEW",
                "body": "THIRD BODY",
                "created_by": 1,
            },
        )

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
        fetched_articles: list[Article] = await views.articles.fetch_all_articles(
            fake_uow,
            created_by=1,
        )

        assert not fetched_articles
        assert isinstance(fetched_articles, list)
