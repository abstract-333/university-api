import uuid

from pydantic import BaseModel, Field, PositiveInt, model_validator

from schemas.base_entity import DateTimeBase, UUIDInDB
from schemas.course_lecturer import CourseLecturerInDBExtended


class QuizBase(BaseModel):
    title: str = Field(
        description="Enter your quiz text",
        min_length=5,
        max_length=50,
    )
    mark: PositiveInt
    number_of_questions: PositiveInt = Field(
        description="Number of questions that student will have to solve"
    )
    duration: PositiveInt = Field(description="Duration in seconds")
    start_date: PositiveInt = Field(description="Start date in unix time (seconds)")
    end_date: PositiveInt = Field(description="End date in unix time (seconds)")


class QuizInDB(QuizBase, UUIDInDB, DateTimeBase):
    lecturer_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )


class QuizInDBExtended(QuizBase, UUIDInDB, DateTimeBase):
    lecturer_course: CourseLecturerInDBExtended


class QuizCreate(QuizBase):
    lecturer_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )

    @model_validator(mode="after")
    def validate_end_date_greater_start_date(self):
        """
        Validate that right_choice is included in choices
        """

        if self.end_date < self.start_date:
            raise ValueError("End date must be greater than start date")

        return self


class QuizUpdate(BaseModel):
    title: str | None = Field(
        description="Enter your quiz text",
        default=None,
    )
    mark: PositiveInt | None = Field(default=None)
    number_of_questions: PositiveInt | None = Field(
        description="Number of questions that student will have to solve",
        default=None,
    )
    duration: PositiveInt | None = Field(
        description="Duration in seconds", default=None
    )
    start_date: PositiveInt | None = Field(
        description="Start date in unix time (seconds)",
        default=None,
    )
    end_date: PositiveInt | None = Field(
        description="End date in unix time (seconds)",
        default=None,
    )
