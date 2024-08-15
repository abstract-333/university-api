import uuid

from pydantic import BaseModel, Field

from schemas.base_entity import UUIDInDB
from schemas.user import UserRead


class LecturerBase(BaseModel):
    user_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    faculty_name: str = Field(
        description="Enter your faculty name",
    )
    is_approved: bool = Field(
        description="Whether lecturer is approved or not",
    )


class LecturerInDB(LecturerBase, UUIDInDB):
    ...


class LecturerComment(UUIDInDB):
    user: UserRead
    faculty_name: str = Field(
        description="Enter your faculty name",
    )
    is_approved: bool = Field(
        description="Whether lecturer is approved or not",
    )


class LecturerCreate(LecturerBase):
    is_approved: bool = Field(
        description="Whether lecturer is approved or not",
        default=False,
    )
