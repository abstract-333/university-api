from pydantic import BaseModel, Field

from schemas.base_entity import UUIDInDB


class SpecialityBase(BaseModel):
    name: str = Field(max_length=32, min_length=2)
    faculty_name: str = Field(
        examples=["IT", "Economy", "Biology"], min_length=2, max_length=32
    )


class SpecialityInDB(SpecialityBase, UUIDInDB):
    ...


class SpecialityCreate(SpecialityBase):
    ...
