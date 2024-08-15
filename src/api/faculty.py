from fastapi import APIRouter, Request

from dependencies import UOWDep, CurrentActiveUserDep
from dependencies.dependencies import PaginationDep
from services import FacultyService
from api.docs.faculty import get_all_faculties_response


faculty_router = APIRouter(
    prefix="/faculty",
    tags=["Faculty: User"],
)


@faculty_router.get(
    path="/all",
    responses=get_all_faculties_response,
)
# @cache(expire=300)
async def get_all_faculties(
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
    pagination: PaginationDep,
    request: Request,
):
    faculty_service = FacultyService()
    return await faculty_service.get_all_faculites(pagination=pagination, uow=uow)
