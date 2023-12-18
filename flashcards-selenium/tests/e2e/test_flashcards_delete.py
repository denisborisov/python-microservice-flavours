"""E2E tests related to DELETE flashcards API."""

import http

from httpx import AsyncClient

from .conftest import ServiceClass


class TestDeleteFlashcard:
    async def test_happy_path_returns_204(self, async_client: AsyncClient) -> None:
        flashcards = await ServiceClass.create_flashcards_in_local_repo(
            async_client,
            {"word": "FIRST"},
            {"word": "SECOND"},
        )

        delete_response, fetchall_response = await ServiceClass.delete_flashcard_and_fetch_all(
            async_client,
            flashcards[1].word,
        )

        assert delete_response.status_code == http.HTTPStatus.NO_CONTENT
        assert len(fetchall_response.json()) == 1
        assert fetchall_response.json()[0] == {
            "word": "FIRST",
            "definitions": ["DEFINITION"],
            "synonyms": ["SYNONYM"],
            "translations": ["TRANSLATION"],
            "examples": ["EXAMPLE"],
        }

    async def test_cannot_delete_nonexistent_flashcard(self, async_client: AsyncClient) -> None:
        response = await async_client.delete("/api/flashcards/WORD")

        assert response.status_code == http.HTTPStatus.NOT_FOUND

    async def test_returns_400_if_bad_flashcard_id(self, async_client: AsyncClient) -> None:
        word = "WORD"

        response = await async_client.delete(f"/api/flashcards/{word}")

        assert response.json()["detail"] == f"No such flashcard for {word=}."
        assert response.status_code == http.HTTPStatus.NOT_FOUND
