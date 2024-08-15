from abc import ABC, abstractmethod

from models import SpecialitiesOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas import SpecialityInDB
from schemas.pagination import Pagination
from specification import Specification
from sqlalchemy.ext.asyncio import AsyncSession


class SpecialityRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_speciality(
        self,
        specification: Specification,
    ) -> SpecialityInDB | None:
        ...

    @abstractmethod
    async def get_specialities(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityInDB] | None:
        ...

    @abstractmethod
    async def get_specialities_all(
        self,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityInDB] | None:
        ...


class SpecialityRepository(SQLAlchemyRepository, SpecialityRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[SpecialitiesOrm] = SpecialitiesOrm
        super().__init__(session=session)

    async def get_speciality(
        self,
        specification: Specification,
    ) -> SpecialityInDB | None:
        speciality: SpecialityInDB | None = await self.find_one(
            schema=SpecialityInDB,
            arguments=specification.is_satisfied_by(),
        )
        return speciality

    async def get_specialities(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityInDB] | None:
        specialities: list[SpecialityInDB] | None = await self.find_by(
            schema=SpecialityInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return specialities

    async def get_specialities_all(
        self,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityInDB] | None:
        specialities: list[SpecialityInDB] | None = await self.find_by(
            schema=SpecialityInDB,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return specialities
