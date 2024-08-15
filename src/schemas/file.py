from pydantic import BaseModel, Field, PositiveInt

from schemas.base_entity import DateTimeBase, UUIDInDB


class FileBase(BaseModel):
    file_id: str
    name: str
    size: PositiveInt | None = Field(
        description="Size of file in bytes, it could be none"
    )


class FileInDB(FileBase, UUIDInDB, DateTimeBase):
    ...


class FileCreate(FileBase):
    ...


class FileUpdate(BaseModel):
    file_id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    size: PositiveInt | None = Field(
        description="Size of file in bytes, it could be none",
        default=None,
    )
