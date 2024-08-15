import uuid

from fastapi import APIRouter, Query
from starlette import status

from api.docs import (
    send_lecturer_request_response,
    get_pending_lecturer_requests_response,
    edit_pending_lecturer_request_response,
)
from dependencies import UOWDep, CurrentVerifiedUserDep
from dependencies.dependencies import PaginationDep
from schemas.lecturer_request import (
    LecturerRequestCreate,
    LecturerRequestUpdate,
)
from services.lecturer_request import LecturerRequestService

lecturer_request_router = APIRouter(
    prefix="/lecturer_request",
    tags=["Lecturer Request: User"],
)


@lecturer_request_router.post(
    path="",
    responses=send_lecturer_request_response,
    status_code=status.HTTP_201_CREATED,
)
async def send_lecturer_request(
    uow: UOWDep,
    current_user: CurrentVerifiedUserDep,
    faculty_name: str = Query(min_length=2, max_length=32),
    description: str | None = Query(min_length=0, max_length=50),
):
    lecturer_request_create = LecturerRequestCreate(
        user_id=current_user.id, faculty_name=faculty_name, description=description
    )
    lecturer_request_service = LecturerRequestService()
    await lecturer_request_service.add_lecturer_request(
        lecturer_request_create=lecturer_request_create, uow=uow
    )


@lecturer_request_router.get(
    path="/me",
    responses=get_pending_lecturer_requests_response,
)
async def get_pending_requests(
    uow: UOWDep,
    pagination: PaginationDep,
    current_user: CurrentVerifiedUserDep,
):
    lecturer_request_service = LecturerRequestService()
    return await lecturer_request_service.get_all_lecturer_requests(
        user_id=current_user.id,
        pagination=pagination,
        uow=uow,
    )


@lecturer_request_router.patch(
    path="",
    status_code=status.HTTP_200_OK,
    responses=edit_pending_lecturer_request_response,
)
async def edit_pending_request(
    uow: UOWDep,
    request_id: uuid.UUID,
    lecturer_request_update: LecturerRequestUpdate,
    current_user: CurrentVerifiedUserDep,
):
    lecturer_request_service = LecturerRequestService()
    await lecturer_request_service.edit_lecturer_request(
        user_id=current_user.id,
        request_id=request_id,
        lecturer_request_update=lecturer_request_update,
        uow=uow,
    )
    return {"message": "updated successfully"}
