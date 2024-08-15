from starlette import status

from fastapi import APIRouter
from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from schemas.question import QuestionCreate, QuestionUpdate
from services.question import QuestionService
from api.docs.question_lecturer import (
    add_question_responses,
    get_questions_responses,
    update_question_responses,
)
from uuid import UUID

question_lecturer_router = APIRouter(
    prefix="/question/lecturer",
    tags=["Question: Lecturer"],
)


@question_lecturer_router.get(
    path="/{lecturer_course_id}/me",
    status_code=status.HTTP_200_OK,
    responses=get_questions_responses,
)
async def get_questions_added_by_me_in_course(
    course_lecturer_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    question_service = QuestionService()
    return await question_service.get_questions_by_lecturer(
        lecturer_course_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@question_lecturer_router.get(
    path="/{lecturer_course_id}/all",
    status_code=status.HTTP_200_OK,
    responses=get_questions_responses,
)
async def get_questions_in_course(
    course_lecturer_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    question_service = QuestionService()
    return await question_service.get_questions_in_course(
        lecturer_course_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@question_lecturer_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=add_question_responses,
)
async def add_question(
    question_create: QuestionCreate,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    question_service = QuestionService()
    await question_service.add_question(
        question_create=question_create,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )


@question_lecturer_router.patch(
    path="/{lecturer_course_id}/{question_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses=update_question_responses,
)
async def update_question(
    question_update: QuestionUpdate,
    lecturer_course_id: UUID,
    question_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    question_service = QuestionService()
    await question_service.edit_question(
        question_update=question_update,
        question_id=question_id,
        lecturer_course_id=lecturer_course_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )
