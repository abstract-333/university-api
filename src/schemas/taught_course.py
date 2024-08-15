import uuid
from pydantic import BaseModel, Field

from schemas.base_entity import UUIDInDB
from schemas.speciality_course import SpecialityCourseInDB, SpecialityCourseInDBExtended


class TaughtCourseBase(BaseModel):
    description: str
    year: int = Field(ge=2022, le=2100)
    speciality_course_id: uuid.UUID


class TaughtCourseInDB(TaughtCourseBase, UUIDInDB):
    ...


class TaughtCourseInDBExtended(UUIDInDB):
    description: str
    year: int = Field(ge=2022, le=2100)
    speciality_course: SpecialityCourseInDBExtended


class TaughtCourseInDBSpecliatyCourse(UUIDInDB):
    description: str
    year: int = Field(ge=2022, le=2100)
    speciality_course: SpecialityCourseInDB


class TaughtCourseCreate(TaughtCourseBase):
    ...


class TaughtCourseUpdate(BaseModel):
    description: str | None = None
    year: int | None = Field(ge=2022, le=2100, default=None)
