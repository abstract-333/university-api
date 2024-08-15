import uuid
from fastapi import APIRouter
from starlette import status
from dependencies.dependencies import (
    CurrentLecturerDep,
    PaginationDep,
    UOWDep,
)
from schemas.post import PostCreate, PostUpdate
from services.post import PostService
from api.docs.post_lecturer import (
    create_post_response,
    get_posts_me_responses,
    update_post_response,
    delete_post_response,
    get_post_responses,
)

post_lecturer_router = APIRouter(
    prefix="/post/lecturer",
    tags=["Post: Lecturer"],
)


@post_lecturer_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=create_post_response,
)
async def create_post(
    post_create: PostCreate,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    post_service = PostService()

    await post_service.add_post(
        lecturer_id=current_lecturer.id,
        post_create=post_create,
        uow=uow,
    )


@post_lecturer_router.get(
    path="/{course_lecturer_id}/all",
    responses=get_posts_me_responses,
)
async def get_posts_all(
    course_lecturer_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    post_service = PostService()
    return await post_service.get_posts_for_course_lecturer(
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@post_lecturer_router.get(
    path="/{course_lecturer_id}/me",
    responses=get_posts_me_responses,
)
async def get_posts_me(
    course_lecturer_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    pagination: PaginationDep,
):
    post_service = PostService()
    return await post_service.get_posts_added_lecturer(
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
        pagination=pagination,
    )


@post_lecturer_router.get(
    path="/{course_lecturer_id}/{post_id}",
    responses=get_post_responses,
)
async def get_post_detailed(
    course_lecturer_id: uuid.UUID,
    post_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    post_service = PostService()
    return await post_service.get_post_detailed_for_lecturer(
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        post_id=post_id,
        uow=uow,
    )


@post_lecturer_router.patch(
    path="",
    status_code=status.HTTP_202_ACCEPTED,
    responses=update_post_response,
)
async def update_post(
    post_update: PostUpdate,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    post_service = PostService()
    await post_service.update_post(
        post_update=post_update,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )


@post_lecturer_router.delete(
    path="/{post_id}/{course_lecturer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_post_response,
)
async def delete_post(
    post_id: uuid.UUID,
    course_lecturer_id: uuid.UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    post_service = PostService()
    await post_service.delete_post(
        post_id=post_id,
        course_lecturer_id=course_lecturer_id,
        lecturer_id=current_lecturer.id,
        uow=uow,
    )
