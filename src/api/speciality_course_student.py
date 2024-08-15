from typing import Annotated
from fastapi import APIRouter, Path
from starlette import status

from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from services.speciality_course import SpecialityCourseService
from api.docs.speicality_course_student import (
    get_speciality_courses_for_my_speciality_responses,
)

speciality_course_student_router = APIRouter(
    prefix="/speciality_course/student",
    tags=["Speciality Course: Student"],
)


@speciality_course_student_router.get(
    path="/{semester}",
    status_code=status.HTTP_200_OK,
    responses=get_speciality_courses_for_my_speciality_responses,
)
async def get_speciality_courses_for_me(
    semester: Annotated[int, Path(le=2, ge=1)],
    pagination: PaginationDep,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    speciality_course_service = SpecialityCourseService()
    return await speciality_course_service.get_speciality_courses_by_speciality(
        speciality_id=current_student.speciality.id,
        current_class=current_student.class_id,
        semester=semester,
        pagination=pagination,
        uow=uow,
    )
