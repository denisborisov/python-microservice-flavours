"""Unit tests related to commands."""

import pytest
from src.domain.events import FlashcardFetchedFromGoogleApi
from src.domain.exceptions import FlashcardCreationError
from src.domain.model import Flashcard


class TestFlashcardFetchedFromGoogleApiEvent:
    def test_cannot_create_with_empty_word(self) -> None:
        flashcard_with_empty_word = Flashcard(
            word=" ",
            definitions=["SOME DEFINITION"],
            synonyms=["SOME SYNONYM"],
            translations=["SOME TRANSLATION"],
            examples=["SOME example"],
        )

        with pytest.raises(FlashcardCreationError) as exc_info:
            FlashcardFetchedFromGoogleApi(flashcard_with_empty_word)

        assert exc_info.value.args[0] == "Cannot create an flashcard for an empty word."

    def test_strips_word(self) -> None:
        flashcard_with_word_empraced_with_spaces = Flashcard(
            word=" SOME WORD ",
            definitions=["SOME DEFINITION"],
            synonyms=["SOME SYNONYM"],
            translations=["SOME TRANSLATION"],
            examples=["SOME example"],
        )

        event = FlashcardFetchedFromGoogleApi(flashcard_with_word_empraced_with_spaces)

        assert event.flashcard.word == "SOME WORD"
