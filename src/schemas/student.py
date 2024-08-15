import uuid
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    NonNegativeInt,
    PositiveInt,
)

from schemas.base_entity import UUIDInDB
from schemas.speciality import SpecialityInDB
from schemas.user import UserRead


class StudentBase(BaseModel):
    university_id: PositiveInt = Field(
        examples=["4444"],
        description="""Your university id number that are written in student card, note that you can only have one 
        record in faculty""",
    )
    class_id: NonNegativeInt = Field(
        ge=1,
        le=6,
        examples=[1, 2, 3, 4, 5, 6],
        description="Enter your class",
    )
    is_freshman: bool


class StudentExtendedBase(StudentBase):
    user_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    speciality_id: uuid.UUID


class StudentInDB(StudentExtendedBase, UUIDInDB):
    """Student InDB without joined tables"""

    ...


class StudentInDBExtended(StudentBase, UUIDInDB):
    user: UserRead
    speciality_id: uuid.UUID


class StudentComment(UUIDInDB, StudentBase):
    user: UserRead
    speciality: SpecialityInDB


class StudentInDBWithSpeciality(UUIDInDB):
    """Student InDB schema that has speciality"""

    university_id: PositiveInt = Field(
        examples=["4444"],
        description="""Your university id number that are written in student card, note that you can only have one 
        record in faculty""",
    )
    class_id: NonNegativeInt = Field(
        examples=[1, 2, 3, 4, 5, 6], description="Enter your class", le=6
    )
    is_freshman: bool
    speciality: SpecialityInDB


class StudentCreate(BaseModel):
    university_id: PositiveInt = Field(
        examples=["4444"],
        description="""Your university id number that are written in student card, note that you can only have one 
    record in faculty""",
    )
    class_id: NonNegativeInt = Field(
        examples=[1, 2, 3, 4, 5, 6], description="Enter your class", le=6
    )
    is_freshman: bool
    speciality_id: uuid.UUID


class StudentCreateFull(StudentCreate):
    user_id: uuid.UUID


class StudentUpdate(BaseModel):
    university_id: Optional[PositiveInt] = None
    speciality_id: Optional[uuid.UUID] = None


class StudentUpdateState(BaseModel):
    class_id: Optional[NonNegativeInt] = Field(
        ge=1,
        le=6,
        examples=[1, 2, 3, 4, 5, 6],
        description="Enter your class",
        default=None,
    )
    is_freshman: bool
