import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.course_lecturer import CoursesLecturersOrm
from specification.base import SpecificationSQLAlchemy


class CourseLecturerBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = CoursesLecturersOrm


class CourseLecturerCourseIDSpecification(CourseLecturerBaseSpecification):
    def __init__(self, course_id: uuid.UUID) -> None:
        super().__init__()
        self.course_id: uuid.UUID = course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.course_id == self.course_id


class CourseLecturerLecturerIdSpecification(CourseLecturerBaseSpecification):
    def __init__(self, lecturer_id: uuid.UUID) -> None:
        super().__init__()
        self.lecturer_id: uuid.UUID = lecturer_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.lecturer_id == self.lecturer_id


class CourseLecturerIdSpecification(CourseLecturerBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
