from fastapi import APIRouter

from dependencies import UOWDep
from dependencies.dependencies import CurrentStudentDep, PaginationDep
from services.course_enrollment import CourseEnrollmentService
from api.docs import get_enrolled_courses_response

enrolled_course_student_router = APIRouter(
    prefix="/enrolled_course",
    tags=["Enrolled Course: Student"],
)


@enrolled_course_student_router.get(
    path="/me",
    responses=get_enrolled_courses_response,
)
async def get_enrolled_courses(
    uow: UOWDep,
    current_student: CurrentStudentDep,
    pagination: PaginationDep,
):
    course_request_service = CourseEnrollmentService()
    return await course_request_service.get_enrolled_courses(
        student_id=current_student.id,
        uow=uow,
        pagination=pagination,
    )
