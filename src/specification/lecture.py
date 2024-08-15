import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.lecture import LecturesOrm
from specification.base import SpecificationSQLAlchemy


class LectureBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = LecturesOrm


class LectureIdSpecification(LectureBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class LectureLecturerCourseIdSpecification(LectureBaseSpecification):
    def __init__(self, lecturer_course_id: uuid.UUID) -> None:
        super().__init__()
        self.lecturer_course_id: uuid.UUID = lecturer_course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.lecturer_course_id == self.lecturer_course_id


class LectureFileIdSpecification(LectureBaseSpecification):
    def __init__(self, file_id: uuid.UUID) -> None:
        super().__init__()
        self.file_id: uuid.UUID = file_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.file_id == self.file_id
