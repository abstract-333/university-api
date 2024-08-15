import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models import SpecialitiesOrm
from specification.base import SpecificationSQLAlchemy


class SpecialityBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = SpecialitiesOrm


class SpecialityNameSpecification(SpecialityBaseSpecification):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.name == self.name


class SpecialityFacultySpecification(SpecialityBaseSpecification):
    def __init__(self, faculty_name: str) -> None:
        super().__init__()
        self.faculty_name = faculty_name

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.faculty_name == self.faculty_name


class SpecialityIdSpecification(SpecialityBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
