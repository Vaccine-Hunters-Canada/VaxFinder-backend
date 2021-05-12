import pytest
from fastapi.testclient import TestClient

from app.db.database import MSSQLBackend

OPENAPI_ENDPOINT = "/openapi.json"


@pytest.mark.asyncio
def test_openapi_health(
    app_client: TestClient, db_client: MSSQLBackend
) -> None:
    response = app_client.get(OPENAPI_ENDPOINT)

    assert response.status_code == 200
