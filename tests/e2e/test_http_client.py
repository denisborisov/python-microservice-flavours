"""Integration tests related to HTTP Client."""

import http
import pytest

import httpx

from src.services.http_client import AbstractHttpClient


class TestHttpClient:
    async def test_happy_path_returns_200(self, httpx_client: AbstractHttpClient) -> None:
        async with httpx_client:
            response: httpx.Response = await httpx_client.get("http://example.com")

            assert response.text
            assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.parametrize(
            "url",
            [
                ("http://www.example.com/lorem_ipsum"),
                (None),
            ],
        )
    async def test_unhappy_path_raises_exception(
        self,
        httpx_client: AbstractHttpClient,
        url: str,
    ) -> None:
        with pytest.raises((httpx.HTTPStatusError, TypeError)):
            async with httpx_client:
                await httpx_client.get(url)
