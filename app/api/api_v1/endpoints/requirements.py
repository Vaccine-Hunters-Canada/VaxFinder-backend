from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.requirements import RequirementResponse
from app.services.requirements import RequirementService

router = APIRouter()


@router.get(
    "", response_model=List[RequirementResponse]
)
async def list_requirements(
    db: MSSQLConnection = Depends(get_db)
) -> List[RequirementResponse]:
    return await RequirementService(db).get_all()


@router.get(
    "/{requirement_id}",
    response_model=RequirementResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The requirement with the specified id could not be found."
        }
    },
)
async def retrieve_requirement_by_id(
    requirement_id: int,
    db: MSSQLConnection = Depends(get_db)
) -> RequirementResponse:
    requirement = await RequirementService(db).get_by_id(requirement_id)

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return requirement
