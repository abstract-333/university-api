import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.post import PostsOrm
from specification.base import SpecificationSQLAlchemy


class PostBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = PostsOrm


class PostCourseIdSpecification(PostBaseSpecification):
    def __init__(self, course_id: uuid.UUID) -> None:
        super().__init__()
        self.course_id: uuid.UUID = course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.lecturer_course_id == self.course_id


class PostIdSpecification(PostBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id
