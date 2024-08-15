import uuid

from common.unit_of_work import IUnitOfWork
from exception.base import (
    ExceptionMethodNotAllowed405,
    ExceptionNotAcceptable406,
    ExceptionNotFound404,
)
from exception.error_code import ErrorCode
from schemas.course_lecturer import CourseLecturerInDB
from schemas.pagination import Pagination
from schemas.speciality_course import SpecialityCourseInDB
from schemas.taught_course import (
    TaughtCourseCreate,
    TaughtCourseInDB,
    TaughtCourseInDBExtended,
    TaughtCourseUpdate,
)
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.speciality import (
    SpecialityFacultySpecification,
)
from specification.speciality_course import (
    SpecialityCourseClassSpecification,
    SpecialityCourseIdSpecification,
    SpecialityCourseSemesterSpecification,
    SpecialityCourseSpecialityIdSpecification,
)
from specification.taught_course import (
    TaughtCourseIdSpecification,
    TaughtCourseSpecialityCourseIDSpecification,
    TaughtCourseYearSpecification,
)


class TaughtCourseService:
    @classmethod
    async def _get_taught_courses_by_faculty_name(
        cls,
        uow: IUnitOfWork,
        faculty_name: str,
        year: int,
        pagination: Pagination,
    ) -> list[TaughtCourseInDBExtended] | None:
        """Get taught_courses joined with speciality_courses by faculty_name"""
        async with uow:
            taught_courses: list[
                TaughtCourseInDBExtended
            ] | None = await uow.taught_course.get_taught_courses_with_speciality(
                specification=SpecialityFacultySpecification(faculty_name=faculty_name)
                & TaughtCourseYearSpecification(year=year),
                pagination=pagination,
            )
            return taught_courses

    @classmethod
    async def _get_taught_courses_by_speciality(
        cls,
        uow: IUnitOfWork,
        speciality_id: uuid.UUID,
        current_class: int,
        semester: int,
        year: int,
        pagination: Pagination,
    ) -> list[TaughtCourseInDBExtended] | None:
        """Get taught_courses joined with speciality_courses by (speciality_id, current_class, semester)"""
        async with uow:
            taught_courses: list[
                TaughtCourseInDBExtended
            ] | None = await uow.taught_course.get_taught_courses_with_speciality(
                specification=SpecialityCourseSpecialityIdSpecification(
                    speciality_id=speciality_id
                )
                & SpecialityCourseClassSpecification(current_class=current_class)
                & SpecialityCourseSemesterSpecification(semester=semester)
                & TaughtCourseYearSpecification(year=year),
                pagination=pagination,
            )
            return taught_courses

    @classmethod
    async def _get_taught_course_joined_by_speciality_course(
        cls,
        speciality_course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> TaughtCourseInDBExtended | None:
        """Get taught_course joined by speciality_course"""
        async with uow:
            taught_course: TaughtCourseInDBExtended | None = (
                await uow.taught_course.get_taught_course_joined(
                    specification=TaughtCourseSpecialityCourseIDSpecification(
                        speciality_course_id=speciality_course_id
                    ),
                )
            )
            return taught_course

    @classmethod
    async def _get_taught_course_by_speciality_course(
        cls,
        speciality_course_id: uuid.UUID,
        year: int,
        uow: IUnitOfWork,
    ) -> TaughtCourseInDB | None:
        """Get taught_course by speciality_course"""
        async with uow:
            taught_course: TaughtCourseInDB | None = (
                await uow.taught_course.get_taught_course(
                    specification=TaughtCourseSpecialityCourseIDSpecification(
                        speciality_course_id=speciality_course_id
                    )
                    & TaughtCourseYearSpecification(year=year),
                )
            )
            return taught_course

    @classmethod
    async def _get_taught_course_by_id(
        cls,
        id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> TaughtCourseInDB | None:
        """Get taught_course by id"""
        async with uow:
            return await uow.taught_course.get_taught_course(
                specification=TaughtCourseIdSpecification(id=id),
            )

    @classmethod
    async def _get_course_lecturer_by_lecturer(
        cls,
        lecturer_id: uuid.UUID,
        taught_course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseLecturerInDB | None:
        """Get course lecturer by id"""
        async with uow:
            return await uow.course_lecturer.get_course_lecturer(
                specification=CourseLecturerLecturerIdSpecification(
                    lecturer_id=lecturer_id
                )
                & CourseLecturerCourseIDSpecification(course_id=taught_course_id),
            )

    @classmethod
    async def _get_speciality_course_by_id(
        cls,
        id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> SpecialityCourseInDB | None:
        """Get speciality_course by id"""
        async with uow:
            speciality_course: SpecialityCourseInDB | None = (
                await uow.speciality_course.get_speciality_course(
                    specification=SpecialityCourseIdSpecification(id=id),
                )
            )
            return speciality_course

    @classmethod
    async def _add_taugth_course(
        cls,
        taught_course_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        """Add new taught_course record to db"""
        async with uow:
            await uow.taught_course.add_taught_course(
                taught_course_data=taught_course_data
            )
            await uow.commit()

    @classmethod
    async def _edit_taught_course_by_id(
        cls,
        id: uuid.UUID,
        taught_course_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.taught_course.edit_taught_course(
                taught_course_data=taught_course_data,
                specification=TaughtCourseIdSpecification(id=id),
            )
            await uow.commit()

    async def get_taught_courses_by_faculty(
        self,
        faculty_name: str,
        year: int,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[TaughtCourseInDBExtended] | None:
        try:
            return await self._get_taught_courses_by_faculty_name(
                faculty_name=faculty_name,
                year=year,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_current_taught_course(
        self,
        speciality_course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> TaughtCourseInDBExtended | None:
        try:
            taught_course: TaughtCourseInDBExtended | None = (
                await self._get_taught_course_joined_by_speciality_course(
                    speciality_course_id=speciality_course_id,
                    uow=uow,
                )
            )
            return taught_course

        except Exception as exception:
            raise exception

    async def get_taught_courses_by_speciality(
        self,
        speciality_id: uuid.UUID,
        current_class: int,
        semester: int,
        year: int,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[TaughtCourseInDBExtended] | None:
        try:
            taught_courses: list[
                TaughtCourseInDBExtended
            ] | None = await self._get_taught_courses_by_speciality(
                speciality_id=speciality_id,
                semester=semester,
                current_class=current_class,
                year=year,
                uow=uow,
                pagination=pagination,
            )
            return taught_courses

        except Exception as exception:
            raise exception

    async def add_taught_course(
        self,
        taught_course_create: TaughtCourseCreate,
        uow: IUnitOfWork,
    ) -> None:
        try:
            speciality_course: SpecialityCourseInDB | None = (
                await self._get_speciality_course_by_id(
                    id=taught_course_create.speciality_course_id,
                    uow=uow,
                )
            )

            if speciality_course is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.SPECIALITY_COURSE_NOT_EXISTS
                )

            old_taught_course: TaughtCourseInDB | None = (
                await self._get_taught_course_by_speciality_course(
                    speciality_course_id=taught_course_create.speciality_course_id,
                    year=taught_course_create.year,
                    uow=uow,
                )
            )

            if old_taught_course is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.TAUGHT_COURSE_ALREADY_EXISTS
                )

            await self._add_taugth_course(
                taught_course_data=taught_course_create.model_dump(),
                uow=uow,
            )
            return None

        except Exception as exception:
            raise exception

    async def edit_taught_course(
        self,
        taught_course_update: TaughtCourseUpdate,
        taught_course_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> TaughtCourseUpdate:
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer_by_lecturer(
                    lecturer_id=lecturer_id,
                    taught_course_id=taught_course_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            await self._edit_taught_course_by_id(
                taught_course_data=taught_course_update.model_dump(
                    exclude_unset=True,
                    exclude_none=True,
                    exclude_defaults=True,
                ),
                id=taught_course_id,
                uow=uow,
            )
            return taught_course_update

        except Exception as exception:
            raise exception
