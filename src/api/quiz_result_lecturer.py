from uuid import UUID
from fastapi import APIRouter
from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from services.quiz_result import QuizResultService
from api.docs.quiz_result_lecturer import get_quiz_results_responses

quiz_result_lecturer_router = APIRouter(
    prefix="/quiz_result/lecturer",
    tags=["Quiz Result: Lecturer"],
)


@quiz_result_lecturer_router.get(
    path="/{course_lecturer_id}/{quiz_id}",
    responses=get_quiz_results_responses,
)
async def get_quiz_results(
    quiz_id: UUID,
    course_lecturer_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    quiz_service = QuizResultService()
    return await quiz_service.get_quiz_results_by_lecturer(
        quiz_id=quiz_id,
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )
