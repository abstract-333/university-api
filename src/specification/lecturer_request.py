import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.lecturer_request import LecturersRequestsOrm
from specification.base import SpecificationSQLAlchemy


class LecturerRequestBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = LecturersRequestsOrm


class LecturerRequestUserIdSpecification(LecturerRequestBaseSpecification):
    def __init__(self, user_id: uuid.UUID) -> None:
        super().__init__()
        self.user_id: uuid.UUID = user_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.user_id == self.user_id


class LecturerRequestIsProcessedSpecification(LecturerRequestBaseSpecification):
    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.processed_at != None


class LecturerRequestIsAcceptedSpecification(LecturerRequestBaseSpecification):
    def __init__(self, is_accepted: bool) -> None:
        super().__init__()
        self.is_accepted: bool = is_accepted

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.is_accepted == self.is_accepted


class LecturerRequestIdSpecification(LecturerRequestBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class LecturerRequestFacultySpecification(LecturerRequestBaseSpecification):
    def __init__(self, faculty_name: str) -> None:
        super().__init__()
        self.faculty_name: str = faculty_name

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.faculty_name == self.faculty_name
