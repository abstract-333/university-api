from uuid import UUID

from fastapi import APIRouter
from starlette import status

from api.docs.quiz_lecturer import (
    get_quizzes_course_responses,
    delete_quiz_responses,
    add_quiz_responses,
)
from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from schemas import QuizCreate
from services.quiz import QuizService

quiz_lecturer_router = APIRouter(
    prefix="/quiz/lecturer",
    tags=["Quiz: Lecturer"],
)


@quiz_lecturer_router.get(
    path="/{course_lecturer_id}/active_pending",
    responses=get_quizzes_course_responses,
)
async def get_active_pending_quizzes_for_course(
    course_lecturer_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    quiz_service = QuizService()
    return await quiz_service.get_active_quizzes_for_course_by_lecturer(
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@quiz_lecturer_router.get(
    path="/{course_lecturer_id}/all",
    responses=get_quizzes_course_responses,
)
async def get_all_quizzes_for_course(
    course_lecturer_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    quiz_service = QuizService()
    return await quiz_service.get_all_quizzes_for_course_by_lecturer(
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@quiz_lecturer_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=add_quiz_responses,
)
async def add_quiz(
    quiz_create: QuizCreate,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    quiz_service = QuizService()
    await quiz_service.add_quiz(
        quiz_create=quiz_create,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )


@quiz_lecturer_router.delete(
    path="/{course_lecturer_id}/{quiz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_quiz_responses,
)
async def delete_quiz(
    course_lecturer_id: UUID,
    quiz_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    quiz_service = QuizService()
    await quiz_service.delete_quiz(
        quiz_id=quiz_id,
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )
