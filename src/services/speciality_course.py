import uuid
from common.unit_of_work import IUnitOfWork
from schemas.pagination import Pagination
from schemas.speciality_course import SpecialityCourseInDB
from specification.speciality import SpecialityFacultySpecification
from specification.speciality_course import (
    SpecialityCourseClassSpecification,
    SpecialityCourseSemesterSpecification,
    SpecialityCourseSpecialityIdSpecification,
)


class SpecialityCourseService:
    @classmethod
    async def _get_speciality_courses_by_faculty(
        cls,
        uow: IUnitOfWork,
        faculty_name: str,
        current_class: int,
        semester: int,
        pagination: Pagination,
    ) -> list[SpecialityCourseInDB] | None:
        """Get speciality courses by (faculty_name, current_class, semester)"""
        async with uow:
            speciality_courses: list[
                SpecialityCourseInDB
            ] | None = await uow.speciality_course.get_speciality_courses(
                specification=SpecialityFacultySpecification(faculty_name=faculty_name)
                & SpecialityCourseClassSpecification(current_class=current_class)
                & SpecialityCourseSemesterSpecification(semester=semester),
                pagination=pagination,
            )
            return speciality_courses

    @classmethod
    async def _get_speciality_courses_by_speciality(
        cls,
        uow: IUnitOfWork,
        speciality_id: uuid.UUID,
        pagination: Pagination,
    ) -> list[SpecialityCourseInDB] | None:
        """Get speciality courses by speciality_id"""
        async with uow:
            speciality_course: list[
                SpecialityCourseInDB
            ] | None = await uow.speciality_course.get_speciality_courses(
                specification=SpecialityCourseSpecialityIdSpecification(
                    speciality_id=speciality_id
                ),
                pagination=pagination,
            )
            return speciality_course

    @classmethod
    async def _get_speciality_courses_by_speciality_arguments(
        cls,
        speciality_id: uuid.UUID,
        current_class: int,
        semester: int,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[SpecialityCourseInDB] | None:
        """Get speciality courses by (speciality_id, current_class, semester)"""
        async with uow:
            speciality_course: list[
                SpecialityCourseInDB
            ] | None = await uow.speciality_course.get_speciality_courses(
                specification=SpecialityCourseClassSpecification(
                    current_class=current_class
                )
                & SpecialityCourseSpecialityIdSpecification(speciality_id=speciality_id)
                & SpecialityCourseSemesterSpecification(semester=semester),
                pagination=pagination,
            )
            return speciality_course

    async def get_speciality_courses_by_specific_speciality(
        self,
        speciality_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[SpecialityCourseInDB] | None:
        try:
            speciality_courses: list[
                SpecialityCourseInDB
            ] | None = await self._get_speciality_courses_by_speciality(
                speciality_id=speciality_id,
                uow=uow,
                pagination=pagination,
            )
            return speciality_courses

        except Exception as exception:
            raise exception

    async def get_speciality_courses_by_faculty(
        self,
        faculty_name: str,
        current_class: int,
        semester: int,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[SpecialityCourseInDB] | None:
        try:
            return await self._get_speciality_courses_by_faculty(
                faculty_name=faculty_name,
                current_class=current_class,
                semester=semester,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_speciality_courses_by_speciality(
        self,
        speciality_id: uuid.UUID,
        current_class: int,
        semester: int,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[SpecialityCourseInDB] | None:
        try:
            return await self._get_speciality_courses_by_speciality_arguments(
                speciality_id=speciality_id,
                current_class=current_class,
                semester=semester,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception
