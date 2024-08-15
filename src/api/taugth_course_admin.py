from fastapi import APIRouter
from starlette import status
from dependencies.dependencies import (
    CurrentVerifiedSuperUserDep,
    UOWDep,
)
from schemas.taught_course import TaughtCourseCreate
from services.taught_course import TaughtCourseService
from api.docs.taught_course_admin import (
    add_taught_course_responses,
)

taught_course_admin_router = APIRouter(
    prefix="/taught_course/admin",
    tags=["Taught Course: Admin"],
)


@taught_course_admin_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=add_taught_course_responses,
)
async def add_taught_course(
    taught_course_create: TaughtCourseCreate,
    uow: UOWDep,
    current_superuser: CurrentVerifiedSuperUserDep,
):
    taugth_course_service = TaughtCourseService()

    await taugth_course_service.add_taught_course(
        taught_course_create=taught_course_create, uow=uow
    )
