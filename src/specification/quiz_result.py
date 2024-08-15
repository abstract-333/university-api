from abc import ABC
from uuid import UUID

from sqlalchemy import ColumnElement

from models.quiz_result import QuizzesResultsOrm
from specification.base import SpecificationSQLAlchemy


class QuizResultBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = QuizzesResultsOrm


class QuizResultIdSpecification(QuizResultBaseSpecification):
    def __init__(self, id: UUID) -> None:
        super().__init__()
        self.id: UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class QuizResultQuizIdSpecification(QuizResultBaseSpecification):
    def __init__(self, quiz_id: UUID) -> None:
        super().__init__()
        self.quiz_id: UUID = quiz_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.quiz_id == self.quiz_id


class QuizResultEnrolledCourseIdSpecification(QuizResultBaseSpecification):
    def __init__(self, enrolled_course_id: UUID) -> None:
        super().__init__()
        self.enrolled_course_id: UUID = enrolled_course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.enrolled_course_id == self.enrolled_course_id
