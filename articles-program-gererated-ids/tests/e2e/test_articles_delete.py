"""E2E tests related to DELETE articles API."""

import http
import uuid

from httpx import AsyncClient

from .conftest import ServiceClass


class TestDeleteArticle:
    async def test_happy_path_returns_204(self, async_client: AsyncClient) -> None:
        json_create_responses = await ServiceClass.create_articles(
            async_client,
            {
                "title": "FIRST TITLE",
                "preview": "FIRST PREVIEW",
                "body": "FIRST BODY",
                "created_by": 1,
            },
            {
                "title": "SECOND TITLE",
                "preview": "SECOND PREVIEW",
                "body": "SECOND BODY",
                "created_by": 2,
            },
        )

        delete_response, fetchall_response = await ServiceClass.delete_article_and_fetch_all(
            async_client,
            json_create_responses[1]["article_id"],
        )

        assert delete_response.status_code == http.HTTPStatus.NO_CONTENT
        assert len(fetchall_response.json()) == 1
        assert fetchall_response.json()[0] == {
            "article_id": json_create_responses[0]["article_id"],
            "title": "FIRST TITLE",
            "preview": "FIRST PREVIEW",
            "body": "FIRST BODY",
            "created_by": 1,
            "events": [],
        }

    async def test_cannot_delete_nonexistent_article(self, async_client: AsyncClient) -> None:
        response = await async_client.delete(f"/api/articles/{uuid.uuid4()}")

        assert response.status_code == http.HTTPStatus.NOT_FOUND

    async def test_returns_400_if_bad_article_id(self, async_client: AsyncClient) -> None:
        article_id = uuid.uuid4()

        response = await async_client.delete(f"/api/articles/{article_id}")

        assert response.json()["detail"] == f"No such article with {article_id=}."
        assert response.status_code == http.HTTPStatus.NOT_FOUND
