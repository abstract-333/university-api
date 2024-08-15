from uuid import UUID
from fastapi import APIRouter
from starlette import status

from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    StorageDep,
    UOWDep,
)
from api.docs.lecture_lecturer import (
    get_lectures_responses,
    add_lecture_responses,
    delete_lecture_responses,
)
from schemas.lecture import LectureCreate
from services.lecture import LectureService

lecture_lecturer_router = APIRouter(
    prefix="/lecture/lecturer",
    tags=["Lecture: Lecturer"],
)


@lecture_lecturer_router.get(
    path="/{course_lecturer_id}",
    status_code=status.HTTP_200_OK,
    responses=get_lectures_responses,
)
async def get_my_lectures_for_course(
    course_lecturer_id: UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_lecturer: CurrentLecturerDep,
):
    lecture_service = LectureService()
    return await lecture_service.get_lectures_for_lecturer(
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        pagination=pagination,
        uow=uow,
    )


@lecture_lecturer_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=add_lecture_responses,
)
async def add_lecture(
    lecture_create: LectureCreate,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    lecture_service = LectureService()
    await lecture_service.add_lecture(
        lecture_create=lecture_create,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )


@lecture_lecturer_router.delete(
    path="/{course_lecturer_id}/{lecture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_lecture_responses,
)
async def delete_lecture(
    lecture_id: UUID,
    course_lecturer_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    storage: StorageDep,
):
    lecture_service = LectureService()
    await lecture_service.delete_lecture(
        course_lecturer_id=course_lecturer_id,
        lecture_id=lecture_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        storage=storage,
    )
