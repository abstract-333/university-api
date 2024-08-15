from uuid import UUID

from common.unit_of_work import IUnitOfWork
from exception.base import ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas.course_lecturer import CourseLecturerInDB
from schemas.pagination import Pagination
from schemas.question import (
    QuestionCreate,
    QuestionInDB,
    QuestionInDBExtended,
    QuestionUpdate,
)
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerIdSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.lecture import LectureLecturerCourseIdSpecification
from specification.question import (
    QuestionIdSpecification,
    QuestionLecturerCourseIdSpecification,
)
from specification.taught_course import TaughtCourseIdSpecification


class QuestionService:
    @classmethod
    async def _add_question(
        cls,
        question_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.question.add_question(question_data=question_data)
            await uow.commit()

    @classmethod
    async def _edit_question(
        cls,
        question_data: dict,
        question_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.question.edit_question(
                question_data=question_data,
                specification=QuestionIdSpecification(id=question_id),
            )
            await uow.commit()

    @classmethod
    async def _get_questions_by_lecturer_course_id(
        cls,
        lecturer_course_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuestionInDBExtended] | None:
        async with uow:
            return await uow.question.get_questions(
                specification=QuestionLecturerCourseIdSpecification(
                    lecturer_course_id=lecturer_course_id
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_questions_in_course(
        cls,
        taught_course_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuestionInDBExtended] | None:
        async with uow:
            return await uow.question.get_questions(
                specification=CourseLecturerCourseIDSpecification(
                    course_id=taught_course_id
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_question_by_id(
        cls,
        question_id: UUID,
        uow: IUnitOfWork,
    ) -> QuestionInDB | None:
        async with uow:
            return await uow.question.get_question(
                specification=QuestionIdSpecification(id=question_id)
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

    async def get_questions_by_lecturer(
        self,
        lecturer_course_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuestionInDBExtended] | None:
        """get questions by lecturer

        Args:
            lecturer_course_id (UUID):
            lecturer_id (UUID):
            uow (IUnitOfWork):
            pagination (Pagination):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:

        Returns:
            list[QuestionInDBExtended] | None:
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )
            return await self._get_questions_by_lecturer_course_id(
                lecturer_course_id=lecturer_course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def get_questions_in_course(
        self,
        lecturer_course_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuestionInDBExtended] | None:
        """get questions in course

        Args:
            lecturer_course_id (UUID):
            lecturer_id (UUID):
            uow (IUnitOfWork):
            pagination (Pagination):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:

        Returns:
            list[QuestionInDBExtended] | None:
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )
            return await self._get_questions_in_course(
                taught_course_id=course_lecturer.course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def add_question(
        self,
        question_create: QuestionCreate,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add question by lecturer

        Args:
            question_create (QuestionCreate):
            lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=question_create.lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )
            await self._add_question(
                question_data=question_create.model_dump(),
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def edit_question(
        self,
        question_update: QuestionUpdate,
        lecturer_id: UUID,
        question_id: UUID,
        lecturer_course_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """Edit question

        Args:
            question_update (QuestionUpdate):
            lecturer_id (UUID):
            question_id (UUID):
            lecturer_course_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )
            await self._edit_question(
                question_data=question_update.model_dump(
                    exclude_unset=True, exclude_none=True, exclude_defaults=True
                ),
                question_id=question_id,
                uow=uow,
            )

        except Exception as exception:
            raise exception
