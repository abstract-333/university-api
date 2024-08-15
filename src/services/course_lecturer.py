import uuid

from common.unit_of_work import IUnitOfWork
from exception.base import (
    ExceptionBadRequest400,
    ExceptionNotAcceptable406,
    ExceptionNotFound404,
)
from exception.error_code import ErrorCode
from schemas.course_lecturer import (
    CourseLecturerCreate,
    CourseLecturerInDB,
    CourseLecturerInDBExtended,
)
from schemas.pagination import Pagination
from schemas.speciality_course import SpecialityCourseInDB
from schemas.taught_course import TaughtCourseCreate, TaughtCourseInDB
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.speciality_course import SpecialityCourseIdSpecification
from specification.taught_course import (
    TaughtCourseIdSpecification,
    TaughtCourseSpecialityCourseIDSpecification,
    TaughtCourseYearSpecification,
)


class CourseLecturerService:
    @classmethod
    async def _get_extended_courses_lecturer_by_lecturer(
        cls,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[CourseLecturerInDBExtended] | None:
        async with uow:
            return await uow.course_lecturer.get_courses_lecturer_extended(
                specification=CourseLecturerLecturerIdSpecification(
                    lecturer_id=lecturer_id
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_course_lecturer_by_lecturer_course(
        cls,
        lecturer_id: uuid.UUID,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseLecturerInDB | None:
        async with uow:
            return await uow.course_lecturer.get_course_lecturer(
                specification=CourseLecturerLecturerIdSpecification(
                    lecturer_id=lecturer_id
                )
                & CourseLecturerCourseIDSpecification(course_id=course_id),
            )

    @classmethod
    async def _get_taught_course(
        cls,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> TaughtCourseInDB | None:
        async with uow:
            return await uow.taught_course.get_taught_course(
                specification=TaughtCourseIdSpecification(
                    id=course_id,
                )
            )

    @classmethod
    async def _get_speciality_course(
        cls,
        id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> SpecialityCourseInDB | None:
        async with uow:
            return await uow.speciality_course.get_speciality_course(
                specification=SpecialityCourseIdSpecification(
                    id=id,
                )
            )

    @classmethod
    async def _get_taught_course_by_speciality_course_year(
        cls,
        speciality_course_id: uuid.UUID,
        year: int,
        uow: IUnitOfWork,
    ) -> TaughtCourseInDB | None:
        async with uow:
            return await uow.taught_course.get_taught_course(
                specification=TaughtCourseSpecialityCourseIDSpecification(
                    speciality_course_id=speciality_course_id,
                )
                & TaughtCourseYearSpecification(year=year)
            )

    @classmethod
    async def _add_lecturer_to_course(
        cls,
        course_lecturer_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.course_lecturer.add_course_lecturer(
                course_lecturer_data=course_lecturer_data
            )
            await uow.commit()

    @classmethod
    async def _add_lecturer_course_taught_course(
        cls,
        taught_course_data: TaughtCourseCreate,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.taught_course.add_taught_course(
                taught_course_data=taught_course_data.model_dump(),
            )
            taught_course: TaughtCourseInDB | None = (
                await uow.taught_course.get_taught_course(
                    specification=TaughtCourseSpecialityCourseIDSpecification(
                        speciality_course_id=taught_course_data.speciality_course_id,
                    )
                    & TaughtCourseYearSpecification(year=taught_course_data.year)
                )
            )
            if taught_course is None:
                raise ExceptionBadRequest400(detail=ErrorCode.FORBIDDEN)

            course_lecturer_create = CourseLecturerCreate(
                course_id=taught_course.id, lecturer_id=lecturer_id
            )
            await uow.course_lecturer.add_course_lecturer(
                course_lecturer_data=course_lecturer_create.model_dump(),
            )
            await uow.commit()

    async def get_extended_course_lecturer_by_leturer(
        self, lecturer_id: uuid.UUID, uow: IUnitOfWork, pagination: Pagination
    ) -> list[CourseLecturerInDBExtended] | None:
        try:
            return await self._get_extended_courses_lecturer_by_lecturer(
                lecturer_id=lecturer_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def add_lecturer_to_existing_course(
        self,
        course_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        try:
            course: TaughtCourseInDB | None = await self._get_taught_course(
                course_id=course_id,
                uow=uow,
            )
            if course is None:
                raise ExceptionNotFound404(detail=ErrorCode.TAUGHT_COURSE_NOT_EXISTS)

            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer_by_lecturer_course(
                    lecturer_id=lecturer_id,
                    course_id=course_id,
                    uow=uow,
                )
            )

            if course_lecturer is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.COURSE_LECTURER_ALREADY_EXISTS
                )

            lecture_course_create = CourseLecturerCreate(
                course_id=course_id, lecturer_id=lecturer_id
            )
            await self._add_lecturer_to_course(
                course_lecturer_data=lecture_course_create.model_dump(),
                uow=uow,
            )
            return None

        except Exception as exception:
            raise exception

    async def add_lecturer_course(
        self,
        taught_course_create: TaughtCourseCreate,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        try:
            specialty_course: SpecialityCourseInDB | None = (
                await self._get_speciality_course(
                    id=taught_course_create.speciality_course_id,
                    uow=uow,
                )
            )
            if specialty_course is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.SPECIALITY_COURSE_NOT_EXISTS
                )

            course: TaughtCourseInDB | None = (
                await self._get_taught_course_by_speciality_course_year(
                    speciality_course_id=taught_course_create.speciality_course_id,
                    year=taught_course_create.year,
                    uow=uow,
                )
            )
            if course is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.TAUGHT_COURSE_ALREADY_EXISTS
                )

            await self._add_lecturer_course_taught_course(
                lecturer_id=lecturer_id,
                taught_course_data=taught_course_create,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception
