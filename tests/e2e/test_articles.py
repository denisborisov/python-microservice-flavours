"""E2E tests related to articles."""

import http
import pytest
import uuid

from httpx import AsyncClient


class TestCreateArticle:
    async def test_happy_path_returns_201(self, async_client: AsyncClient) -> None:
        article = {"title": "Title", "preview": "Preview", "body": "Body", "created_by": 1}
        response = await async_client.post("/api/articles", json=article)

        assert response.status_code == http.HTTPStatus.CREATED
        assert response.json()

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
        assert response.json().startswith("Failed to create article.")

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
        assert response.json().startswith("Failed to create article.")

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
        assert response.json().startswith("Failed to create article.")


class TestFetchArticleById:
    async def test_happy_path_returns_200_and_fetches_article_by_id(
        self,
        async_client: AsyncClient,
    ) -> None:
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
        post_response = await async_client.post("/api/articles", json=article_2)

        response = await async_client.get(f"/api/articles/{post_response.json()['article_id']}")

        assert response.status_code == http.HTTPStatus.OK
        assert response.json()["title"] == article_2["title"]
        assert response.json()["preview"] == article_2["preview"]
        assert response.json()["body"] == article_2["body"]
        assert response.json()["created_by"] == article_2["created_by"]

    async def test_cannot_return_nonexistent_article(self, async_client: AsyncClient) -> None:
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
        await async_client.post("/api/articles", json=article_2)

        nonexistent_article_id = uuid.uuid4()
        response = await async_client.get(f"/api/articles/{nonexistent_article_id!s}")

        assert response.status_code == http.HTTPStatus.NOT_FOUND
        assert response.json() == \
            f"Article with article_id='{nonexistent_article_id!s}' has not been found."


class TestFetchAllArticles:
    async def test_happy_path_returns_200_and_fetches_all_articles(
        self,
        async_client: AsyncClient,
    ) -> None:
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
        await async_client.post("/api/articles", json=article_2)
        response = await async_client.get("/api/articles")

        assert response.status_code == http.HTTPStatus.OK

        assert response.json()[0]["title"] == article_1["title"]
        assert response.json()[0]["preview"] == article_1["preview"]
        assert response.json()[0]["body"] == article_1["body"]
        assert response.json()[0]["created_by"] == article_1["created_by"]

        assert response.json()[1]["title"] == article_2["title"]
        assert response.json()[1]["preview"] == article_2["preview"]
        assert response.json()[1]["body"] == article_2["body"]
        assert response.json()[1]["created_by"] == article_2["created_by"]

    async def test_cannot_fetch_articles_from_empty_repository(
        self,
        async_client: AsyncClient,
    ) -> None:
        response = await async_client.get("/api/articles")
        assert response.status_code == http.HTTPStatus.NOT_FOUND
        assert response.json() == "There are no articles at all."
