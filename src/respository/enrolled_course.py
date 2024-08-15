from abc import ABC, abstractmethod
from models.enrolled_course import EnrolledCoursesOrm
from models.speciality_course import SpecialityCoursesOrm
from models.taught_courses import TaughtCoursesOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas.enrolled_course import (
    EnrolledCourseInDB,
    EnrolledCourseInDBExtended,
)
from schemas.pagination import Pagination
from specification.base import Specification
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class EnrolledCourseRepsitoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_enrolled_course(
        self,
        enrolled_course_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_enrolled_course(
        self,
        enrolled_course_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def get_enrolled_courses(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[EnrolledCourseInDBExtended] | None:
        ...

    @abstractmethod
    async def get_enrolled_course(
        self,
        specification: Specification,
    ) -> EnrolledCourseInDB | None:
        ...


class EnrolledCourseRepsitory(SQLAlchemyRepository, EnrolledCourseRepsitoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[EnrolledCoursesOrm] = EnrolledCoursesOrm
        super().__init__(session=session)

    async def add_enrolled_course(
        self,
        enrolled_course_data: dict,
    ) -> None:
        await self.add_one(data=enrolled_course_data)

    async def edit_enrolled_course(
        self,
        enrolled_course_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=enrolled_course_data,
            arguments=specification.is_satisfied_by(),
        )

    async def get_enrolled_course(
        self, specification: Specification
    ) -> EnrolledCourseInDB | None:
        return await self.find_one(
            schema=EnrolledCourseInDB,
            arguments=specification.is_satisfied_by(),
        )

    async def get_enrolled_courses(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[EnrolledCourseInDBExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            schema=EnrolledCourseInDBExtended,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
