"""E2E tests related to GET articles API."""

import http
import uuid

from httpx import AsyncClient

from .conftest import ServiceClass


class TestFetchArticleById:
    async def test_happy_path_returns_200_and_fetches_article_by_id(
        self,
        async_client: AsyncClient,
    ) -> None:
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

        fetch_one_response = await async_client.get(
            f"/api/articles/{json_create_responses[1]['article_id']}",
        )

        assert fetch_one_response.status_code == http.HTTPStatus.OK
        assert fetch_one_response.json() == {
            "article_id": json_create_responses[1]["article_id"],
            "title": "SECOND TITLE",
            "preview": "SECOND PREVIEW",
            "body": "SECOND BODY",
            "created_by": 2,
            "events": [],
        }

    async def test_cannot_return_nonexistent_article(self, async_client: AsyncClient) -> None:
        article_id = uuid.uuid4()

        fetch_one_response = await async_client.get(f"/api/articles/{article_id}")

        assert fetch_one_response.status_code == http.HTTPStatus.NOT_FOUND
        assert fetch_one_response.json() == f"Article with {article_id=} has not been found."


class TestFetchAllArticles:
    async def test_happy_path_returns_200_and_fetches_all_articles(
        self,
        async_client: AsyncClient,
    ) -> None:
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

        fetch_all_response = await async_client.get("/api/articles")

        assert fetch_all_response.status_code == http.HTTPStatus.OK

        assert fetch_all_response.json()[0] == {
            "article_id": json_create_responses[0]["article_id"],
            "title": "FIRST TITLE",
            "preview": "FIRST PREVIEW",
            "body": "FIRST BODY",
            "created_by": 1,
            "events": [],
        }

        assert fetch_all_response.json()[1] == {
            "article_id": json_create_responses[1]["article_id"],
            "title": "SECOND TITLE",
            "preview": "SECOND PREVIEW",
            "body": "SECOND BODY",
            "created_by": 2,
            "events": [],
        }

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
            {
                "title": "THIRD TITLE",
                "preview": "THIRD PREVIEW",
                "body": "THIRD BODY",
                "created_by": 1,
            },
        )

        fetch_all_or_one_user_response = await async_client.get("/api/articles?created_by=1")

        assert fetch_all_or_one_user_response.status_code == http.HTTPStatus.OK

        assert fetch_all_or_one_user_response.json()[0] == {
            "article_id": json_create_responses[0]["article_id"],
            "title": "FIRST TITLE",
            "preview": "FIRST PREVIEW",
            "body": "FIRST BODY",
            "created_by": 1,
            "events": [],
        }

        assert fetch_all_or_one_user_response.json()[1] == {
            "article_id": json_create_responses[2]["article_id"],
            "title": "THIRD TITLE",
            "preview": "THIRD PREVIEW",
            "body": "THIRD BODY",
            "created_by": 1,
            "events": [],
        }

    async def test_cannot_fetch_articles_of_nonexistent_user(
        self,
        async_client: AsyncClient,
    ) -> None:
        await ServiceClass.create_articles(
            async_client,
            {
                "title": "TITLE",
                "preview": "PREVIEW",
                "body": "BODY",
                "created_by": 1,
            },
        )

        fetch_all_or_one_user_response = await async_client.get("/api/articles?created_by=2")

        assert fetch_all_or_one_user_response.status_code == http.HTTPStatus.NOT_FOUND
        assert fetch_all_or_one_user_response.json() == "There are no articles at all."
