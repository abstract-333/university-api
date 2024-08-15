from uuid import UUID

from common.unit_of_work import IUnitOfWork
from exception.base import ExceptionNotAcceptable406, ExceptionNotFound404
from exception.error_code import ErrorCode

from schemas.course_lecturer import CourseLecturerInDB
from schemas.enrolled_course import EnrolledCourseInDB
from schemas.pagination import Pagination
from schemas.quiz import QuizInDBExtended
from schemas.quiz_result import (
    QuizResultCreate,
    QuizResultInDB,
    QuizResultInDBExtended,
    QuizResultInDBQuizExtended,
)
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerIdSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.enrolled_course import (
    EnrolledCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
)
from specification.quiz import QuizActiveSpecification, QuizIdSpecification
from specification.quiz_result import (
    QuizResultEnrolledCourseIdSpecification,
    QuizResultQuizIdSpecification,
)


class QuizResultService:
    @classmethod
    async def _add_quiz_result(
        cls,
        quiz_result_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.quiz_result.add_quiz_result(quiz_result_data=quiz_result_data)
            await uow.commit()

    @classmethod
    async def _get_quiz_result(
        cls,
        quiz_id: UUID,
        enrolled_course_id: UUID,
        uow: IUnitOfWork,
    ) -> QuizResultInDB | None:
        async with uow:
            return await uow.quiz_result.get_quiz_result(
                specification=QuizResultQuizIdSpecification(quiz_id=quiz_id)
                & QuizResultEnrolledCourseIdSpecification(
                    enrolled_course_id=enrolled_course_id
                ),
            )

    @classmethod
    async def _get_quizzes_results_for_students(
        cls,
        enrolled_course_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuizResultInDB] | None:
        async with uow:
            return await uow.quiz_result.get_quizzes_results(
                specification=QuizResultEnrolledCourseIdSpecification(
                    enrolled_course_id=enrolled_course_id
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_quiz_results(
        cls,
        quiz_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuizResultInDBExtended] | None:
        async with uow:
            return await uow.quiz_result.get_quizzes_results_full_extended(
                specification=QuizResultQuizIdSpecification(quiz_id=quiz_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_quizzes_results_for_students_extended(
        cls,
        enrolled_course_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuizResultInDBQuizExtended] | None:
        async with uow:
            return await uow.quiz_result.get_quizzes_results_quiz_extended(
                specification=QuizResultEnrolledCourseIdSpecification(
                    enrolled_course_id=enrolled_course_id
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_quizzes_results_extended_for_student(
        cls,
        enrolled_course_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizResultInDBExtended] | None:
        async with uow:
            return await uow.quiz_result.get_quizzes_results_full_extended(
                specification=QuizResultEnrolledCourseIdSpecification(
                    enrolled_course_id=enrolled_course_id
                ),
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

    async def add_quiz_result(
        self,
        quiz_result_create: QuizResultCreate,
        student_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add quiz result

        Args:
            quiz_result_create (QuizResultCreate):
            student_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            ExceptionNotFound404: QUIZ_NOT_EXISTS
            ExceptionNotAcceptable406: RESULT_GREATER_THAN_QUIZ_MARKS
            ExceptionNotAcceptable406: QUIZ_RESULT_ALREADY_EXISTS
            exception:
        """
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=quiz_result_create.enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )

            if enrolled_course is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            quiz: QuizInDBExtended | None = await self._get_quiz(
                quiz_id=quiz_result_create.quiz_id,
                course_id=enrolled_course.taught_course_id,
                uow=uow,
            )

            if quiz is None:
                raise ExceptionNotFound404(detail=ErrorCode.QUIZ_NOT_EXISTS)

            if quiz.mark < quiz_result_create.result:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.RESULT_GREATER_THAN_QUIZ_MARKS
                )

            quiz_result: QuizResultInDB | None = await self._get_quiz_result(
                quiz_id=quiz_result_create.quiz_id,
                enrolled_course_id=quiz_result_create.enrolled_course_id,
                uow=uow,
            )
            if quiz_result is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.QUIZ_RESULT_ALREADY_EXISTS
                )

            await self._add_quiz_result(
                quiz_result_data=quiz_result_create.model_dump(),
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_quizzes_results_for_student(
        self,
        student_id: UUID,
        enrolled_course_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[QuizResultInDBQuizExtended] | None:
        """get quizzes results for student

        Args:
            student_id (UUID):
            enrolled_course_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            exception:

        Returns:
            list[QuizResultInDBExtended] | None:
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
            return await self._get_quizzes_results_for_students_extended(
                enrolled_course_id=enrolled_course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def get_quiz_results_by_lecturer(
        self,
        lecturer_id: UUID,
        quiz_id: UUID,
        course_lecturer_id: UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[QuizResultInDBExtended] | None:
        """Get quiz results for students (By Lecturer)

        Args:
            lecturer_id (UUID):
            quiz_id (UUID):
            course_lecturer_id (UUID):
            uow (IUnitOfWork):
            pagination (Pagination):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            ExceptionNotFound404: QUIZ_NOT_EXISTS
            exception:

        Returns:
            list[QuizResultInDBExtended] | None:
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

            return await self._get_quiz_results(
                quiz_id=quiz_id,
                uow=uow,
                pagination=pagination,
            )
        except Exception as exception:
            raise exception
