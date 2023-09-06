"""E2E tests related to POST articles API."""

import http
import uuid

import pytest
from httpx import AsyncClient


class TestCreateArticle:
    async def test_happy_path_returns_201(self, async_client: AsyncClient) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}

        response = await async_client.post("/api/articles", json=article)

        assert response.status_code == http.HTTPStatus.CREATED
        assert uuid.UUID(response.json()["article_id"])

    @pytest.mark.parametrize(
        ("title", "preview", "body", "created_by"),
        [
            (" ", "Preview", "Body", 1),
            ("", "Preview", "Body", 1),
        ],
    )
    async def test_cannot_create_article_with_empty_title(  # noqa: PLR0913
        self,
        async_client: AsyncClient,
        title: str,
        preview: str,
        body: str,
        created_by: int,
    ) -> None:
        article = {"title": title, "preview": preview, "body": body, "created_by": created_by}

        response = await async_client.post("/api/articles", json=article)

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json()["detail"].startswith("Failed to create article.")

    @pytest.mark.parametrize(
        ("title", "preview", "body", "created_by"),
        [
            ("Title", " ", "Body", 1),
            ("Title", "", "Body", 1),
        ],
    )
    async def test_cannot_create_article_with_empty_preview(  # noqa: PLR0913
        self,
        async_client: AsyncClient,
        title: str,
        preview: str,
        body: str,
        created_by: int,
    ) -> None:
        article = {"title": title, "preview": preview, "body": body, "created_by": created_by}

        response = await async_client.post("/api/articles", json=article)

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json()["detail"].startswith("Failed to create article.")

    @pytest.mark.parametrize(
        ("title", "preview", "body", "created_by"),
        [
            ("Title", "Preview", " ", 1),
            ("Title", "Preview", "", 1),
        ],
    )
    async def test_cannot_create_article_with_empty_body(  # noqa: PLR0913
        self,
        async_client: AsyncClient,
        title: str,
        preview: str,
        body: str,
        created_by: int,
    ) -> None:
        article = {"title": title, "preview": preview, "body": body, "created_by": created_by}

        response = await async_client.post("/api/articles", json=article)

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json()["detail"].startswith("Failed to create article.")
