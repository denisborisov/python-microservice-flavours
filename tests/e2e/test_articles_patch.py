"""E2E tests related to PATCH articles API."""

import http
import uuid

from httpx import AsyncClient


class TestModifyArticle:
    async def test_happy_path_returns_200(self, async_client: AsyncClient) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}
        response = await async_client.post("/api/articles", json=article)

        article_modification = {
            "title": "Another Title",
            "preview": "Another Preview",
            "body": "Another Body",
        }

        response = await async_client.patch(
            f"/api/articles/{response.json()['article_id']}",
            json=article_modification,
        )

        assert response.status_code == http.HTTPStatus.OK

    async def test_cannot_modify_nonexistent_article (
        self,
        async_client: AsyncClient,
    ) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}
        response = await async_client.post("/api/articles", json=article)

        article_modification = {
            "title": "Another Title",
            "preview": "Another Preview",
            "body": "Another Body",
        }

        article_id = uuid.uuid4()
        response = await async_client.patch(
            f"/api/articles/{article_id}",
            json=article_modification,
        )

        assert response.status_code == http.HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == \
            f"Article with {article_id=} has not been found."

    async def test_cannot_modify_article_with_empty_title(
        self,
        async_client: AsyncClient,
    ) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}
        response = await async_client.post("/api/articles", json=article)

        article_modification = {"title": " "}

        response = await async_client.patch(
            f"/api/articles/{response.json()['article_id']}",
            json=article_modification,
        )

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json()["detail"].startswith("Failed to update article.")

    async def test_cannot_modify_article_with_empty_preview(
        self,
        async_client: AsyncClient,
    ) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}
        response = await async_client.post("/api/articles", json=article)

        article_modification = {"preview": " "}

        response = await async_client.patch(
            f"/api/articles/{response.json()['article_id']}",
            json=article_modification,
        )

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json()["detail"].startswith("Failed to update article.")

    async def test_cannot_modify_article_with_empty_body(
        self,
        async_client: AsyncClient,
    ) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}
        response = await async_client.post("/api/articles", json=article)

        article_modification = {"body": " "}

        response = await async_client.patch(
            f"/api/articles/{response.json()['article_id']}",
            json=article_modification,
        )

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json()["detail"].startswith("Failed to update article.")
