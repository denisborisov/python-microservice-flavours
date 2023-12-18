"""E2E tests related to PATCH articles API."""

import http
import uuid

import pytest
from httpx import AsyncClient

from .conftest import ServiceClass


class TestModifyArticle:
    async def test_happy_path_returns_200(self, async_client: AsyncClient) -> None:
        json_create_responses = await ServiceClass.create_articles(
            async_client,
            {
                "title": "TITLE",
                "preview": "PREVIEW",
                "body": "BODY",
                "created_by": 1,
            },
        )

        update_response = await ServiceClass.update_article(
            async_client,
            {
                "article_id": json_create_responses[0]["article_id"],
                "title": "ANOTHER TITLE",
                "preview": "ANOTHER PREVIEW",
                "body": "ANOTHER BODY",
            },
        )

        assert update_response.status_code == http.HTTPStatus.OK

    async def test_cannot_modify_nonexistent_article(
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

        article_id = uuid.uuid4()
        update_response = await ServiceClass.update_article(
            async_client,
            {
                "article_id": str(article_id),
                "title": "ANOTHER TITLE",
                "preview": "ANOTHER PREVIEW",
                "body": "ANOTHER BODY",
            },
        )

        assert update_response.status_code == http.HTTPStatus.NOT_FOUND
        assert (
            update_response.json()["detail"] == f"Article with {article_id=} has not been found."
        )

    @pytest.mark.parametrize(
        ("field"),
        [
            ("title"),
            ("preview"),
            ("body"),
        ],
    )
    async def test_cannot_modify_article_with_empty_fields(
        self,
        field: str,
        async_client: AsyncClient,
    ) -> None:
        json_create_responses = await ServiceClass.create_articles(
            async_client,
            {
                "title": "TITLE",
                "preview": "PREVIEW",
                "body": "BODY",
                "created_by": 1,
            },
        )

        update_response = await ServiceClass.update_article(
            async_client,
            {
                "article_id": json_create_responses[0]["article_id"],
                field: " ",
            },
        )

        assert update_response.status_code == http.HTTPStatus.BAD_REQUEST
        assert update_response.json()["detail"].startswith("Failed to update article.")
