import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.taught_courses import TaughtCoursesOrm
from specification.base import SpecificationSQLAlchemy


class TaughtCourseBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = TaughtCoursesOrm


class TaughtCourseYearSpecification(TaughtCourseBaseSpecification):
    def __init__(self, year: int) -> None:
        super().__init__()
        self.year: int = year

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.year == self.year


class TaughtCourseSpecialityCourseIDSpecification(TaughtCourseBaseSpecification):
    def __init__(self, speciality_course_id: uuid.UUID) -> None:
        super().__init__()
        self.speciality_course_id: uuid.UUID = speciality_course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.speciality_course_id == self.speciality_course_id


class TaughtCourseIdSpecification(TaughtCourseBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
