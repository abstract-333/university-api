import uuid

from pydantic import BaseModel

from schemas.base_entity import UUIDInDB


class CourseBase(BaseModel):
    name: str


class CourseInDB(CourseBase, UUIDInDB):
    ...


class CourseCreate(CourseBase):
    ...
