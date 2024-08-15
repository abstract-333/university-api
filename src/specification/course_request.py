import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.course_request import CoursesRequestsOrm
from specification.base import SpecificationSQLAlchemy


class CourseRequestBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = CoursesRequestsOrm


class CourseRequestStudentIdSpecification(CourseRequestBaseSpecification):
    def __init__(self, student_id: uuid.UUID) -> None:
        super().__init__()
        self.student_id: uuid.UUID = student_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.student_id == self.student_id


class CourseRequestIsProcessedSpecification(CourseRequestBaseSpecification):
    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.processed_at != None


class CourseRequestIsAcceptedSpecification(CourseRequestBaseSpecification):
    def __init__(self, is_accepted: bool) -> None:
        super().__init__()
        self.is_accepted: bool = is_accepted

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.is_accepted == self.is_accepted


class CourseRequestIdSpecification(CourseRequestBaseSpecification):
    def __init__(self, id: uuid.UUID) -> None:
        super().__init__()
        self.id: uuid.UUID = id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.id


class CourseRequestCourseIdSpecification(CourseRequestBaseSpecification):
    def __init__(self, course_id: uuid.UUID) -> None:
        super().__init__()
        self.course_id: uuid.UUID = course_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.taught_course_id == self.course_id
