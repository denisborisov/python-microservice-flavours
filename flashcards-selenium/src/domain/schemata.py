"""Schemata for CRUD operations."""

import typing

from pydantic import BaseModel


class Flashcard(BaseModel):
    word: str
    definitions: list[str] | None
    synonyms: list[str] | None
    translations: list[str] | None
    examples: list[str] | None

    model_config: typing.ClassVar = {
        "json_schema_extra": {
            "examples": [
                {
                    "word": "challenge",
                    "definitions": [
                        "a call to take part in a contest or competition, especially a duel.",
                        "an objection or query as to the truth of something, often with "
                        "an implicit demand for proof.",
                    ],
                    "synonyms": ["dare", "provocation"],
                    "translations": ["испытание", "вызов"],
                    "examples": [
                        "recently vaccinated calves should be protected from challenge",
                    ],
                },
            ],
        },
    }
