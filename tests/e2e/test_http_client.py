"""Integration tests related to HTTP Client."""

import http

import httpx
import pytest

from src.services.http_client import HttpxClient


class TestHttpClient:
    async def test_happy_path_returns_200(self) -> None:
        async with HttpxClient() as httpx_client:
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
        url: str,
    ) -> None:
        with pytest.raises((httpx.HTTPStatusError, TypeError)):
            async with HttpxClient() as httpx_client:
                await httpx_client.get(url)
