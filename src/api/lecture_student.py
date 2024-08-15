from uuid import UUID
from fastapi import APIRouter
from starlette import status

from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from services.lecture import LectureService
from api.docs.lecture_student import get_lectures_responses

lecture_student_router = APIRouter(
    prefix="/lecture/student",
    tags=["Lecture: Student"],
)


@lecture_student_router.get(
    path="/{enrolled_course_id}",
    status_code=status.HTTP_200_OK,
    responses=get_lectures_responses,
)
async def get_my_lectures_for_course(
    enrolled_course_id: UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_student: CurrentStudentDep,
):
    lecture_service = LectureService()
    return await lecture_service.get_lectures_for_student(
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        pagination=pagination,
        uow=uow,
    )
