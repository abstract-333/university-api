import uuid
from abc import ABC
from typing import Literal

from pydantic import NonNegativeInt
from sqlalchemy import ColumnElement

from models.speciality_course import SpecialityCoursesOrm
from specification.base import SpecificationSQLAlchemy


class SpecialityCourseBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = SpecialityCoursesOrm


class SpecialityCourseSemesterSpecification(SpecialityCourseBaseSpecification):
    def __init__(self, semester: Literal[1, 2]) -> None:
        super().__init__()
        self.semester: Literal[1, 2] = semester

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.semester == self.semester


class SpecialityCourseClassSpecification(SpecialityCourseBaseSpecification):
    def __init__(self, current_class: NonNegativeInt) -> None:
        super().__init__()
        self.current_class: int = current_class

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.current_class == self.current_class


class SpecialityCourseNameSpecification(SpecialityCourseBaseSpecification):
    def __init__(self, course_name: str) -> None:
        super().__init__()
        self.course_name: str = course_name

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.course_name == self.course_name


class SpecialityCourseSpecialityIdSpecification(SpecialityCourseBaseSpecification):
    def __init__(self, speciality_id: uuid.UUID) -> None:
        super().__init__()
        self.speciality_id: uuid.UUID = speciality_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.speciality_id == self.speciality_id


class SpecialityCourseIdSpecification(SpecialityCourseBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
