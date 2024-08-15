import uuid
from pydantic import BaseModel, Field, PositiveInt


def uuid_field():
    return Field(examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7")


def uuid_field_default_none():
    return Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
        default=None,
    )


class UUIDInDB(BaseModel):
    id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )


class DateTimeBase(BaseModel):
    added_at: PositiveInt = Field(
        examples=[1699057255],
        description="Unix time in seconds, it's set once by server",
    )
    updated_at: PositiveInt = Field(
        examples=[1699057255],
        description="Unix time in seconds, first time we insert date it is equal to added_at.",
    )
