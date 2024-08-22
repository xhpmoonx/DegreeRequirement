from fastapi import APIRouter, Depends, Body,HTTPException
from Db.database import get_db
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from Schema.schema import RequirementSet
from operation.RequirementSetOperation import Operation


router= APIRouter ()
@router.post("/requirement_set/validate/")
async def validate_requirement_set(db_session: Annotated[AsyncSession, Depends(get_db)] , data:RequirementSet = Body()):
    requirementSet = await Operation(db_session).create(data)
    return requirementSet
@router.post("/requirement_set/validate/is_valid")
async def validate_requirement_set(db_session: Annotated[AsyncSession, Depends(get_db)] , data:RequirementSet = Body()):
    operation = Operation(db_session)
    await operation.validate_requirement_set(data)
    return {"message": "Requirement set message available above"}