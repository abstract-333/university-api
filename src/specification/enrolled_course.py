import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.enrolled_course import EnrolledCoursesOrm
from specification.base import SpecificationSQLAlchemy


class EnrolledCourseBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = EnrolledCoursesOrm


class EnrolledCourseStudentIdSpecification(EnrolledCourseBaseSpecification):
    def __init__(self, student_id: uuid.UUID) -> None:
        super().__init__()
        self.student_id: uuid.UUID = student_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.student_id == self.student_id


class EnrolledCourseCourseIdSpecification(EnrolledCourseBaseSpecification):
    def __init__(self, course_id: uuid.UUID) -> None:
        super().__init__()
        self.course_id: uuid.UUID = course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.taught_course_id == self.course_id


class EnrolledCourseIdSpecification(EnrolledCourseBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
