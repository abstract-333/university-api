import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.lecturer import LecturersOrm
from specification.base import SpecificationSQLAlchemy


class LecturerBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = LecturersOrm


class LecturerUserIdSpecification(LecturerBaseSpecification):
    def __init__(self, user_id: uuid.UUID) -> None:
        super().__init__()
        self.user_id: uuid.UUID = user_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.user_id == self.user_id


class LecturerFacultySpecification(LecturerBaseSpecification):
    def __init__(self, faculty_name: str) -> None:
        super().__init__()
        self.faculty_name: str = faculty_name

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.faculty_name == self.faculty_name


class LecturerIdSpecification(LecturerBaseSpecification):
    def __init__(self, lecturer_id: uuid.UUID) -> None:
        super().__init__()
        self.lecturer_id: uuid.UUID = lecturer_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.lecturer_id


class LecturerIsApprovedSpecification(LecturerBaseSpecification):
    def __init__(self) -> None:
        super().__init__()

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.is_approved == True
