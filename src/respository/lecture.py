from abc import ABC, abstractmethod

from models.lecture import LecturesOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.lecture import LectureInDBExtended
from schemas.pagination import Pagination
from specification.base import Specification


class LectureRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_lectures(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[LectureInDBExtended] | None:
        ...

    @abstractmethod
    async def get_lecture(
        self,
        specification: Specification,
    ) -> LectureInDBExtended | None:
        ...

    @abstractmethod
    async def add_lecture(
        self,
        lecture_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_lecture(
        self,
        lecture_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def delete_lecture(
        self,
        specification: Specification,
    ) -> None:
        ...


class LectureRepository(SQLAlchemyRepository, LectureRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[LecturesOrm] = LecturesOrm
        super().__init__(session=session)

    async def add_lecture(
        self,
        lecture_data: dict,
    ) -> None:
        await self.add_one(
            data=lecture_data,
        )

    async def edit_lecture(
        self,
        lecture_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=lecture_data,
            arguments=specification.is_satisfied_by(),
        )

    async def get_lecture(
        self, specification: Specification
    ) -> LectureInDBExtended | None:
        return await self.find_one(
            joinedload(self.model_cls.file),
            arguments=specification.is_satisfied_by(),
            schema=LectureInDBExtended,
        )

    async def get_lectures(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[LectureInDBExtended] | None:
        return await self.find_by(
            selectinload(self.model_cls.file),
            join_conditions=(self.model_cls.lecturer_course,),
            arguments=specification.is_satisfied_by(),
            schema=LectureInDBExtended,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def delete_lecture(
        self,
        specification: Specification,
    ) -> None:
        return await self.delete_one(
            arguments=specification.is_satisfied_by(),
        )
