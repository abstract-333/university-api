import uuid

from pydantic import BaseModel, Field
from pydantic.types import NonNegativeFloat

from schemas.base_entity import DateTimeBase, UUIDInDB
from schemas.enrolled_course import EnrolledCourseInDBExtended
from schemas.quiz import QuizInDBExtended


class QuizResultBase(BaseModel):
    enrolled_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    quiz_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    result: NonNegativeFloat


class QuizResultInDB(QuizResultBase, UUIDInDB, DateTimeBase):
    ...


class QuizResultInDBQuizExtended(UUIDInDB, DateTimeBase):
    quiz: QuizInDBExtended
    result: NonNegativeFloat
    enrolled_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )


class QuizResultInDBExtended(UUIDInDB, DateTimeBase):
    enrolled_course: EnrolledCourseInDBExtended
    quiz: QuizInDBExtended
    result: NonNegativeFloat


class QuizResultCreate(QuizResultBase):
    ...


class QuizResultUpdate(BaseModel):
    enrolled_course_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
        default=None,
    )
    quiz_id: uuid.UUID | None = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"],
        description="uuid7",
        default=None,
    )
    result: NonNegativeFloat | None = Field(default=None)
