from abc import ABC, abstractmethod

from models.speciality import SpecialitiesOrm
from models.speciality_course import SpecialityCoursesOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas.pagination import Pagination
from schemas.speciality_course import SpecialityCourseInDB
from specification import Specification
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import joinedload, selectinload


class SpecialityCourseRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_speciality_course(
        self,
        specification: Specification,
    ) -> SpecialityCourseInDB | None:
        ...

    @abstractmethod
    async def get_speciality_courses(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityCourseInDB] | None:
        ...

    @abstractmethod
    async def get_speciality_courses_all(
        self,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityCourseInDB] | None:
        ...


class SpecialityCourseRepository(SQLAlchemyRepository, SpecialityCourseRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[SpecialityCoursesOrm] = SpecialityCoursesOrm
        super().__init__(session=session)

    async def get_speciality_course(
        self,
        specification: Specification,
    ) -> SpecialityCourseInDB | None:
        speciality_course: SpecialityCourseInDB | None = await self.find_one(
            schema=SpecialityCourseInDB,
            arguments=specification.is_satisfied_by(),
        )
        return speciality_course

    async def get_speciality_courses(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityCourseInDB] | None:
        speciality_courses: list[SpecialityCourseInDB] | None = await self.find_by(
            joinedload(self.model_cls.speciality),
            join_conditions=(SpecialitiesOrm,),
            schema=SpecialityCourseInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return speciality_courses

    async def get_speciality_courses_all(
        self,
        pagination: Pagination = Pagination(),
    ) -> list[SpecialityCourseInDB] | None:
        speciality_courses: list[SpecialityCourseInDB] | None = await self.find_by(
            schema=SpecialityCourseInDB,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return speciality_courses
