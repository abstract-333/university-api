from datetime import datetime
from typing import Annotated
from fastapi import APIRouter
from starlette import status
from fastapi import Path

from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from services.taught_course import TaughtCourseService
from api.docs.taught_coures_student import get_taught_courses_for_me_responses

taught_course_student_router = APIRouter(
    prefix="/taught_course/student",
    tags=["Taught Course: Student"],
)


@taught_course_student_router.get(
    path="/{semester}/{year}",
    status_code=status.HTTP_200_OK,
    responses=get_taught_courses_for_me_responses,
)
async def get_taught_courses_for_my_speciality(
    semester: Annotated[int, Path(le=2, ge=1)],
    year: Annotated[int, Path(le=datetime.now().year, ge=2020)],
    pagination: PaginationDep,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    taugth_course_service = TaughtCourseService()
    return await taugth_course_service.get_taught_courses_by_speciality(
        speciality_id=current_student.speciality.id,
        current_class=current_student.class_id,
        semester=semester,
        year=year,
        pagination=pagination,
        uow=uow,
    )
