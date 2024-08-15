from abc import ABC, abstractmethod

from models.faculty import FacultiesOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas import Faculty
from schemas.pagination import Pagination
from specification.base import Specification
from sqlalchemy.ext.asyncio import AsyncSession


class FacultyRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_faculties(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[Faculty] | None:
        ...

    @abstractmethod
    async def get_faculties_all(
        self, pagination: Pagination = Pagination()
    ) -> list[Faculty] | None:
        ...


class FacultyRepository(SQLAlchemyRepository, FacultyRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[FacultiesOrm] = FacultiesOrm
        super().__init__(session=session)

    async def get_faculties(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[Faculty] | None:
        faculties: list[Faculty] | None = await self.find_by(
            arguments=specification.is_satisfied_by(),
            schema=Faculty,
            limit=pagination.limit,
            offset=pagination.offset,
        )
        return faculties

    async def get_faculties_all(
        self, pagination: Pagination = Pagination()
    ) -> list[Faculty] | None:
        faculties: list[Faculty] | None = await self.find_by(
            schema=Faculty,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return faculties
