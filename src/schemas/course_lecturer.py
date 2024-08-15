import uuid

from pydantic import BaseModel

from schemas.base_entity import UUIDInDB
from schemas.lecturer import LecturerComment
from schemas.taught_course import TaughtCourseInDBExtended


class CourseLecturerBase(BaseModel):
    course_id: uuid.UUID
    lecturer_id: uuid.UUID


class CourseLecturerInDB(CourseLecturerBase, UUIDInDB):
    ...


class CourseLecturerInDBExtended(UUIDInDB):
    lecturer_id: uuid.UUID
    course: TaughtCourseInDBExtended


class CourseLecturerInDBExtendedLecturer(UUIDInDB):
    lecturer: LecturerComment
    course: TaughtCourseInDBExtended


class CourseLecturerCreate(CourseLecturerBase):
    ...


class CourseLecturerUpdate(CourseLecturerBase):
    ...
