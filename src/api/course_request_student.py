import uuid
from fastapi import APIRouter
from starlette import status

from dependencies import UOWDep
from dependencies.dependencies import CurrentStudentDep, PaginationDep
from schemas.course_request import CourseRequestBase, CourseRequestUpdate
from services.course_enrollment import CourseEnrollmentService
from api.docs import (
    get_pending_requests_response,
    send_course_request_responses,
    update_course_request_response,
)

course_request_student_router = APIRouter(
    prefix="/course_request",
    tags=["Course Request: Student"],
)


@course_request_student_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=send_course_request_responses,
)
async def send_course_request(
    request_create: CourseRequestBase,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    course_request_service = CourseEnrollmentService()
    await course_request_service.add_course_request(
        student_id=current_student.id,
        course_request_create=request_create,
        uow=uow,
    )


@course_request_student_router.get(
    path="/me",
    responses=get_pending_requests_response,
)
async def get_pending_requests(
    uow: UOWDep,
    pagination: PaginationDep,
    current_student: CurrentStudentDep,
):
    course_request_service = CourseEnrollmentService()
    return await course_request_service.get_all_course_requests_for_student(
        student_id=current_student.id,
        pagination=pagination,
        uow=uow,
    )


@course_request_student_router.patch(
    path="/{course_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses=update_course_request_response,
)
async def update_course_request(
    request_update: CourseRequestUpdate,
    course_id: uuid.UUID,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    course_request_service = CourseEnrollmentService()
    await course_request_service.edit_course_request(
        course_id=course_id,
        student_id=current_student.id,
        course_request_update=request_update,
        uow=uow,
    )
