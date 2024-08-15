import uuid
from pydantic import BaseModel

from schemas.base_entity import UUIDInDB
from schemas.student import StudentInDB
from schemas.taught_course import TaughtCourseInDBExtended
from schemas.user import UserRead


class EnrolledCourseBase(BaseModel):
    student_id: uuid.UUID
    taught_course_id: uuid.UUID


class EnrolledCourseInDB(UUIDInDB, EnrolledCourseBase):
    is_banned: bool


class EnrolledCourseInDBExtended(UUIDInDB):
    student_id: uuid.UUID
    course: TaughtCourseInDBExtended
    is_banned: bool


class EnrolledCourseInDBExtendedJoined(UUIDInDB):
    student: StudentInDB
    course: TaughtCourseInDBExtended
    is_banned: bool


class EnrolledCourseCreate(EnrolledCourseBase):
    ...


class EnrolledCourseUpdate(BaseModel):
    is_banned: bool
