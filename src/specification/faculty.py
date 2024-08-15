from abc import ABC

from sqlalchemy import ColumnElement

from models.faculty import FacultiesOrm
from specification.base import SpecificationSQLAlchemy


class FacultyBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = FacultiesOrm


class FacultyNameSpecification(FacultyBaseSpecification):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.name == self.name
