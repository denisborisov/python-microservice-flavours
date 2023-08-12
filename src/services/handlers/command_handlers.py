"""Command handlers."""

import typing

from ... import domain
from ..unit_of_work import AbstractUnitOfWork


async def create_article(
    cmd: domain.commands.CreateArticle,
    uow: AbstractUnitOfWork,
) -> None:
    async with uow:
        article = domain.model.Article(cmd.title, cmd.preview, cmd.body, cmd.created_by)
        uow.article_repository.create_article(article)
        await uow.commit()


COMMAND_HANDLERS: dict[
    type[domain.commands.Command],
    typing.Callable[[domain.commands.Command, AbstractUnitOfWork], typing.Any],
] = {
    domain.commands.CreateArticle: create_article,
}
