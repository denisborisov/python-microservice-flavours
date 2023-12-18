"""Unit tests related to model."""

import pytest
from src.domain import model


class ServiceClass:
    @staticmethod
    def create_aricle(
        flashcard_data: dict,
    ) -> model.Flashcard:
        return model.Flashcard(
            flashcard_data["word"],
            flashcard_data["definitions"],
            flashcard_data["synonyms"],
            flashcard_data["translations"],
            flashcard_data["examples"],
        )


class TestFlashcards:
    @pytest.mark.parametrize(
        ("first_flashcard", "second_flashcard", "equality", "cardinality"),
        [
            (
                {
                    "word": "SAME WORD",
                    "definitions": ["FIRST DEFINITION"],
                    "synonyms": ["FIRST SYNONYM"],
                    "translations": ["FIRST TRANSLATION"],
                    "examples": ["FIRST EXAMPLE"],
                },
                {
                    "word": "SAME WORD",
                    "definitions": ["SECOND DEFINITION"],
                    "synonyms": ["SECOND SYNONYM"],
                    "translations": ["SECOND TRANSLATION"],
                    "examples": ["SECOND EXAMPLE"],
                },
                True,
                1,
            ),
            (
                {
                    "word": "FIRST WORD",
                    "definitions": ["SAME DEFINITION"],
                    "synonyms": ["SAME SYNONYM"],
                    "translations": ["SAME TRANSLATION"],
                    "examples": ["SAME EXAMPLE"],
                },
                {
                    "word": "SECOND WORD",
                    "definitions": ["SAME DEFINITION"],
                    "synonyms": ["SAME SYNONYM"],
                    "translations": ["SAME TRANSLATION"],
                    "examples": ["SAME EXAMPLE"],
                },
                False,
                2,
            ),
        ],
    )
    def test_flashcard_identity_is_based_on_word(
        self,
        first_flashcard: dict,
        second_flashcard: dict,
        equality: bool,
        cardinality: int,
    ) -> None:
        flashcard_1 = ServiceClass.create_aricle(first_flashcard)

        flashcard_2 = ServiceClass.create_aricle(second_flashcard)

        assert (flashcard_1 == flashcard_2) is equality
        assert len({flashcard_1, flashcard_2}) == cardinality

    def test_flashcard_sorting_is_based_on_word(self) -> None:
        flashcard_1 = ServiceClass.create_aricle(
            {
                "word": "WORD A",
                "definitions": ["DEFINITION Z"],
                "synonyms": ["SYNONYM Z"],
                "translations": ["TRANSLATION Z"],
                "examples": ["EXAMPLE Z"],
            },
        )

        flashcard_2 = ServiceClass.create_aricle(
            {
                "word": "WORD Z",
                "definitions": ["DEFINITION A"],
                "synonyms": ["SYNONYM A"],
                "translations": ["TRANSLATION A"],
                "examples": ["EXAMPLE A"],
            },
        )

        flashcards = sorted([flashcard_1, flashcard_2])

        assert flashcards[0] == flashcard_1
        assert flashcards[1] == flashcard_2
