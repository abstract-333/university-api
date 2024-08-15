from abc import ABC
from uuid import UUID

from sqlalchemy import ColumnElement

from models.file import FilesOrm
from specification.base import SpecificationSQLAlchemy


class FileBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = FilesOrm


class FileIdSpecification(FileBaseSpecification):
    def __init__(self, id: UUID) -> None:
        super().__init__()
        self.id: UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class FileFileIdSpecification(FileBaseSpecification):
    def __init__(self, file_id: str) -> None:
        super().__init__()
        self.file_id: str = file_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.file_id == self.file_id
