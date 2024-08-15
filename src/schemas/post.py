import uuid

from pydantic import BaseModel, Field

from schemas.base_entity import DateTimeBase, UUIDInDB
from schemas.comment import CommentInDBExtended
from schemas.course_lecturer import CourseLecturerInDBExtendedLecturer


class PostBase(BaseModel):
    lecturer_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    body: str = Field(
        description="Enter your post text",
        examples=["This is first post", "This is post about University, so.."],
    )


class PostInDB(UUIDInDB, DateTimeBase):
    lecturer_course_id: uuid.UUID
    body: str


class PostInDBExtended(UUIDInDB, DateTimeBase):
    lecturer_course: CourseLecturerInDBExtendedLecturer
    body: str
    comments: list[CommentInDBExtended]


class PostInDBExtendedWithoutComments(UUIDInDB, DateTimeBase):
    lecturer_course: CourseLecturerInDBExtendedLecturer
    body: str


class PostCreate(PostBase):
    ...


class PostUpdate(UUIDInDB):
    lecturer_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
    )
    body: str = Field(
        description="Enter your post text",
        examples=["This is first post", "This is post about University, so.."],
    )
