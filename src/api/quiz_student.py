from uuid import UUID


from fastapi import APIRouter
from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from services.quiz import QuizService
from api.docs.quiz_student import (
    get_active_quizzes_for_course_responses,
    get_all_active_quizzes_responses,
    start_quiz_responses,
)

quiz_student_router = APIRouter(
    prefix="/quiz/student",
    tags=["Quiz: Student"],
)


@quiz_student_router.get(
    path="/{enrolled_course_id}",
    responses=get_active_quizzes_for_course_responses,
)
async def get_active_quizzes_for_course(
    enrolled_course_id: UUID,
    current_student: CurrentStudentDep,
    uow: UOWDep,
    pagination: PaginationDep,
):
    quiz_service = QuizService()
    return await quiz_service.get_active_quizzes_for_course_by_student(
        student_id=current_student.id,
        enrolled_course_id=enrolled_course_id,
        uow=uow,
        pagination=pagination,
    )


@quiz_student_router.get(
    path="",
    responses=get_all_active_quizzes_responses,
)
async def get_all_active_quizzes(
    current_student: CurrentStudentDep,
    uow: UOWDep,
    pagination: PaginationDep,
):
    quiz_service = QuizService()
    return await quiz_service.get_all_active_quizzes_student(
        student_id=current_student.id,
        uow=uow,
        pagination=pagination,
    )


@quiz_student_router.get(
    path="/start/{enrolled_course_id}/{quiz_id}",
    responses=start_quiz_responses,
)
async def start_quiz(
    quiz_id: UUID,
    enrolled_course_id: UUID,
    current_student: CurrentStudentDep,
    uow: UOWDep,
):
    quiz_service = QuizService()
    return await quiz_service.take_quiz(
        quiz_id=quiz_id,
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        uow=uow,
    )
