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
from services.speciality_course import SpecialityCourseService
from api.docs.speciality_course_lecturer import (
    get_speciality_courses_by_speciality_id_responses,
    get_speciality_courses_for_my_faculty_responses,
)

speciality_course_lecturer_router = APIRouter(
    prefix="/speciality_course/lecturer",
    tags=["Speciality Course: Lecturer"],
)


@speciality_course_lecturer_router.get(
    path="/{current_class}/{semester}",
    status_code=status.HTTP_200_OK,
    responses=get_speciality_courses_for_my_faculty_responses,
)
async def get_speciality_courses_for_my_faculty(
    semester: Annotated[int, Path(le=2, ge=1)],
    current_class: Annotated[int, Path(le=6, ge=1)],
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    speciality_course_service = SpecialityCourseService()
    return await speciality_course_service.get_speciality_courses_by_faculty(
        faculty_name=current_lecturer.faculty_name,
        current_class=current_class,
        semester=semester,
        pagination=pagination,
        uow=uow,
    )


@speciality_course_lecturer_router.get(
    path="/{speciality_id}",
    status_code=status.HTTP_200_OK,
    responses=get_speciality_courses_by_speciality_id_responses,
)
async def get_speciality_courses_by_speciality_id(
    speciality_id: uuid.UUID,
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    speciality_course_service = SpecialityCourseService()
    return (
        await speciality_course_service.get_speciality_courses_by_specific_speciality(
            speciality_id=speciality_id,
            uow=uow,
            pagination=pagination,
        )
    )
