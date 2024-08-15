from uuid import UUID

from common.unit_of_work import IUnitOfWork
from dependencies.dependencies import StorageDep
from exception.base import ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas.course_lecturer import CourseLecturerInDB
from schemas.enrolled_course import EnrolledCourseInDB
from schemas.file import FileInDB
from schemas.lecture import LectureCreate, LectureInDBExtended
from schemas.pagination import Pagination
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerIdSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.enrolled_course import (
    EnrolledCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
)
from specification.file import FileIdSpecification
from specification.lecture import LectureIdSpecification


class LectureService:
    @classmethod
    async def _get_lectures(
        cls,
        course_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[LectureInDBExtended] | None:
        async with uow:
            return await uow.lecture.get_lectures(
                specification=CourseLecturerCourseIDSpecification(course_id=course_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_lecture_detailed(
        cls,
        lecture_id: UUID,
        uow: IUnitOfWork,
    ) -> LectureInDBExtended | None:
        async with uow:
            return await uow.lecture.get_lecture(
                specification=LectureIdSpecification(id=lecture_id),
            )

    @classmethod
    async def _add_lecture(
        cls,
        lecture_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.lecture.add_lecture(lecture_data=lecture_data)
            await uow.commit()

    @classmethod
    async def _get_file(
        cls,
        file_id: UUID,
        uow: IUnitOfWork,
    ) -> FileInDB | None:
        async with uow:
            return await uow.file.get_file(
                specification=FileIdSpecification(id=file_id)
            )

    @classmethod
    async def _get_course_lecturer(
        cls,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> CourseLecturerInDB | None:
        async with uow:
            return await uow.course_lecturer.get_course_lecturer(
                specification=CourseLecturerLecturerIdSpecification(
                    lecturer_id=lecturer_id
                )
                & CourseLecturerIdSpecification(id=course_lecturer_id)
            )

    @classmethod
    async def _get_enrolled_course(
        cls,
        enrolled_course_id: UUID,
        student_id: UUID,
        uow: IUnitOfWork,
    ) -> EnrolledCourseInDB | None:
        async with uow:
            enrolled_course: EnrolledCourseInDB | None = (
                await uow.enrolled_course.get_enrolled_course(
                    specification=EnrolledCourseIdSpecification(id=enrolled_course_id)
                    & EnrolledCourseStudentIdSpecification(student_id=student_id)
                )
            )
            return enrolled_course

    @classmethod
    async def _delete_lecture(
        cls,
        lecture_id: UUID,
        file_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.file.delete_file(specification=FileIdSpecification(id=file_id))
            await uow.lecture.delete_lecture(
                specification=LectureIdSpecification(id=lecture_id)
            )
            await uow.commit()

    async def get_lectures_for_lecturer(
        self,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[LectureInDBExtended] | None:
        """get lectures for lecturer

        Args:
            course_lecturer_id (UUID):
            lecturer_id (UUID):
            uow (IUnitOfWork):
            pagination (Pagination):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception: _description_

        Returns:
            list[LectureInDBExtended] | None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_lectures(
                course_id=course_lecturer.course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def get_lectures_for_student(
        self,
        enrolled_course_id: UUID,
        student_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[LectureInDBExtended] | None:
        """get lectures for student

        Args:
            enrolled_course_id (UUID):
            student_id (UUID):
            uow (IUnitOfWork):
            pagination (Pagination):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            exception:

        Returns:
            list[LectureInDBExtended] | None
        """
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )
            if enrolled_course is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            return await self._get_lectures(
                course_id=enrolled_course.taught_course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def add_lecture(
        self,
        lecture_create: LectureCreate,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add lecture

        Args:
            lecture_create (LectureCreate):
            lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: FILE_NOT_FOUND
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception: None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=lecture_create.lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            file: FileInDB | None = await self._get_file(
                file_id=lecture_create.file_id, uow=uow
            )
            if file is None:
                raise ExceptionNotFound404(detail=ErrorCode.FILE_NOT_FOUND)

            await self._add_lecture(lecture_data=lecture_create.model_dump(), uow=uow)

        except Exception as exception:
            raise exception

    async def delete_lecture(
        self,
        lecture_id: UUID,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
        storage: StorageDep,
    ) -> None:
        """delete lecture

        Args:
            lecture_id (UUID):
            course_lecturer_id (UUID):
            lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            ExceptionNotFound404: LECTURE_NOT_EXISTS
            exception:

        Returns:
            _type_: None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            lecture: LectureInDBExtended | None = await self._get_lecture_detailed(
                lecture_id=lecture_id,
                uow=uow,
            )

            if lecture is None:
                raise ExceptionNotFound404(detail=ErrorCode.LECTURE_NOT_EXISTS)

            await self._delete_lecture(
                lecture_id=lecture_id,
                file_id=lecture.file.id,
                uow=uow,
            )
            await storage.delete_file(file_name=lecture.file.file_id)

        except Exception as exception:
            raise exception
