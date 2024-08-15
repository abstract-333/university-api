from uuid import UUID
from fastapi import APIRouter
from starlette import status

from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from services import CommentService
from api.docs.comment_lecturer import (
    get_comments_responses,
    add_comment_responses,
    update_comment_responses,
    delete_comment_responses,
)

comment_lecturer_router = APIRouter(
    prefix="/comment/lecturer",
    tags=["Comment: Lecturer"],
)


@comment_lecturer_router.get(
    path="/{course_lecturer_id}/{post_id}",
    status_code=status.HTTP_200_OK,
    responses=get_comments_responses,
)
async def get_comments(
    post_id: UUID,
    course_lecturer_id: UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_lecturer: CurrentLecturerDep,
):
    comment_service = CommentService()
    return await comment_service.get_comments_for_post_by_lecturer(
        post_id=post_id,
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        pagination=pagination,
        uow=uow,
    )


@comment_lecturer_router.get(
    path="/{course_lecturer_id}/{post_id}/me",
    status_code=status.HTTP_200_OK,
    responses=get_comments_responses,
)
async def get_my_comments(
    post_id: UUID,
    course_lecturer_id: UUID,
    uow: UOWDep,
    pagination: PaginationDep,
    current_lecturer: CurrentLecturerDep,
):
    comment_service = CommentService()
    return await comment_service.get_own_comments_for_lecturer(
        post_id=post_id,
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        pagination=pagination,
        uow=uow,
    )


@comment_lecturer_router.post(
    path="/{course_lecturer_id}/{post_id}",
    status_code=status.HTTP_201_CREATED,
    responses=add_comment_responses,
)
async def add_comment(
    post_id: UUID,
    course_lecturer_id: UUID,
    body: str,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    comment_service = CommentService()
    return await comment_service.add_comment_for_lecturer(
        post_id=post_id,
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        body=body,
        uow=uow,
    )


@comment_lecturer_router.patch(
    path="/{comment_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses=update_comment_responses,
)
async def edit_comment(
    comment_id: UUID,
    body: str,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    comment_service = CommentService()
    return await comment_service.update_comment_for_lecturer(
        comment_id=comment_id,
        lecturer_id=current_lecturer.id,
        body=body,
        uow=uow,
    )


@comment_lecturer_router.delete(
    path="/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_comment_responses,
)
async def delete_comment(
    comment_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    comment_service = CommentService()
    return await comment_service.delete_comment_for_lecturer(
        comment_id=comment_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )
