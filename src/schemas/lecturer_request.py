import uuid

from pydantic import BaseModel, Field, PositiveInt

from schemas.base_entity import DateTimeBase, UUIDInDB


class LecturerRequestBase(BaseModel):
    user_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    faculty_name: str = Field(
        description="Enter your faculty name",
        min_length=2,
        max_length=32,
    )
    description: str | None = Field(min_length=0, max_length=50)


class LecturerRequestInDB(LecturerRequestBase, UUIDInDB, DateTimeBase):
    processed_at: PositiveInt | None
    is_accepted: bool | None


class LecturerRequestCreate(LecturerRequestBase):
    ...


class LecturerRequestUpdate(BaseModel):
    faculty_name: str | None = Field(
        description="Enter your faculty name",
        min_length=2,
        max_length=32,
        default=None,
    )
    description: str | None = Field(
        min_length=0,
        max_length=50,
        default=None,
    )


class LecturerRequestProcess(BaseModel):
    id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    user_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    faculty_name: str = Field(
        description="Enter your faculty name",
        min_length=2,
        max_length=32,
    )


class LecturerRequestProcessUpdate(BaseModel):
    processed_at: PositiveInt
    is_accepted: bool
