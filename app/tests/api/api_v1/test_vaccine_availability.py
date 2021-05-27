import pytest
from httpx import AsyncClient

from app.tests.client.db_client import MSSQLClient


@pytest.mark.asyncio
async def test_Given_NoPostalCode_WhenGettingAvailabilities_Then422(
    app_client: AsyncClient, db_client: MSSQLClient
) -> None:
    response = await app_client.get("/api/v1/vaccine-availability")

    assert response.status_code == 422
