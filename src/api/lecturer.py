import uuid
from fastapi import APIRouter
from starlette import status
from api.docs import (
    register_lecturer_response,
    get_all_my_lecturers_response,
    get_tokens_lecturer_response,
    get_me_lecturer_response,
)
from dependencies.dependencies import (
    CurrentLecturerDep,
    CurrentVerifiedSuperUserDep,
    PaginationDep,
    UOWDep,
    CurrentVerifiedUserDep,
)
from schemas import LecturerCreate
from schemas.auth import AccessRefreshTokens
from services import LecturerService
from services.auth import AuthService

lecturer_router = APIRouter(
    prefix="/lecturer",
    tags=["Lecturer"],
)


@lecturer_router.post(
    path="/get-tokens",
    status_code=status.HTTP_200_OK,
    responses=get_tokens_lecturer_response,
)
async def get_access_refresh_tokens_lecturer(
    uow: UOWDep,
    refresh_token: str,
    lecturer_id: uuid.UUID,
    device_id: str,
    current_user: CurrentVerifiedUserDep,
):
    lecturer_service = LecturerService()
    auth_service = AuthService()

    new_refresh_token: bytes = await auth_service.create_refresh_token(
        refresh_token=refresh_token,
        device_id=device_id,
        uow=uow,
    )
    access_token: bytes = await lecturer_service.make_token_lecturer(
        lecturer_id=lecturer_id,
        uow=uow,
    )
    return AccessRefreshTokens(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )


@lecturer_router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    responses=get_me_lecturer_response,
)
async def get_lecturer(
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
):
    return current_lecturer


@lecturer_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    responses=register_lecturer_response,
)
async def register_lecturer_by_admin(
    uow: UOWDep,
    faculty_name: str,
    user_id: uuid.UUID,
    current_superuser: CurrentVerifiedSuperUserDep,
):
    """
    User must be superuser, verified and active
    """
    lecturer_service = LecturerService()
    lecturer_data = LecturerCreate(user_id=user_id, faculty_name=faculty_name)
    await lecturer_service.register_lecturer(lecturer_data=lecturer_data, uow=uow)
    return {"message": "success"}


@lecturer_router.get(
    path="/all",
    responses=get_all_my_lecturers_response,
)
async def get_my_lecturers_list(
    uow: UOWDep,
    current_user: CurrentVerifiedUserDep,
    pagination: PaginationDep,
):
    lecturer_service = LecturerService()
    return await lecturer_service._get_lecturers(
        user_id=current_user.id,
        pagination=pagination,
        uow=uow,
    )
