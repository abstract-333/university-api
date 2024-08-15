from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    ColumnExpressionArgument,
    Delete,
    Insert,
    Result,
    ScalarResult,
    Select,
    Update,
    func,
    insert,
    select,
    update,
    delete,
)
from models.base import BaseModelORM
from models.course_lecturer import CoursesLecturersOrm
from models.question import QuestionsOrm
from models.speciality_course import SpecialityCoursesOrm
from models.taught_courses import TaughtCoursesOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from schemas.pagination import Pagination
from schemas.question import QuestionInDB, QuestionInDBExtended
from specification.base import Specification
from sqlalchemy.orm import joinedload, selectinload


class QuestionsRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_questions(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuestionInDBExtended] | None:
        ...

    @abstractmethod
    async def get_question(
        self,
        specification: Specification,
    ) -> QuestionInDB | None:
        ...

    @abstractmethod
    async def get_questions_for_quiz(
        self,
        specification: Specification,
        limit: int,
    ) -> list[QuestionInDB] | None:
        ...

    @abstractmethod
    async def add_question(
        self,
        question_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_question(
        self,
        question_data: dict,
        specification: Specification,
    ) -> None:
        ...


class QuestionRepository(SQLAlchemyRepository, QuestionsRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[QuestionsOrm] = QuestionsOrm
        super().__init__(session=session)

    async def get_questions(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[QuestionInDBExtended] | None:
        questions: list[QuestionInDBExtended] | None = await self.find_by(
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            join_conditions=(self.model_cls.lecturer_course,),
            arguments=specification.is_satisfied_by(),
            schema=QuestionInDBExtended,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return questions

    async def get_questions_for_quiz(
        self,
        specification: Specification,
        limit: int,
    ) -> list[QuestionInDB] | None:
        query: Select[tuple[BaseModelORM]] = select(self.model_cls)

        query = (
            query.join(self.model_cls.lecturer_course)
            .filter(specification.is_satisfied_by())
            .order_by(func.random())
            .limit(limit=limit)
        )

        query_result: Result[tuple[BaseModelORM]] = await self.session.execute(
            statement=query
        )
        scalar_result: ScalarResult[BaseModelORM] = query_result.scalars()

        if not scalar_result:
            return None

        result: list[QuestionInDB] = [
            element.to_read_model(schema=QuestionInDB)
            for element in scalar_result.all()
        ]

        if not result:
            return None

        return result

    async def get_question(
        self,
        specification: Specification,
    ) -> QuestionInDB | None:
        return await self.find_one(
            arguments=specification.is_satisfied_by(),
            schema=QuestionInDB,
        )

    async def add_question(
        self,
        question_data: dict,
    ) -> None:
        await self.add_one(
            data=question_data,
        )

    async def edit_question(
        self,
        question_data: dict,
        specification: Specification,
    ) -> None:
        return await self.edit_one(
            arguments=specification.is_satisfied_by(),
            data=question_data,
        )
