"""Articles repository."""

import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.model import Article

from ..domain.model import Article


class AbstractArticleRepository(typing.Protocol):
    seen: set[Article]

    def create_article(self, article: Article) -> None:
        self._create_article(article)
        self.seen.add(article)

    async def retrieve_article_by_id(self, article_id: int) -> Article:
        article = await self._retrieve_article_by_id(article_id)
        if article:
            self.seen.add(article)
        return article
    
    async def retrieve_all_articles(self) -> list[Article]:
        articles = await self._retrieve_all_articles()
        for one_article in articles:
            self.seen.add(one_article)
        return articles
    
    def _create_article(self, article: Article) -> None:
        raise NotImplementedError

    async def _retrieve_article_by_id(self, article_id: int) -> Article:
        raise NotImplementedError
    
    async def _retrieve_all_articles(self) -> list[Article]:
        raise NotImplementedError
    

class SqlAlchemyArticleRepository(AbstractArticleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.seen: set[Article] = set()

    def _create_article(self, article: Article) -> None:
        self.session.add(article)

    async def _retrieve_article_by_id(self, article_id: int) -> Article:
        result = await self.session.scalars(sqlalchemy.select(Article).filter(Article.id == article_id))
        return result.first()
    
    async def _retrieve_all_articles(self) -> sqlalchemy.Sequence[Article]:
        result = await self.session.scalars(sqlalchemy.select(Article))
        return result.all()
