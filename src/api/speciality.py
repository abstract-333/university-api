from fastapi import APIRouter

from api.docs.speciality import (
    get_specialities_by_faculty_response,
    get_all_specialities_response,
)
from dependencies import UOWDep, CurrentActiveUserDep
from dependencies.dependencies import PaginationDep
from services import SpecialityService

speciality_router = APIRouter(
    prefix="/speciality",
    tags=["Speciality: User"],
)


@speciality_router.get(
    path="/all",
    responses=get_all_specialities_response,
)
async def get_all_specialities(
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
    pagination: PaginationDep,
):
    speciality_service = SpecialityService()
    return await speciality_service.get_all_specialities(
        uow=uow,
        pagination=pagination,
    )


@speciality_router.get(
    path="/{faculty}",
    responses=get_specialities_by_faculty_response,
)
async def get_specialities_by_faculty_name(
    uow: UOWDep,
    faculty: str,
    current_user: CurrentActiveUserDep,
    pagination: PaginationDep,
):
    speciality_service = SpecialityService()
    return await speciality_service.get_specialities_by_faculty_name(
        faculty_name=faculty, uow=uow, pagination=pagination
    )
