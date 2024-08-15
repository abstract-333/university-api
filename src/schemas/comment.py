from enum import Enum
import uuid

from pydantic import BaseModel, Field

from schemas.base_entity import DateTimeBase, UUIDInDB
from schemas.lecturer import LecturerComment
from schemas.student import StudentComment


class AuthorType(str, Enum):
    student = "student"
    lecturer = "lecturer"


class CommentBase(BaseModel):
    student_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    lecturer_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    author_type: AuthorType
    post_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    body: str = Field(
        description="Enter your comment text",
        examples=["This is first comment on post"],
    )


class CommentInDB(CommentBase, UUIDInDB, DateTimeBase):
    ...


class CommentInDBExtended(UUIDInDB, DateTimeBase):
    student: StudentComment | None
    lecturer: LecturerComment | None
    author_type: AuthorType
    post_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    body: str = Field(
        description="Enter your comment text",
        examples=["This is first comment on post"],
    )


class CommentCreate(CommentBase):
    ...


class CommentUpdate(BaseModel):
    student_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
    )
    lecturer_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
    )
    course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
    )
    body: str = Field(
        description="Enter your comment text",
        examples=["This is first comment on post"],
    )
