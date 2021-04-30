from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    addresses,
    entries,
    locations,
    organizations,
)

api_router = APIRouter()

api_router.include_router(
    entries.router,
    prefix="/entries",
    tags=["Entries"],
)

api_router.include_router(
    locations.router,
    prefix="/locations",
    tags=["Locations"],
)

api_router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["Organizations"],
)

api_router.include_router(
    addresses.router,
    prefix="/addresses",
    tags=["Addresses"],
)
