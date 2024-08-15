from uuid import UUID
from fastapi import APIRouter
from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from schemas.quiz_result import QuizResultCreate
from services.quiz_result import QuizResultService
from api.docs.quiz_result_student import (
    get_quizzes_results_responses,
    add_quiz_result_responses,
)
from starlette import status

quiz_result_student_router = APIRouter(
    prefix="/quiz_result/student",
    tags=["Quiz Result: Student"],
)


@quiz_result_student_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=add_quiz_result_responses,
)
async def add_quiz_result(
    quiz_result_create: QuizResultCreate,
    current_student: CurrentStudentDep,
    uow: UOWDep,
):
    quiz_service = QuizResultService()
    await quiz_service.add_quiz_result(
        student_id=current_student.id,
        quiz_result_create=quiz_result_create,
        uow=uow,
    )


@quiz_result_student_router.get(
    path="/{enrolled_course_id}",
    responses=get_quizzes_results_responses,
)
async def get_quizzes_results_for_course(
    enrolled_course_id: UUID,
    current_student: CurrentStudentDep,
    uow: UOWDep,
    pagination: PaginationDep,
):
    quiz_service = QuizResultService()
    return await quiz_service.get_quizzes_results_for_student(
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        uow=uow,
        pagination=pagination,
    )
