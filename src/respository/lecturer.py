from abc import ABC, abstractmethod

from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas import LecturerInDB
from models import LecturersOrm
from schemas.pagination import Pagination
from specification.base import Specification
from sqlalchemy.ext.asyncio import AsyncSession


class LecturerRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_lecturer(
        self,
        lecturer_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def get_lecturers(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[LecturerInDB] | None:
        ...

    @abstractmethod
    async def get_lecturer(
        self,
        specification: Specification,
    ) -> LecturerInDB | None:
        ...


class LecturerRepository(SQLAlchemyRepository, LecturerRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[LecturersOrm] = LecturersOrm
        super().__init__(session=session)

    async def add_lecturer(
        self,
        lecturer_data: dict,
    ) -> None:
        await self.add_one(lecturer_data)

    async def get_lecturers(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[LecturerInDB] | None:
        lecturer_records: list[LecturerInDB] | None = await self.find_by(
            schema=LecturerInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return lecturer_records

    async def get_lecturer(
        self,
        specification: Specification,
    ) -> LecturerInDB | None:
        lecturer: LecturerInDB | None = await self.find_one(
            schema=LecturerInDB,
            arguments=specification.is_satisfied_by(),
        )
        return lecturer
