from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.course_lecturer import CoursesLecturersOrm
from models.enrolled_course import EnrolledCoursesOrm
from models.quiz import QuizzesOrm
from models.speciality import SpecialitiesOrm
from models.speciality_course import SpecialityCoursesOrm
from models.taught_courses import TaughtCoursesOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from schemas.pagination import Pagination
from schemas.quiz import QuizInDB, QuizInDBExtended
from specification.base import Specification


class QuizBaseRepository(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_quiz(
        self,
        quiz_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def get_quiz(
        self,
        specification: Specification,
    ) -> QuizInDB | None:
        ...

    @abstractmethod
    async def get_quizzes(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizInDB] | None:
        ...

    @abstractmethod
    async def get_quiz_extended(
        self,
        specification: Specification,
    ) -> QuizInDBExtended | None:
        ...

    @abstractmethod
    async def get_quizzes_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizInDBExtended] | None:
        ...

    @abstractmethod
    async def get_quizzes_extended_for_student(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizInDBExtended] | None:
        ...

    @abstractmethod
    async def delete_quiz(
        self,
        specification: Specification,
    ) -> None:
        ...


class QuizRepository(QuizBaseRepository, SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[QuizzesOrm] = QuizzesOrm
        super().__init__(session=session)

    async def add_quiz(
        self,
        quiz_data: dict,
    ) -> None:
        await self.add_one(data=quiz_data)

    async def get_quiz(
        self,
        specification: Specification,
    ) -> QuizInDB | None:
        return await self.find_one(
            schema=QuizInDB,
            arguments=specification.is_satisfied_by(),
        )

    async def get_quizzes(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizInDB] | None:
        return await self.find_by(
            schema=QuizInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_quiz_extended(
        self,
        specification: Specification,
    ) -> QuizInDBExtended | None:
        return await self.find_one(
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            join_conditions=(
                CoursesLecturersOrm,
                TaughtCoursesOrm,
            ),
            arguments=specification.is_satisfied_by(),
            schema=QuizInDBExtended,
        )

    async def get_quizzes_extended_for_student(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizInDBExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .selectinload(TaughtCoursesOrm.enrolled_courses),
            join_conditions=(
                CoursesLecturersOrm,
                TaughtCoursesOrm,
                EnrolledCoursesOrm,
            ),
            arguments=specification.is_satisfied_by(),
            schema=QuizInDBExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_quizzes_extended(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuizInDBExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            join_conditions=(
                CoursesLecturersOrm,
                TaughtCoursesOrm,
            ),
            arguments=specification.is_satisfied_by(),
            schema=QuizInDBExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def delete_quiz(self, specification: Specification) -> None:
        await self.delete_one(
            arguments=specification.is_satisfied_by(),
        )
