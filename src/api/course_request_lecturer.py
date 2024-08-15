import uuid

from fastapi import APIRouter, BackgroundTasks
from starlette import status

from api.docs import (
    accept_all_freshman_requests_response,
    get_pending_requests_responses,
    accept_reject_request_response,
)
from dependencies import UOWDep
from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
)
from services.course_enrollment import CourseEnrollmentService

course_request_lecturer_router = APIRouter(
    prefix="/course_request",
    tags=["Course Request: Lecturer"],
)


@course_request_lecturer_router.get(
    path="/{course_id}",
    responses=get_pending_requests_responses,
)
async def get_pending_requests(
    course_id: uuid.UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_lecturer: CurrentLecturerDep,
):
    course_request_service = CourseEnrollmentService()
    return await course_request_service.get_all_course_requests_for_course(
        course_id=course_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@course_request_lecturer_router.post(
    path="/{course_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses=accept_all_freshman_requests_response,
)
async def accept_freshman_requests(
    course_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
    background_tasks: BackgroundTasks,
):
    course_request_service = CourseEnrollmentService()
    background_tasks.add_task(
        course_request_service.accept_course_requests_freshman,
        course_id=course_id,
        lecturer_id=current_lecturer.id,
        lecturer_user_id=current_lecturer.user_id,
        uow=uow,
        pagination=pagination,
    )
    return None


@course_request_lecturer_router.post(
    path="/{course_id}/{request_id}/{student_id}/accept",
    status_code=status.HTTP_202_ACCEPTED,
    responses=accept_reject_request_response,
)
async def accept_course_request(
    course_id: uuid.UUID,
    request_id: uuid.UUID,
    student_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    course_request_service = CourseEnrollmentService()
    await course_request_service.accept_course_request(
        course_id=course_id,
        course_request_id=request_id,
        student_id=student_id,
        lecturer_id=current_lecturer.id,
        lecturer_user_id=current_lecturer.user_id,
        uow=uow,
    )


@course_request_lecturer_router.post(
    path="/{course_id}/{request_id}/{student_id}/reject",
    status_code=status.HTTP_202_ACCEPTED,
    responses=accept_reject_request_response,
)
async def reject_course_request(
    course_id: uuid.UUID,
    request_id: uuid.UUID,
    student_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    course_request_service = CourseEnrollmentService()
    await course_request_service.reject_course_request(
        course_id=course_id,
        course_request_id=request_id,
        student_id=student_id,
        lecturer_id=current_lecturer.id,
        lecturer_user_id=current_lecturer.user_id,
        uow=uow,
    )
