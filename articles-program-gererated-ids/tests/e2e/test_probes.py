"""E2E tests related to probes."""

from fastapi import status
from httpx import AsyncClient


class TestProbes:
    async def test_check_startup(self, async_client: AsyncClient) -> None:
        response = await async_client.get("api/status/startup")

        assert response.status_code == status.HTTP_200_OK

    async def test_check_liveness(self, async_client: AsyncClient) -> None:
        response = await async_client.get("api/status/liveness")

        assert response.status_code == status.HTTP_200_OK

    async def test_check_readiness(self, async_client: AsyncClient) -> None:
        response = await async_client.get("api/status/readiness")

        assert response.status_code == status.HTTP_200_OK
