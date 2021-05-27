from datetime import date, datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from loguru import logger

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.vaccine_availability import VaccineLocationExpandedResponse
from app.services.exceptions import (
    DatabaseNotInSyncError,
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.vaccine_availability import VaccineAvailabilityService
from app.services.vaccine_availability_locations import VaccineLocationsService

router = APIRouter()


@router.get("", response_model=List[VaccineLocationExpandedResponse])
async def list_vaccine_locations(
    min_date: Optional[date] = Query(
        date.today(),
        title="Minimum Date",
        description="**Search for vaccine availabilities after a certain date "
        "and time (UTC) in the format YYYY-MM-DD**. The default value is the current date ("
        "UTC).<br/><br/>Valid example(s): *2021-05-30*",
    ),
    postal_code: str = Query(
        ...,
        title="Postal Code",
        description="**Search for vaccine availabilities within the vicinity "
        "of a postal code. (First 3 characters ONLY)**"
        "<br/><br/>Valid example(s): *K1A; M5V;* ",
        min_length=3,
        max_length=3,
    ),
    include_empty: bool = Query(
        False,
        title="Include Empty",
        description="**Include Vaccine Availabilities "
        "with no remaining vaccines**"
        "<br/><br/>Valid example(s): *true; false;* ",
    ),
    db: MSSQLConnection = Depends(get_db),
) -> List[VaccineLocationExpandedResponse]:
    """
    **Retrieves the list of vaccine availabilities within the vicinity of a
    `postal_code` and after the `min_date`.**
    """
    # Done here so the OpenAPI spec doesn't show the wrong default value
    if min_date is None:
        min_date = datetime.today().date()
    try:
        availabilities = await VaccineLocationsService(
            db
        ).get_filtered_multi_expanded(
            postal_code=postal_code,
            min_date=min_date,
            include_empty=include_empty,
        )
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    except DatabaseNotInSyncError as e:
        logger.warning("Database not in sync: {}", e.message)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return availabilities
