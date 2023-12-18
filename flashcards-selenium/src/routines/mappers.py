"""Routines related to mappers."""

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.asyncio import AsyncSession

from ..adapters import orm
from ..domain import model

mapper_registry = sqlalchemy.orm.registry()


def start_mappers() -> None:
    mapper_registry.map_imperatively(
        model.Flashcard,
        orm.Flashcard.__table__,
    )


def stop_mappers() -> None:
    mapper_registry.dispose()


@sqlalchemy.event.listens_for(model.Flashcard, "load", restore_load_context=True)
def receive_load(flashcard: model.Flashcard, qc: sqlalchemy.orm.QueryContext) -> None:
    if qc.params.get("with_definitions", True):
        flashcard.definitions = flashcard.details["definitions"]  # type: ignore[attr-defined]
    if qc.params.get("with_synonyms", True):
        flashcard.synonyms = flashcard.details["synonyms"]  # type: ignore[attr-defined]
    if qc.params.get("with_translations", True):
        flashcard.translations = flashcard.details["translations"]  # type: ignore[attr-defined]
    if qc.params.get("with_examples", True):
        flashcard.examples = flashcard.details["examples"]  # type: ignore[attr-defined]
    del flashcard.details  # type: ignore[attr-defined]
    flashcard.events = []


@sqlalchemy.event.listens_for(sqlalchemy.orm.Session, "before_flush")
def receive_before_flush(
    session: AsyncSession,
    flush_context: sqlalchemy.orm.UOWTransaction,  # noqa: ARG001
    instances: sqlalchemy.Sequence | None,  # noqa: ARG001
) -> None:
    flashcards: list[model.Flashcard] = []
    flashcards.extend(session.new)
    flashcards.extend(session.dirty)
    flashcards.extend(session.deleted)

    for flashcard in flashcards:
        setattr(
            flashcard,
            "details",
            {
                "definitions": flashcard.definitions,
                "synonyms": flashcard.synonyms,
                "translations": flashcard.translations,
                "examples": flashcard.examples,
            },
        )
