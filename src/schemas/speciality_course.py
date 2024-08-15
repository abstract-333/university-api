from typing import Literal
import uuid
from pydantic import BaseModel, Field, NonNegativeInt

from schemas.base_entity import UUIDInDB
from schemas.speciality import SpecialityInDB


class SpecialityCourseBase(BaseModel):
    speciality_id: uuid.UUID
    course_name: str = Field(max_length=32, min_length=2)
    current_class: NonNegativeInt = Field(le=6)
    semester: Literal[1, 2]


class SpecialityCourseInDBExtended(UUIDInDB):
    course_name: str = Field(max_length=32, min_length=2)
    current_class: NonNegativeInt = Field(le=6)
    semester: Literal[1, 2]
    speciality: SpecialityInDB


class SpecialityCourseInDB(SpecialityCourseBase, UUIDInDB):
    ...


class SpecialityCourseCreate(SpecialityCourseBase):
    ...
