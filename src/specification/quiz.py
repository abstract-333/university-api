from abc import ABC
from uuid import UUID

from sqlalchemy import ColumnElement

from models.quiz import QuizzesOrm
from specification.base import SpecificationSQLAlchemy
from utils.seconds_unix import get_time


class QuizBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = QuizzesOrm


class QuizIdSpecification(QuizBaseSpecification):
    def __init__(self, id: UUID) -> None:
        super().__init__()
        self.id: UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class QuizLecturerCourseIdSpecification(QuizBaseSpecification):
    def __init__(self, lecturer_course_id: UUID) -> None:
        super().__init__()
        self.lecturer_course_id: UUID = lecturer_course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.lecturer_course_id == self.lecturer_course_id


class QuizActiveSpecification(QuizBaseSpecification):
    def __init__(self) -> None:
        super().__init__()

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.end_date > get_time()
