import uuid
from fastapi import APIRouter
from dependencies import UOWDep, CurrentActiveUserDep
from dependencies.dependencies import PaginationDep
from services.session import SessionService
from api.docs.session import (
    get_session_response,
    delete_session_response,
    get_sessions_response,
)
from starlette import status

session_router = APIRouter(
    prefix="/session",
    tags=["Active Session: User"],
)


@session_router.get(
    path="/all",
    responses=get_sessions_response,
)
# @cache(expire=300)
async def get_all_sessions(
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
    pagination: PaginationDep,
):
    session_service = SessionService()

    return await session_service.get_all_sessions_for_user(
        user_id=current_user.id,
        pagination=pagination,
        uow=uow,
    )


@session_router.get(
    path="/{device_id}",
    responses=get_session_response,
)
async def get_session(
    device_id: str,
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
):
    session_service = SessionService()

    return await session_service.get_session(
        device_id=device_id,
        user_id=current_user.id,
        uow=uow,
    )


@session_router.delete(
    path="/{session_id}/{current_device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_session_response,
)
async def delete_newer_session(
    current_device_id: str,
    session_id: uuid.UUID,
    current_user: CurrentActiveUserDep,
    uow: UOWDep,
):
    session_service = SessionService()
    await session_service.delete_newer_session(
        session_id=session_id,
        current_device_id=current_device_id,
        user_id=current_user.id,
        uow=uow,
    )
