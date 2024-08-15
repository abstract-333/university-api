import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.user import UsersOrm
from specification.base import SpecificationSQLAlchemy


class UserBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = UsersOrm


class UserEmailSpecification(UserBaseSpecification):
    def __init__(self, email: str) -> None:
        super().__init__()
        self.email: str = email

    def is_satisfied_by(
        self,
    ) -> ColumnElement[bool]:
        return self.model.email == self.email


class UserIdSpecification(UserBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(
        self,
    ) -> ColumnElement[bool]:
        return self.model.id == self.id
