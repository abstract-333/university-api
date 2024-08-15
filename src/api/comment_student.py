from uuid import UUID
from fastapi import APIRouter
from starlette import status

from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
)
from services import CommentService
from api.docs.comment_student import (
    get_comments_responses,
    add_comment_responses,
    update_comment_responses,
    delete_comment_responses,
)

comment_student_router = APIRouter(
    prefix="/comment/student",
    tags=["Comment: Student"],
)


@comment_student_router.get(
    path="/{enrolled_course_id}/{post_id}",
    status_code=status.HTTP_200_OK,
    responses=get_comments_responses,
)
async def get_comments(
    post_id: UUID,
    enrolled_course_id: UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_student: CurrentStudentDep,
):
    comment_service = CommentService()
    return await comment_service.get_comments_for_post_by_student(
        post_id=post_id,
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        pagination=pagination,
        uow=uow,
    )


@comment_student_router.get(
    path="/{enrolled_course_id}/{post_id}/me",
    status_code=status.HTTP_200_OK,
    responses=get_comments_responses,
)
async def get_my_comments(
    post_id: UUID,
    enrolled_course_id: UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_student: CurrentStudentDep,
):
    comment_service = CommentService()
    return await comment_service.get_own_comments_for_student(
        post_id=post_id,
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        pagination=pagination,
        uow=uow,
    )


@comment_student_router.post(
    path="/{enrolled_course_id}/{post_id}",
    status_code=status.HTTP_201_CREATED,
    responses=add_comment_responses,
)
async def add_comment(
    post_id: UUID,
    enrolled_course_id: UUID,
    body: str,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    comment_service = CommentService()
    return await comment_service.add_comment_for_student(
        post_id=post_id,
        enrolled_course_id=enrolled_course_id,
        student_id=current_student.id,
        body=body,
        uow=uow,
    )


@comment_student_router.patch(
    path="/{comment_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses=update_comment_responses,
)
async def edit_comment(
    comment_id: UUID,
    body: str,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    comment_service = CommentService()
    return await comment_service.update_comment_for_student(
        comment_id=comment_id,
        student_id=current_student.id,
        body=body,
        uow=uow,
    )


@comment_student_router.delete(
    path="/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_comment_responses,
)
async def delete_comment(
    comment_id: UUID,
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    comment_service = CommentService()
    return await comment_service.delete_comment_for_student(
        comment_id=comment_id,
        student_id=current_student.id,
        uow=uow,
    )
