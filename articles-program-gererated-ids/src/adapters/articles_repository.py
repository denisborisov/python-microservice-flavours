"""Articles repository."""

import typing
import uuid

from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain import exceptions
from ..domain.model import Article


class AbstractArticleRepository(typing.Protocol):
    seen: set[Article]

    def create_article(self, article: Article) -> None:
        self._create_article(article)
        self.seen.add(article)

    async def retrieve_article_by_id(self, article_id: uuid.UUID) -> Article | None:
        article = await self._retrieve_article_by_id(article_id)
        if article:
            self.seen.add(article)
        return article

    async def retrieve_all_articles(self, created_by: int | None = None) -> list[Article]:
        articles = await self._retrieve_all_articles(created_by)
        for one_article in articles:
            self.seen.add(one_article)
        return articles

    async def update_article(
        self,
        article_id: uuid.UUID,
        title: str | None,
        preview: str | None,
        body: str | None,
    ) -> None:
        article = await self.retrieve_article_by_id(article_id)
        if not article:
            raise exceptions.ArticleModificationError(
                f"Article with {article_id=} has not been found.",
            )
        article.title = title or article.title
        article.preview = preview or article.preview
        article.body = body or article.body

    async def delete_article(self, article_id: uuid.UUID) -> None:
        article = await self.retrieve_article_by_id(article_id)
        if not article:
            raise exceptions.ArticleDeletionError(f"No such article with {article_id=}.")
        await self._delete_article(article)
        self.seen.remove(article)

    def _create_article(self, article: Article) -> None:
        raise NotImplementedError

    async def _retrieve_article_by_id(self, article_id: uuid.UUID) -> Article | None:
        raise NotImplementedError

    async def _retrieve_all_articles(self, created_by: int | None) -> list[Article]:
        raise NotImplementedError

    async def _delete_article(self, article: Article) -> None:
        raise NotImplementedError


class SqlAlchemyArticleRepository(AbstractArticleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.seen: set[Article] = set()

    def _create_article(self, article: Article) -> None:
        self.session.add(article)

    async def _retrieve_article_by_id(self, article_id: uuid.UUID) -> Article | None:
        try:
            result = await self.session.scalars(
                select(Article).where(Article.article_id == article_id),  # type: ignore[arg-type]
            )
        except OperationalError as ex:
            raise exceptions.DatabaseConnectionError from ex

        return result.first()

    async def _retrieve_all_articles(self, created_by: int | None) -> list[Article]:
        try:
            if created_by:
                result = await self.session.scalars(
                    select(Article).where(
                        Article.created_by == created_by,  # type: ignore[arg-type]
                    ),
                )
            else:
                result = await self.session.scalars(select(Article))
        except OperationalError as ex:
            raise exceptions.DatabaseConnectionError from ex

        return list(result)

    async def _delete_article(self, article: Article) -> None:
        await self.session.delete(article)
