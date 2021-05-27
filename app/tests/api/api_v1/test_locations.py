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
    assert content["results"] == []
    assert content["total"] == 0


@pytest.mark.asyncio
async def test_GivenOneLocation_WhenGettingLocations_ThenLocationReceived(
    db_client: MSSQLClient, app_client: AsyncClient
) -> None:
    locations_helper = LocationsDBHelper(db_client)

    name = "Location1"
    active = 1
    phone = "6041112222"
    notes = "Accepting all V postal codes"
    postcode = "V6C1P7"
    url = "http://novaxhere.ca/"

    await locations_helper.create_location(
        name,
        active,
        phone=phone,
        notes=notes,
        postcode=postcode,
        url=url,
    )

    response = await app_client.get("/api/v1/locations")

    assert response.status_code == 200

    content = response.json()

    assert content["total"] == 1

    results = content["results"]
    assert len(results) == 1

    received_location = results[0]

    assert received_location["name"] == name
    assert received_location["active"] == active
    assert received_location["organization"] is None
    assert received_location["phone"] == phone
    assert received_location["notes"] == notes
    assert received_location["postcode"] == postcode
    assert received_location["url"] == url
    assert received_location["address"] is None
    assert received_location["tags"] is None
