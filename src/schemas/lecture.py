import uuid

from pydantic import BaseModel, Field

from schemas.base_entity import DateTimeBase, UUIDInDB
from schemas.file import FileInDB


class LectureBase(BaseModel):
    lecturer_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    title: str = Field(
        examples=["First Lecture", "Second Lecture", "First Session"],
        description="Enter the title(name) of lecture",
    )
    body: str | None = Field(
        description="Enter your lecture body(description)",
        examples=[
            "This is lecture is important, please give it attention!!!",
        ],
    )


class LectureInDB(LectureBase, UUIDInDB, DateTimeBase):
    file_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )


class LectureInDBExtended(LectureBase, UUIDInDB, DateTimeBase):
    file: FileInDB


class LectureCreate(LectureBase):
    file_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )


class LecturetUpdate(BaseModel):
    lecturer_course_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
        default=None,
    )
    file_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
        default=None,
    )
    name: str | None = Field(
        examples=["First Lecture", "Second Lecture", "First Session"],
        description="Enter the title(name) of lecture",
        default=None,
    )
    body: str | None = Field(
        description="Enter your lecture body(description)",
        examples=["This lecture is important, please give it attention!!!"],
        default=None,
    )
