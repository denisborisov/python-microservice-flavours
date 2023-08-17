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
        assert uuid.UUID(response.json()["article_id"])
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

        article_id = uuid.uuid4()
        response = await async_client.get(f"/api/articles/{article_id}")

        assert response.status_code == http.HTTPStatus.NOT_FOUND
        assert response.json() == \
            f"Article with {article_id=} has not been found."


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

        assert uuid.UUID(response.json()[0]["article_id"])
        assert response.json()[0]["title"] == article_1["title"]
        assert response.json()[0]["preview"] == article_1["preview"]
        assert response.json()[0]["body"] == article_1["body"]
        assert response.json()[0]["created_by"] == article_1["created_by"]

        assert uuid.UUID(response.json()[1]["article_id"])
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


class TestFetchAllArticlesOfOneUser:
    async def test_happy_path_returns_200_and_fetches_all_articles_of_user(
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
        article_3 = {
            "title": "Third Title",
            "preview": "Third Preview",
            "body": "Third Body",
            "created_by": 1,
        }
        await async_client.post("/api/articles", json=article_1)
        await async_client.post("/api/articles", json=article_2)
        await async_client.post("/api/articles", json=article_3)
        response = await async_client.get("/api/articles?created_by=1")

        assert response.status_code == http.HTTPStatus.OK

        assert uuid.UUID(response.json()[0]["article_id"])
        assert response.json()[0]["title"] == article_1["title"]
        assert response.json()[0]["preview"] == article_1["preview"]
        assert response.json()[0]["body"] == article_1["body"]
        assert response.json()[0]["created_by"] == article_1["created_by"]

        assert uuid.UUID(response.json()[1]["article_id"])
        assert response.json()[1]["title"] == article_3["title"]
        assert response.json()[1]["preview"] == article_3["preview"]
        assert response.json()[1]["body"] == article_3["body"]
        assert response.json()[1]["created_by"] == article_3["created_by"]

    async def test_cannot_fetch_articles_of_nonexistent_user(
        self,
        async_client: AsyncClient,
    ) -> None:
        article = {
            "title": "First Title",
            "preview": "First Preview",
            "body": "First Body",
            "created_by": 1,
        }
        await async_client.post("/api/articles", json=article)
        response = await async_client.get("/api/articles?created_by=2")

        assert response.status_code == http.HTTPStatus.NOT_FOUND
        assert response.json() == "There are no articles at all."


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
