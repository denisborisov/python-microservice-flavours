"""Views related to categories."""

from ..domain.model import Article
from ..services.unit_of_work import AbstractUnitOfWork


async def fetch_article_by_id(article_id: int, uow: AbstractUnitOfWork) -> Article | None:
    async with uow:
        return await uow.article_repository.retrieve_article_by_id(article_id)


async def fetch_all_articles(uow: AbstractUnitOfWork) -> list[Article]:
    async with uow:
        return await uow.article_repository.retrieve_all_articles()
