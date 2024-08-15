import time
import uuid

from pydantic import BaseModel, Field, PositiveInt

from schemas.base_entity import (
    DateTimeBase,
    UUIDInDB,
    uuid_field,
)
from schemas.lecturer import LecturerInDB
from schemas.student import StudentInDB, StudentInDBExtended
from schemas.taught_course import (
    TaughtCourseInDBSpecliatyCourse,
)


def get_time() -> int:
    return int(time.time())


class CourseRequestBase(BaseModel):
    taught_course_id: uuid.UUID = uuid_field()
    description: str | None = Field(min_length=0, max_length=50)


class CourseRequestInDBExtended(UUIDInDB, DateTimeBase):
    student_id: uuid.UUID = uuid_field()
    description: str | None = Field(min_length=0, max_length=50)
    processed_at: PositiveInt | None
    processed_by: LecturerInDB | None
    is_accepted: bool | None
    course: TaughtCourseInDBSpecliatyCourse


class CourseRequestInDBExtendedStudent(UUIDInDB, DateTimeBase):
    student: StudentInDBExtended
    processed_at: PositiveInt | None
    processed_by: uuid.UUID | None
    is_accepted: bool | None


class CourseRequestInDB(CourseRequestBase, UUIDInDB, DateTimeBase):
    student_id: uuid.UUID = uuid_field()
    processed_at: PositiveInt | None
    processed_by: uuid.UUID | None
    is_accepted: bool | None


class CourseRequestCreate(CourseRequestBase):
    student_id: uuid.UUID = uuid_field()


class CourseRequestUpdate(BaseModel):
    description: str = Field(
        min_length=2,
        max_length=50,
        default=None,
    )


class CourseRequestProcess(BaseModel):
    processed_at: PositiveInt = Field(default_factory=get_time, kw_only=True)
    processed_by: uuid.UUID
    is_accepted: bool
