"""Fixtures related to integration tests."""

import typing

import pytest
import sqlalchemy.ext.asyncio

from src.adapters.articles_repository import SqlAlchemyArticleRepository
from src.domain.model import Article
from src.routines import mappers


@pytest.fixture(scope="module", autouse=True)
def _use_mappers() -> typing.Generator:
    mappers.start_mappers()
    yield
    mappers.stop_mappers()


class ServiceClass:
    @staticmethod
    def create_repository_with_articles(
        session: sqlalchemy.ext.asyncio.AsyncSession,
        *article_data: dict,
    ) -> tuple[SqlAlchemyArticleRepository, list[Article]]:
        repo = SqlAlchemyArticleRepository(session)

        articles: list[Article] = []

        for one_dict in article_data:
            article = Article(
                one_dict["title"],
                one_dict["preview"],
                one_dict["body"],
                one_dict["created_by"],
            )
            articles.append(article)
            repo.create_article(article)

        return repo, articles

    @staticmethod
    async def update_and_retrieve_article(
        repo: SqlAlchemyArticleRepository,
        patch_data: dict,
    ) -> Article | None:
        await repo.update_article(
            article_id=patch_data["article_id"],
            title=patch_data.get("title"),
            preview=patch_data.get("preview"),
            body=patch_data.get("body"),
        )

        return await repo.retrieve_article_by_id(patch_data["article_id"])
