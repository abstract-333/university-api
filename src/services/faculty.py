from common import IUnitOfWork
from schemas import Faculty
from schemas.pagination import Pagination
from specification.faculty import FacultyNameSpecification


class FacultyService:
    @classmethod
    async def _get_all_faculties(
        cls,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[Faculty] | None:
        async with uow:
            return await uow.faculty.get_faculties_all(pagination=pagination)

    @classmethod
    async def get_faculties_by_name(
        cls,
        uow: IUnitOfWork,
        name: str,
        pagination: Pagination,
    ) -> list[Faculty] | None:
        async with uow:
            return await uow.faculty.get_faculties(
                specification=FacultyNameSpecification(name=name),
                pagination=pagination,
            )

    async def get_all_faculites(
        self,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[Faculty] | None:
        try:
            facutlies: list[Faculty] | None = await self._get_all_faculties(
                uow=uow, pagination=pagination
            )
            return facutlies

        except Exception as exception:
            raise exception
