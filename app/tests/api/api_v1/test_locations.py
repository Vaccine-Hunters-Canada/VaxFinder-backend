import pytest
from httpx import AsyncClient

from app.tests.client.db_client import MSSQLClient
from app.tests.utils.locations_utils import LocationsDBHelper


@pytest.mark.asyncio
async def test_GivenNoLocations_WhenGettingLocations_ThenNothingReceived(
    db_client: MSSQLClient, app_client: AsyncClient
) -> None:
    locations_helper = LocationsDBHelper(db_client)

    response = await app_client.get("/api/v1/locations")

    assert response.status_code == 200

    content = response.json()
    assert content == []


@pytest.mark.asyncio
async def test_GivenOneLocation_WhenGettingLocations_ThenLocationReceived(
    db_client: MSSQLClient, app_client: AsyncClient
) -> None:
    locations_helper = LocationsDBHelper(db_client)

    await locations_helper.create_location("Location1", 1)

    response = await app_client.get("/api/v1/locations")

    assert response.status_code == 200

    content = response.json()
    assert not content == []
