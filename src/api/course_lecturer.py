import uuid

from fastapi import APIRouter
from starlette import status

from api.docs.course_lecturer import (
    get_courses_me_responses,
    add_course_responses,
    join_existing_course_responses,
    edit_course_responses,
)
from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from schemas.taught_course import TaughtCourseCreate, TaughtCourseUpdate
from services.course_lecturer import CourseLecturerService
from services.taught_course import TaughtCourseService

course_lecturer_router = APIRouter(
    prefix="/course_lecturer",
    tags=["Course Lecturer: Lecturer"],
)


@course_lecturer_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=get_courses_me_responses,
)
async def get_courses_me(
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    course_service = CourseLecturerService()
    return await course_service.get_extended_course_lecturer_by_leturer(
        lecturer_id=current_lecturer.id,
        pagination=pagination,
        uow=uow,
    )


@course_lecturer_router.post(
    path="/{course_id}",
    status_code=status.HTTP_201_CREATED,
    responses=join_existing_course_responses,
)
async def join_existing_course(
    course_id: uuid.UUID,
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    course_service = CourseLecturerService()
    await course_service.add_lecturer_to_existing_course(
        course_id=course_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )


@course_lecturer_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=add_course_responses,
)
async def add_course(
    taught_course_create: TaughtCourseCreate,
    pagination: PaginationDep,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    course_service = CourseLecturerService()
    await course_service.add_lecturer_course(
        taught_course_create=taught_course_create,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )


@course_lecturer_router.patch(
    path="/{course_id}",
    status_code=status.HTTP_200_OK,
    responses=edit_course_responses,
)
async def edit_course(
    taught_course_update: TaughtCourseUpdate,
    course_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    taught_course_service = TaughtCourseService()
    return await taught_course_service.edit_taught_course(
        lecturer_id=current_lecturer.id,
        taught_course_update=taught_course_update,
        taught_course_id=course_id,
        uow=uow,
    )
