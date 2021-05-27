import pytest
from httpx import AsyncClient

from app.tests.client.db_client import MSSQLClient

OPENAPI_ENDPOINT = "/openapi.json"


@pytest.mark.asyncio
async def test_WhenRequestingOpenApi_ThenNoProblem(
    app_client: AsyncClient, db_client: MSSQLClient
) -> None:
    response = await app_client.get(OPENAPI_ENDPOINT)

    assert response.status_code == 200
