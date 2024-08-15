import uuid

from pydantic import BaseModel, Field, PositiveInt

from schemas.base_entity import UUIDInDB


class ActiveSessionBase(BaseModel):
    user_id: uuid.UUID
    refresh_token: str = Field(max_length=256, min_length=100)
    device_id: str = Field(max_length=44, min_length=10)
    device_name: str = Field(
        max_length=127,
        min_length=2,
        examples=["Samsung Galaxy S24 Ultra", "IPhone 15", "Xiaomi 14"],
    )
    expire_at: PositiveInt


class ActiveSessionInDB(ActiveSessionBase, UUIDInDB):
    added_at: PositiveInt


class ActiveSessionOutput(UUIDInDB):
    device_name: str = Field(
        max_length=127,
        min_length=2,
        examples=["Samsung Galaxy S24 Ultra", "IPhone 15", "Xiaomi 14"],
    )
    expire_at: PositiveInt
    added_at: PositiveInt


class ActiveSessionCreate(ActiveSessionBase):
    ...


class ActiveSessionUpdate(BaseModel):
    refresh_token: str | None = Field(max_length=256, min_length=100, default=None)
    expire_at: PositiveInt | None = None
