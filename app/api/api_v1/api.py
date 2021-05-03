from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    addresses,
    locations,
    organizations,
    requirements,
    vaccine_availability,
)

api_router = APIRouter()

api_router.include_router(
    vaccine_availability.router,
    prefix="/vaccine-availability",
    tags=["Vaccine Availability"],
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

api_router.include_router(
    requirements.router,
    prefix="/requirements",
    tags=["Requirements"],
)
