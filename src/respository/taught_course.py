from abc import ABC, abstractmethod


from models.faculty import FacultiesOrm
from models.speciality import SpecialitiesOrm
from models.speciality_course import SpecialityCoursesOrm
from models.taught_courses import TaughtCoursesOrm
from sqlalchemy.ext.asyncio import AsyncSession

from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from schemas.pagination import Pagination
from schemas.taught_course import (
    TaughtCourseInDB,
    TaughtCourseInDBExtended,
    TaughtCourseInDBSpecliatyCourse,
)
from specification.base import Specification
from sqlalchemy.orm import joinedload, selectinload, InstrumentedAttribute


class TaughtCourseRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_taught_courses_with_speciality(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[TaughtCourseInDBExtended] | None:
        ...

    @abstractmethod
    async def get_taught_courses_with_speciality_course(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[TaughtCourseInDBSpecliatyCourse] | None:
        ...

    @abstractmethod
    async def get_taught_course_joined(
        self,
        specification: Specification,
    ) -> TaughtCourseInDBExtended | None:
        ...

    @abstractmethod
    async def get_taught_course(
        self,
        specification: Specification,
    ) -> TaughtCourseInDB | None:
        ...

    @abstractmethod
    async def add_taught_course(
        self,
        taught_course_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_taught_course(
        self,
        taught_course_data: dict,
        specification: Specification,
    ) -> None:
        ...


class TaughtCourseRepository(SQLAlchemyRepository, TaughtCourseRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[TaughtCoursesOrm] = TaughtCoursesOrm
        super().__init__(session=session)

    async def get_taught_courses_with_speciality(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[TaughtCourseInDBExtended] | None:
        taught_courses_with_speciality_course: list[
            TaughtCourseInDBExtended
        ] | None = await self.find_by(
            joinedload(self.model_cls.speciality_course).joinedload(
                SpecialityCoursesOrm.speciality
            ),
            join_conditions=(
                SpecialityCoursesOrm,
                SpecialitiesOrm,
            ),
            arguments=specification.is_satisfied_by(),
            schema=TaughtCourseInDBExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return taught_courses_with_speciality_course

    async def get_taught_courses_with_speciality_course(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[TaughtCourseInDBSpecliatyCourse] | None:
        return await self.find_by(
            joinedload(self.model_cls.speciality_course),
            arguments=specification.is_satisfied_by(),
            schema=TaughtCourseInDBSpecliatyCourse,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_taught_course_joined(
        self, specification: Specification
    ) -> TaughtCourseInDBExtended | None:
        return await self.find_one(
            joinedload(self.model_cls.speciality_course).joinedload(
                SpecialityCoursesOrm.speciality
            ),
            arguments=specification.is_satisfied_by(),
            schema=TaughtCourseInDBExtended,
        )

    async def get_taught_course(
        self,
        specification: Specification,
    ) -> TaughtCourseInDB | None:
        return await self.find_one(
            arguments=specification.is_satisfied_by(),
            schema=TaughtCourseInDB,
        )

    async def add_taught_course(self, taught_course_data: dict) -> None:
        await self.add_one(data=taught_course_data)

    async def edit_taught_course(
        self,
        taught_course_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            arguments=specification.is_satisfied_by(),
            data=taught_course_data,
        )
