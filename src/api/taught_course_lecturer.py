import datetime
from typing import Annotated
import uuid
from fastapi import APIRouter
from starlette import status
from fastapi import Path

from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from services.taught_course import TaughtCourseService
from datetime import datetime
from api.docs.taught_course_lecturer import (
    get_taught_course_by_speciality_course_responses,
    get_taught_courses_in_faculty_now_responses,
    get_taught_courses_responses,
)

taught_course_lecturer_router = APIRouter(
    prefix="/taught_course/lecturer",
    tags=["Taught Course: Lecturer"],
)


@taught_course_lecturer_router.get(
    path="/{faculty}/{year}",
    status_code=status.HTTP_200_OK,
    responses=get_taught_courses_responses,
)
async def get_taught_courses(
    faculty: str,
    year: Annotated[int, Path(ge=2000, le=datetime.now().year)],
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    taugth_course_service = TaughtCourseService()
    return await taugth_course_service.get_taught_courses_by_faculty(
        faculty_name=faculty,
        year=year,
        pagination=pagination,
        uow=uow,
    )


@taught_course_lecturer_router.get(
    path="/{speciality_course_id}",
    status_code=status.HTTP_200_OK,
    responses=get_taught_course_by_speciality_course_responses,
)
async def get_taught_course_by_speciality_course(
    speciality_course_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    taugth_course_service = TaughtCourseService()
    return await taugth_course_service.get_current_taught_course(
        speciality_course_id=speciality_course_id,
        uow=uow,
    )


@taught_course_lecturer_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=get_taught_courses_in_faculty_now_responses,
)
async def get_taught_courses_in_faculty_now(
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    taugth_course_service = TaughtCourseService()
    return await taugth_course_service.get_taught_courses_by_faculty(
        faculty_name=current_lecturer.faculty_name,
        year=datetime.now().year,
        pagination=pagination,
        uow=uow,
    )
