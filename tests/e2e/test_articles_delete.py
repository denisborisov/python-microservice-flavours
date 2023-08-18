"""E2E tests related to DELETE articles API."""

import http
import uuid

from httpx import AsyncClient


class TestDeleteArticle:
    async def test_happy_path_returns_204(self, async_client: AsyncClient) -> None:
        article_1 = {
            "title": "First Title",
            "preview": "First Preview",
            "body": "First Body",
            "created_by": 1,
        }
        article_2 = {
            "title": "Second Title",
            "preview": "Second Preview",
            "body": "Second Body",
            "created_by": 2,
        }
        await async_client.post("/api/articles", json=article_1)
        response = await async_client.post("/api/articles", json=article_2)

        response = await async_client.delete(
            f"/api/articles/{response.json()['article_id']}",
        )
        assert response.status_code == http.HTTPStatus.NO_CONTENT

        response = await async_client.get("/api/articles")
        assert len(response.json()) == 1
        assert uuid.UUID(response.json()[0]["article_id"])
        assert response.json()[0]["title"] == article_1["title"]
        assert response.json()[0]["preview"] == article_1["preview"]
        assert response.json()[0]["body"] == article_1["body"]
        assert response.json()[0]["created_by"] == article_1["created_by"]

    async def test_cannot_delete_nonexistent_article(self, async_client: AsyncClient) -> None:
        await async_client.delete(f"/api/articles/{uuid.uuid4()}")

        response = await async_client.get("/api/articles")

        assert response.status_code == http.HTTPStatus.NOT_FOUND

    async def test_returns_400_if_bad_article_id(self, async_client: AsyncClient) -> None:
        article_id = uuid.uuid4()
        response = await async_client.delete(f"/api/articles/{article_id}")
        assert response.json()["detail"] == f"No such article with {article_id=}."
        assert response.status_code == http.HTTPStatus.NOT_FOUND
