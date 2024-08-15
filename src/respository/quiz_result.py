from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.course_lecturer import CoursesLecturersOrm
from models.enrolled_course import EnrolledCoursesOrm
from models.quiz import QuizzesOrm
from models.quiz_result import QuizzesResultsOrm
from models.speciality_course import SpecialityCoursesOrm
from models.student import StudentsOrm
from models.taught_courses import TaughtCoursesOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from schemas.pagination import Pagination
from schemas.quiz import QuizInDBExtended
from schemas.quiz_result import (
    QuizResultInDB,
    QuizResultInDBExtended,
    QuizResultInDBQuizExtended,
)
from specification.base import Specification


class QuizResultBaseRepository(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_quiz_result(
        self,
        quiz_result_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def get_quiz_result(
        self,
        specification: Specification,
    ) -> QuizResultInDB | None:
        ...

    @abstractmethod
    async def get_quizzes_results(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizResultInDB] | None:
        ...

    @abstractmethod
    async def get_quizzes_results_quiz_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizResultInDBQuizExtended] | None:
        ...

    @abstractmethod
    async def get_quizzes_results_full_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizResultInDBExtended] | None:
        ...


class QuizResultRepository(QuizResultBaseRepository, SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[QuizzesResultsOrm] = QuizzesResultsOrm
        super().__init__(session=session)

    async def add_quiz_result(self, quiz_result_data: dict) -> None:
        await self.add_one(data=quiz_result_data)

    async def get_quizzes_results(
        self, specification: Specification, pagination: Pagination = Pagination()
    ) -> list[QuizResultInDB] | None:
        return await self.find_by(
            arguments=specification.is_satisfied_by(),
            schema=QuizResultInDB,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_quizzes_results_quiz_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizResultInDBQuizExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.quiz)
            .joinedload(QuizzesOrm.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            arguments=specification.is_satisfied_by(),
            schema=QuizResultInDBQuizExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_quiz_result(
        self, specification: Specification
    ) -> QuizResultInDB | None:
        return await self.find_one(
            arguments=specification.is_satisfied_by(),
            schema=QuizResultInDB,
        )

    async def get_quizzes_results_full_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizResultInDBExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.quiz)
            .joinedload(QuizzesOrm.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            joinedload(self.model_cls.enrolled_course)
            .joinedload(EnrolledCoursesOrm.student)
            .joinedload(StudentsOrm.user),
            join_conditions=(QuizzesOrm,),
            arguments=specification.is_satisfied_by(),
            schema=QuizResultInDBExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )
