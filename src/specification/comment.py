from abc import ABC
from uuid import UUID

from sqlalchemy import ColumnElement

from models.comment import CommentsOrm
from schemas.comment import AuthorType
from specification.base import SpecificationSQLAlchemy


class CommentBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = CommentsOrm


class CommentStudentIdSpecification(CommentBaseSpecification):
    def __init__(self, student_id: UUID) -> None:
        super().__init__()
        self.student_id: UUID = student_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.student_id == self.student_id


class CommentLecturerIdSpecification(CommentBaseSpecification):
    def __init__(self, lecturer_id: UUID) -> None:
        super().__init__()
        self.lecturer_id: UUID = lecturer_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.lecturer_id == self.lecturer_id


class CommentAuthorTypeSpecification(CommentBaseSpecification):
    def __init__(self, author_type: AuthorType) -> None:
        super().__init__()
        self.author_type: AuthorType = author_type

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.author_type == self.author_type


class CommentPostIdSpecification(CommentBaseSpecification):
    def __init__(self, post_id: UUID) -> None:
        super().__init__()
        self.post_id: UUID = post_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.post_id == self.post_id


class CommentIdSpecification(CommentBaseSpecification):
    def __init__(self, id: UUID) -> None:
        super().__init__()
        self.id: UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
