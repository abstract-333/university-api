import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.student import StudentsOrm
from specification.base import SpecificationSQLAlchemy


class StudentBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = StudentsOrm


class StudentUserIdSpecification(StudentBaseSpecification):
    def __init__(self, user_id: uuid.UUID) -> None:
        super().__init__()
        self.user_id: uuid.UUID = user_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.user_id == self.user_id


class StudentSpecialityIdSpecification(StudentBaseSpecification):
    def __init__(self, speciality_id: uuid.UUID) -> None:
        super().__init__()
        self.speciality_id: uuid.UUID = speciality_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.speciality_id == self.speciality_id


class StudentUniversityIdSpecification(StudentBaseSpecification):
    def __init__(self, university_id: int) -> None:
        super().__init__()
        self.university_id: int = university_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.university_id == self.university_id


class StudentIdSpecification(StudentBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class StudentIsFreshmanSpecification(StudentBaseSpecification):
    def __init__(self, is_freshman: bool) -> None:
        super().__init__()
        self.is_freshman: bool = is_freshman

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.is_freshman == self.is_freshman
