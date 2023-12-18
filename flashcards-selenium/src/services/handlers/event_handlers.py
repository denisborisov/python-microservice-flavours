"""Event handlers."""

import typing

from ...domain import events
from ...services.unit_of_work import AbstractUnitOfWork


async def create_flashcard(
    event: events.FlashcardFetchedFromGoogleApi,
    uow: AbstractUnitOfWork,
) -> None:
    async with uow:
        uow.local_flashcard_repository.create_flashcard(event.flashcard)
        await uow.commit()


EVENT_HANDLERS: dict[
    type[events.Event],
    list[typing.Callable[[events.Event, AbstractUnitOfWork], typing.Awaitable[None]]],
] = {
    events.FlashcardFetchedFromGoogleApi: [create_flashcard],  # type: ignore[list-item]
}
