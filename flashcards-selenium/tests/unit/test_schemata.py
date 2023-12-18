"""Unit tests related to schemata."""

from src.domain import schemata


class TestFlashcard:
    def test_can_create_flashcard(self) -> None:
        flashcard = schemata.Flashcard(
            word="WORD",
            definitions=["FIRST DEFINITION", "SECOND DEFINITION"],
            synonyms=["FIRST SYNONYM", "SECOND SYNONYM"],
            translations=["FIRST TRANSLATION", "SECOND TRANSLATION"],
            examples=["FIRST EXAMPLE", "SECOND EXAMPLE"],
        )

        assert flashcard.word == "WORD"
        assert flashcard.definitions == ["FIRST DEFINITION", "SECOND DEFINITION"]
        assert flashcard.synonyms == ["FIRST SYNONYM", "SECOND SYNONYM"]
        assert flashcard.translations == ["FIRST TRANSLATION", "SECOND TRANSLATION"]
        assert flashcard.examples == ["FIRST EXAMPLE", "SECOND EXAMPLE"]

    def test_flashcard_contains_valid_config(self) -> None:
        example = schemata.Flashcard.model_config["json_schema_extra"]["examples"][0]

        assert example["word"] == "challenge"
        assert example["definitions"] == [
            "a call to take part in a contest or competition, especially a duel.",
            "an objection or query as to the truth of something, often with "
            "an implicit demand for proof.",
        ]
        assert example["synonyms"] == ["dare", "provocation"]
        assert example["translations"] == ["испытание", "вызов"]
        assert example["examples"] == [
            "recently vaccinated calves should be protected from challenge",
        ]
