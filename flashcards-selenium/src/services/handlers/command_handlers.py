"""Command handlers."""

import typing

from ... import domain
from ..unit_of_work import AbstractUnitOfWork


async def delete_flashcard(
    cmd: domain.commands.DeleteFlashcard,
    uow: AbstractUnitOfWork,
) -> None:
    async with uow:
        await uow.local_flashcard_repository.delete_flashcard(cmd.word)
        await uow.commit()


COMMAND_HANDLERS: dict[
    type[domain.commands.Command],
    typing.Callable[[domain.commands.Command, AbstractUnitOfWork], typing.Any],
] = {
    domain.commands.DeleteFlashcard: delete_flashcard,  # type: ignore[dict-item]
}
