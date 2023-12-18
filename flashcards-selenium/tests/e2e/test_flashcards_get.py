"""E2E tests related to GET flashcards API."""

import http

from httpx import AsyncClient

from .conftest import ServiceClass


class TestFetchFlashcardById:
    async def test_happy_path_returns_200_and_fetches_flashcard_by_word(
        self,
        async_client: AsyncClient,
    ) -> None:
        flashcards = await ServiceClass.create_flashcards_in_local_repo(
            async_client,
            {"prefix": "FIRST_"},
            {"prefix": "SECOND_"},
        )

        fetch_one_response = await async_client.get(
            f"/api/flashcards/{flashcards[1].word}",
        )

        assert fetch_one_response.status_code == http.HTTPStatus.OK
        assert fetch_one_response.json() == {
            "word": "SECOND_WORD",
            "definitions": ["SECOND_DEFINITION"],
            "synonyms": ["SECOND_SYNONYM"],
            "translations": ["SECOND_TRANSLATION"],
            "examples": ["SECOND_EXAMPLE"],
        }

    async def test_cannot_return_nonexistent_flashcard(self, async_client: AsyncClient) -> None:
        word = "NO_SUCH_WORD"

        fetch_one_response = await async_client.get(f"/api/flashcards/{word}")

        assert fetch_one_response.status_code == http.HTTPStatus.NOT_FOUND
        assert fetch_one_response.json() == f"Flashcard for {word=} has not been found."


class TestFetchAllFlashcards:
    async def test_happy_path_returns_200_and_fetches_all_flashcards(
        self,
        async_client: AsyncClient,
    ) -> None:
        await ServiceClass.create_flashcards_in_local_repo(
            async_client,
            {"prefix": "FIRST_"},
            {"prefix": "SECOND_"},
        )

        fetch_all_response = await async_client.get(
            "/api/flashcards",
            params={
                "regular_expression": ".",
                "with_definitions": True,
                "with_synonyms": True,
                "with_translations": True,
                "with_examples": True,
                "last_retrieved_word": "",
                "limit": 100,
            },
        )

        assert fetch_all_response.status_code == http.HTTPStatus.OK

        assert fetch_all_response.json()[0] == {
            "word": "FIRST_WORD",
            "definitions": ["FIRST_DEFINITION"],
            "synonyms": ["FIRST_SYNONYM"],
            "translations": ["FIRST_TRANSLATION"],
            "examples": ["FIRST_EXAMPLE"],
        }

        assert fetch_all_response.json()[1] == {
            "word": "SECOND_WORD",
            "definitions": ["SECOND_DEFINITION"],
            "synonyms": ["SECOND_SYNONYM"],
            "translations": ["SECOND_TRANSLATION"],
            "examples": ["SECOND_EXAMPLE"],
        }

    async def test_happy_path_returns_200_and_fetches_only_words_by_default(
        self,
        async_client: AsyncClient,
    ) -> None:
        await ServiceClass.create_flashcards_in_local_repo(
            async_client,
            {"prefix": "FIRST_"},
            {"prefix": "SECOND_"},
        )

        fetch_all_response = await async_client.get("/api/flashcards")

        assert fetch_all_response.status_code == http.HTTPStatus.OK

        assert fetch_all_response.json()[0] == {
            "word": "FIRST_WORD",
        }

        assert fetch_all_response.json()[1] == {
            "word": "SECOND_WORD",
        }

    async def test_cannot_fetch_flashcards_from_empty_repository(
        self,
        async_client: AsyncClient,
    ) -> None:
        response = await async_client.get("/api/flashcards")

        assert response.status_code == http.HTTPStatus.NOT_FOUND
        assert response.json() == "There are no flashcards at all."
