"""Command handlers."""

import typing
import uuid

from ... import domain
from ..unit_of_work import AbstractUnitOfWork


async def create_article(
    cmd: domain.commands.CreateArticle,
    uow: AbstractUnitOfWork,
) -> uuid.UUID:
    async with uow:
        article = domain.model.Article(cmd.title, cmd.preview, cmd.body, cmd.created_by)
        uow.article_repository.create_article(article)
        await uow.commit()
        return article.article_id


async def update_article(
    cmd: domain.commands.UpdateArticle,
    uow: AbstractUnitOfWork,
) -> None:
    async with uow:
        await uow.article_repository.update_article(
            cmd.article_id,
            cmd.title,
            cmd.preview,
            cmd.body,
        )
        await uow.commit()


async def delete_article(
    cmd: domain.commands.DeleteArticle,
    uow: AbstractUnitOfWork,
) -> None:
    async with uow:
        await uow.article_repository.delete_article(cmd.article_id)
        await uow.commit()


COMMAND_HANDLERS: dict[
    type[domain.commands.Command],
    typing.Callable[[domain.commands.Command, AbstractUnitOfWork], typing.Any],
] = {
    domain.commands.CreateArticle: create_article,  # type: ignore[dict-item]
    domain.commands.UpdateArticle: update_article,  # type: ignore[dict-item]
    domain.commands.DeleteArticle: delete_article,  # type: ignore[dict-item]
}
