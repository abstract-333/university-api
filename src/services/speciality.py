from common import IUnitOfWork
from schemas import SpecialityInDB
from schemas.pagination import Pagination
from specification import SpecialityFacultySpecification, SpecialityNameSpecification


class SpecialityService:
    @classmethod
    async def get_speciality_by_name(
        cls,
        name: str,
        uow: IUnitOfWork,
    ) -> SpecialityInDB | None:
        async with uow:
            speciality: SpecialityInDB | None = await uow.speciality.get_speciality(
                specification=SpecialityNameSpecification(name=name),
            )
            return speciality

    @classmethod
    async def get_specialities_by_faculty_name(
        cls,
        faculty_name: str,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[SpecialityInDB] | None:
        async with uow:
            specialities: list[
                SpecialityInDB
            ] | None = await uow.speciality.get_specialities(
                specification=SpecialityFacultySpecification(faculty_name=faculty_name),
                pagination=pagination,
            )
            return specialities

    @classmethod
    async def get_all_specialities(
        cls,
        uow: IUnitOfWork,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityInDB] | None:
        async with uow:
            specialities: list[
                SpecialityInDB
            ] | None = await uow.speciality.get_specialities_all(pagination=pagination)
            return specialities
