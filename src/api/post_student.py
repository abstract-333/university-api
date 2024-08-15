import uuid
from fastapi import APIRouter
from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from services.post import PostService
from api.docs.post_student import (
    get_posts_me_responses,
    get_post_responses,
)

post_student_router = APIRouter(
    prefix="/post/student",
    tags=["Post: Student"],
)


@post_student_router.get(
    path="/{enrolled_course_id}",
    responses=get_posts_me_responses,
)
async def get_posts_me(
    enrolled_course_id: uuid.UUID,
    uow: UOWDep,
    current_student: CurrentStudentDep,
    pagination: PaginationDep,
):
    post_service = PostService()
    return await post_service.get_posts_course_student(
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        uow=uow,
        pagination=pagination,
    )


@post_student_router.get(
    path="/{enrolled_course_id}/{post_id}",
    responses=get_post_responses,
)
async def get_post_detailed(
    enrolled_course_id: uuid.UUID,
    post_id: uuid.UUID,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    post_service = PostService()
    return await post_service.get_post_detailed_for_student(
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        post_id=post_id,
        uow=uow,
    )
