from abc import ABC

from uuid import UUID
from sqlalchemy import ColumnElement

from models.question import QuestionsOrm
from specification.base import SpecificationSQLAlchemy


class QuestionBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = QuestionsOrm


class QuestionIdSpecification(QuestionBaseSpecification):
    def __init__(self, id: UUID) -> None:
        super().__init__()
        self.id: UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class QuestionLecturerCourseIdSpecification(QuestionBaseSpecification):
    def __init__(self, lecturer_course_id: UUID) -> None:
        super().__init__()
        self.lecturer_course_id: UUID = lecturer_course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.lecturer_course_id == self.lecturer_course_id


class QuestionIsVisibleSpecification(QuestionBaseSpecification):
    def __init__(self, is_visible: bool) -> None:
        super().__init__()
        self.is_visible: bool = is_visible

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.is_visible == self.is_visible
