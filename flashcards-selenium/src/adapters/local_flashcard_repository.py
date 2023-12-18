"""Flashcard repository."""

import typing

from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain import exceptions
from ..domain.model import Flashcard


class AbstractLocalFlashcardRepository(typing.Protocol):
    seen: set[Flashcard]

    def create_flashcard(self, flashcard: Flashcard) -> None:
        self._create_flashcard(flashcard)
        self.seen.add(flashcard)

    async def retrieve_flashcard_by_word(self, word: str) -> Flashcard | None:
        flashcard = await self._retrieve_flashcard_by_word(word)
        if flashcard:
            self.seen.add(flashcard)
        return flashcard

    async def retrieve_all_flashcards(  # noqa: PLR0913
        self,
        regular_expression: str,
        with_definitions: bool,
        with_synonyms: bool,
        with_translations: bool,
        with_examples: bool,
        last_retrieved_word: str,
        limit: int,
    ) -> list[Flashcard]:
        flashcards = await self._retrieve_all_flashcards(
            regular_expression,
            with_definitions,
            with_synonyms,
            with_translations,
            with_examples,
            last_retrieved_word,
            limit,
        )
        for one_flashcard in flashcards:
            self.seen.add(one_flashcard)
        return flashcards

    async def delete_flashcard(self, word: str) -> None:
        flashcard = await self.retrieve_flashcard_by_word(word)
        if not flashcard:
            raise exceptions.FlashcardDeletionError(f"No such flashcard for {word=}.")
        await self._delete_flashcard(flashcard)
        self.seen.remove(flashcard)

    def _create_flashcard(self, flashcard: Flashcard) -> None:
        raise NotImplementedError

    async def _retrieve_flashcard_by_word(self, word: str) -> Flashcard | None:
        raise NotImplementedError

    async def _retrieve_all_flashcards(  # noqa: PLR0913
        self,
        regular_expression: str,
        with_definitions: bool,
        with_synonyms: bool,
        with_translations: bool,
        with_examples: bool,
        last_retrieved_word: str,
        limit: int,
    ) -> list[Flashcard]:
        raise NotImplementedError

    async def _delete_flashcard(self, flashcard: Flashcard) -> None:
        raise NotImplementedError


class SqlAlchemyFlashcardRepository(AbstractLocalFlashcardRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.seen: set[Flashcard] = set()

    def _create_flashcard(self, flashcard: Flashcard) -> None:
        self.session.add(flashcard)

    async def _retrieve_flashcard_by_word(self, word: str) -> Flashcard | None:
        try:
            result = await self.session.scalars(
                select(Flashcard).where(Flashcard.word == word),  # type: ignore[arg-type]
            )
        except OperationalError as ex:
            raise exceptions.DatabaseConnectionError from ex

        return result.first()

    async def _retrieve_all_flashcards(  # noqa: PLR0913
        self,
        regular_expression: str,
        with_definitions: bool,
        with_synonyms: bool,
        with_translations: bool,
        with_examples: bool,
        last_retrieved_word: str,
        limit: int,
    ) -> list[Flashcard]:
        try:
            results = await self.session.scalars(
                select(Flashcard)
                .filter(Flashcard.word.regexp_match(regular_expression))  # type: ignore[attr-defined]
                .where(Flashcard.word > last_retrieved_word)  # type: ignore[arg-type]
                .order_by(Flashcard.word)
                .limit(limit),
                params={
                    "with_definitions": with_definitions,
                    "with_synonyms": with_synonyms,
                    "with_translations": with_translations,
                    "with_examples": with_examples,
                },
            )
        except OperationalError as ex:
            raise exceptions.DatabaseConnectionError from ex

        return list(results)

    async def _delete_flashcard(self, flashcard: Flashcard) -> None:
        await self.session.delete(flashcard)
