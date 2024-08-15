from abc import ABC, abstractmethod
from models.course_request import CoursesRequestsOrm
from models.student import StudentsOrm
from models.taught_courses import TaughtCoursesOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas.course_request import (
    CourseRequestInDB,
    CourseRequestInDBExtended,
    CourseRequestInDBExtendedStudent,
)
from schemas.pagination import Pagination
from specification.base import Specification
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class CourseRequestRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_course_request(
        self,
        course_request_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_course_request(
        self,
        course_request_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def get_course_requests_extended_course_processed_by(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseRequestInDBExtended] | None:
        ...

    @abstractmethod
    async def get_course_requests_extended_student(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseRequestInDBExtendedStudent,] | None:
        ...

    @abstractmethod
    async def get_course_requests(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseRequestInDB] | None:
        ...

    @abstractmethod
    async def get_course_request(
        self,
        specification: Specification,
    ) -> CourseRequestInDB | None:
        ...


class CourseRequestRepository(SQLAlchemyRepository, CourseRequestRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[CoursesRequestsOrm] = CoursesRequestsOrm
        super().__init__(session=session)

    async def add_course_request(
        self,
        course_request_data: dict,
    ) -> None:
        await self.add_one(data=course_request_data)

    async def edit_course_request(
        self,
        course_request_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=course_request_data,
            arguments=specification.is_satisfied_by(),
        )

    async def get_course_request(
        self, specification: Specification
    ) -> CourseRequestInDB | None:
        course_request_record: CourseRequestInDB | None = await self.find_one(
            schema=CourseRequestInDB,
            arguments=specification.is_satisfied_by(),
        )
        return course_request_record

    async def get_course_requests_extended_student(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseRequestInDBExtendedStudent] | None:
        return await self.find_by(
            joinedload(self.model_cls.student).joinedload(StudentsOrm.user),
            schema=CourseRequestInDBExtendedStudent,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_course_requests_extended_course_processed_by(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseRequestInDBExtended] | None:
        course_requests_records: list[
            CourseRequestInDBExtended
        ] | None = await self.find_by(
            joinedload(self.model_cls.course).joinedload(
                TaughtCoursesOrm.speciality_course
            ),
            joinedload(self.model_cls.processed_by_user),
            # join_conditions=(
            #     self.model_cls.course,
            #     SpecialityCoursesOrm,
            # ),
            schema=CourseRequestInDBExtended,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return course_requests_records

    async def get_course_requests(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CourseRequestInDB] | None:
        course_requests_records: list[CourseRequestInDB] | None = await self.find_by(
            schema=CourseRequestInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return course_requests_records
