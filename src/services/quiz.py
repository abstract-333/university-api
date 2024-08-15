from uuid import UUID

from common.unit_of_work import IUnitOfWork
from exception import ExceptionNotAcceptable406
from exception.base import ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas import QuestionInDBExtended
from schemas.course_lecturer import CourseLecturerInDB
from schemas.enrolled_course import EnrolledCourseInDB
from schemas.pagination import Pagination
from schemas.question import QuestionInDB
from schemas.quiz import QuizInDBExtended, QuizCreate
from specification import (
    QuizActiveSpecification,
    QuestionIsVisibleSpecification,
)
from specification.course_lecturer import (
    CourseLecturerIdSpecification,
    CourseLecturerLecturerIdSpecification,
    CourseLecturerCourseIDSpecification,
)
from specification.enrolled_course import (
    EnrolledCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
)
from specification.quiz import QuizIdSpecification, QuizLecturerCourseIdSpecification
from specification.taught_course import TaughtCourseIdSpecification


class QuizService:
    @classmethod
    async def _add_quiz(
        cls,
        quiz_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.quiz.add_quiz(quiz_data=quiz_data)
            await uow.commit()

    @classmethod
    async def _get_all_active_quizzes_taught_course(
        cls,
        taught_course_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        async with uow:
            return await uow.quiz.get_quizzes_extended(
                specification=TaughtCourseIdSpecification(id=taught_course_id)
                & QuizActiveSpecification(),
                pagination=pagination,
            )

    @classmethod
    async def _get_all_quizzes_taught_course(
        cls,
        taught_course_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        async with uow:
            return await uow.quiz.get_quizzes_extended(
                specification=TaughtCourseIdSpecification(id=taught_course_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_all_active_quizzes_for_student(
        cls,
        student_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        async with uow:
            return await uow.quiz.get_quizzes_extended_for_student(
                specification=EnrolledCourseStudentIdSpecification(
                    student_id=student_id
                )
                & QuizActiveSpecification(),
                pagination=pagination,
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
    async def _get_questions_course(
        cls,
        taught_course_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuestionInDBExtended] | None:
        async with uow:
            return await uow.question.get_questions(
                specification=CourseLecturerCourseIDSpecification(
                    course_id=taught_course_id
                )
                & QuestionIsVisibleSpecification(is_visible=True),
                pagination=pagination,
            )

    @classmethod
    async def _get_questions_for_quiz(
        cls,
        count_of_questions: int,
        course_id: UUID,
        uow: IUnitOfWork,
    ) -> list[QuestionInDB] | None:
        async with uow:
            return await uow.question.get_questions_for_quiz(
                specification=QuestionIsVisibleSpecification(is_visible=True)
                & CourseLecturerCourseIDSpecification(course_id=course_id),
                limit=count_of_questions,
            )

    @classmethod
    async def _get_quiz(
        cls,
        quiz_id: UUID,
        course_id: UUID,
        uow: IUnitOfWork,
    ) -> QuizInDBExtended | None:
        async with uow:
            return await uow.quiz.get_quiz_extended(
                specification=QuizActiveSpecification()
                & QuizIdSpecification(id=quiz_id)
                & CourseLecturerCourseIDSpecification(course_id=course_id)
            )

    @classmethod
    async def _delete_quiz(
        cls,
        quiz_id: UUID,
        course_lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.quiz.delete_quiz(
                specification=QuizActiveSpecification()
                & QuizIdSpecification(id=quiz_id)
                & QuizLecturerCourseIdSpecification(
                    lecturer_course_id=course_lecturer_id
                )
            )
            await uow.commit()

    async def get_active_quizzes_for_course_by_student(
        self,
        student_id: UUID,
        enrolled_course_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        """Get active quizzes for course (student)

        Args:
            student_id (UUID):
            enrolled_course_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            exception:

        Returns:
            list[QuizInDBExtended] | None
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

            return await self._get_all_active_quizzes_taught_course(
                uow=uow,
                pagination=pagination,
                taught_course_id=enrolled_course.taught_course_id,
            )

        except Exception as exception:
            raise exception

    async def get_all_active_quizzes_student(
        self,
        student_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        """Get all active quizzes for student

        Args:
            student_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            exception:

        Returns:
            list[QuizInDBExtended] | None
        """
        try:
            return await self._get_all_active_quizzes_for_student(
                student_id=student_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def get_active_quizzes_for_course_by_lecturer(
        self,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        """Get all active quizzes for course (Lecturer)

        Args:
            course_lecturer_id (UUID):
            lecturer_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:

        Returns:
            list[QuizInDBExtended] | None:
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
            return await self._get_all_active_quizzes_taught_course(
                taught_course_id=course_lecturer.course_id,
                pagination=pagination,
                uow=uow,
            )
        except Exception as exception:
            raise exception

    async def get_all_quizzes_for_course_by_lecturer(
        self,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizInDBExtended] | None:
        """Get all  quizzes for course (Lecturer)

        Args:
            course_lecturer_id (UUID):
            lecturer_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:

        Returns:
            list[QuizInDBExtended] | None:
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
            return await self._get_all_quizzes_taught_course(
                taught_course_id=course_lecturer.course_id,
                pagination=pagination,
                uow=uow,
            )
        except Exception as exception:
            raise exception

    async def add_quiz(
        self,
        quiz_create: QuizCreate,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add quiz by lecturer

        Args:
            quiz_create (QuizCreate):
            lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            ExceptionNotAcceptable406: NOT_ENOUGH_QUESTIONS
            exception:
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=quiz_create.lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )
            questions: list[
                QuestionInDBExtended
            ] | None = await self._get_questions_course(
                taught_course_id=course_lecturer.course_id,
                uow=uow,
                pagination=Pagination(limit=30, offset=0),
            )
            if questions is not None:
                if len(questions) < quiz_create.number_of_questions:
                    raise ExceptionNotAcceptable406(
                        detail=ErrorCode.NOT_ENOUGH_QUESTIONS
                    )
            await self._add_quiz(
                quiz_data=quiz_create.model_dump(),
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def take_quiz(
        self,
        quiz_id: UUID,
        student_id: UUID,
        enrolled_course_id: UUID,
        uow: IUnitOfWork,
    ) -> list[QuestionInDB] | None:
        """take quiz for student

        Args:
            quiz_id (UUID):
            student_id (UUID):
            enrolled_course_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            ExceptionNotFound404: QUIZ_NOT_EXISTS
            exception:

        Returns:
            list[QuestionInDB] | None:
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
            quiz: QuizInDBExtended | None = await self._get_quiz(
                quiz_id=quiz_id,
                course_id=enrolled_course.taught_course_id,
                uow=uow,
            )
            if quiz is None:
                raise ExceptionNotFound404(detail=ErrorCode.QUIZ_NOT_EXISTS)

            return await self._get_questions_for_quiz(
                count_of_questions=quiz.number_of_questions,
                course_id=quiz.lecturer_course.course.id,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def delete_quiz(
        self,
        quiz_id: UUID,
        lecturer_id: UUID,
        course_lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """delete quiz by lecturer

        Args:
            quiz_id (UUID):
            lecturer_id (UUID):
            course_lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            ExceptionNotFound404: QUIZ_NOT_EXISTS
            exception:Otherwise
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
            quiz: QuizInDBExtended | None = await self._get_quiz(
                quiz_id=quiz_id,
                course_id=course_lecturer.course_id,
                uow=uow,
            )
            if quiz is None:
                raise ExceptionNotFound404(detail=ErrorCode.QUIZ_NOT_EXISTS)

            await self._delete_quiz(
                quiz_id=quiz.id,
                course_lecturer_id=course_lecturer.id,
                uow=uow,
            )
        except Exception as exception:
            raise exception
