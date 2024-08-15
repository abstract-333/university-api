from fastapi import APIRouter
from starlette import status

from api.docs import (
    accept_pending_lecturer_request_response,
)
from dependencies import UOWDep
from dependencies.dependencies import CurrentVerifiedSuperUserDep
from schemas.lecturer_request import (
    LecturerRequestProcess,
)
from services.lecturer_request import LecturerRequestService

lecturer_request_admin_router = APIRouter(
    prefix="/lecturer_request/admin",
    tags=["Lecturer Request: Admin"],
)


@lecturer_request_admin_router.post(
    path="/accept",
    responses=accept_pending_lecturer_request_response,
    status_code=status.HTTP_200_OK,
)
async def process_lecturer_request_by_admin(
    uow: UOWDep,
    accept: bool,
    lecturer_request: LecturerRequestProcess,
    current_user: CurrentVerifiedSuperUserDep,
):
    lecturer_request_service = LecturerRequestService()
    if accept:
        await lecturer_request_service.accept_lecturer_request(
            lecturer_request=lecturer_request,
            uow=uow,
        )
    else:
        await lecturer_request_service.reject_lecturer_request(
            lecturer_request=lecturer_request, uow=uow
        )
    return {"message": "request processed"}
