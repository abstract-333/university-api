from abc import ABC, abstractmethod
from models.course_lecturer import CoursesLecturersOrm
from sqlalchemy.ext.asyncio import AsyncSession

from models.speciality_course import SpecialityCoursesOrm
from models.taught_courses import TaughtCoursesOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from schemas.course_lecturer import CourseLecturerInDB, CourseLecturerInDBExtended
from schemas.pagination import Pagination
from specification.base import Specification
from sqlalchemy.orm import joinedload, selectinload


class CourseLecturerRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_course_lecturers(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseLecturerInDB] | None:
        ...

    @abstractmethod
    async def get_course_lecturer_extended(
        self,
        specification: Specification,
    ) -> CourseLecturerInDBExtended | None:
        ...

    @abstractmethod
    async def get_courses_lecturer_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseLecturerInDBExtended] | None:
        ...

    @abstractmethod
    async def get_course_lecturer(
        self,
        specification: Specification,
    ) -> CourseLecturerInDB | None:
        ...

    @abstractmethod
    async def add_course_lecturer(
        self,
        course_lecturer_data: dict,
    ) -> None:
        ...


class CourseLecturerRepository(SQLAlchemyRepository, CourseLecturerRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[CoursesLecturersOrm] = CoursesLecturersOrm
        super().__init__(session=session)

    async def get_course_lecturers(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseLecturerInDB] | None:
        courses_lecturers: list[CourseLecturerInDB] | None = await self.find_by(
            arguments=specification.is_satisfied_by(),
            schema=CourseLecturerInDB,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return courses_lecturers

    async def get_course_lecturer_extended(
        self, specification: Specification
    ) -> CourseLecturerInDBExtended | None:
        return await self.find_one(
            joinedload(self.model_cls.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            arguments=specification.is_satisfied_by(),
            schema=CourseLecturerInDBExtended,
        )

    async def get_courses_lecturer_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseLecturerInDBExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            arguments=specification.is_satisfied_by(),
            schema=CourseLecturerInDBExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_course_lecturer(
        self,
        specification: Specification,
    ) -> CourseLecturerInDB | None:
        return await self.find_one(
            arguments=specification.is_satisfied_by(),
            schema=CourseLecturerInDB,
        )

    async def add_course_lecturer(self, course_lecturer_data: dict) -> None:
        await self.add_one(data=course_lecturer_data)
