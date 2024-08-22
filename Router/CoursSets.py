from fastapi import APIRouter, Depends, Body,HTTPException
from Db.database import get_db
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from Schema.schema import CourseSet
from operation.CourseSetOperation import Operation


router= APIRouter ()
@router.post("/course_set/validate/")
async def validate_course_set(db_session: Annotated[AsyncSession, Depends(get_db)] , data:CourseSet = Body()):
    courseSet = await Operation(db_session).create(data)
    return courseSet
