"""Views related to flashcards."""

import asyncio

from ..domain.events import FlashcardFetchedFromGoogleApi
from ..domain.model import Flashcard
from ..services.message_bus import MessageBus
from ..services.unit_of_work import AbstractUnitOfWork


async def fetch_flashcard_by_word(word: str, bus: MessageBus) -> Flashcard | None:
    async with bus.uow:
        flashcard = await bus.uow.local_flashcard_repository.retrieve_flashcard_by_word(word)

        if flashcard:
            return flashcard

        if flashcard := await asyncio.to_thread(
            bus.uow.google_flashcard_repository.retrieve_flashcard_by_word,
            word,
        ):
            await bus.handle(FlashcardFetchedFromGoogleApi(flashcard))

        return flashcard


async def fetch_all_flashcards(  # noqa: PLR0913
    regular_expression: str,
    with_definitions: bool,
    with_synonyms: bool,
    with_translations: bool,
    with_examples: bool,
    last_retrieved_word: str,
    limit: int,
    uow: AbstractUnitOfWork,
) -> list[Flashcard]:
    async with uow:
        return await uow.local_flashcard_repository.retrieve_all_flashcards(
            regular_expression,
            with_definitions,
            with_synonyms,
            with_translations,
            with_examples,
            last_retrieved_word,
            limit,
        )
