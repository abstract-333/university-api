import uuid

from pydantic import BaseModel, Field, model_validator

from schemas.base_entity import DateTimeBase, UUIDInDB
from schemas.course_lecturer import CourseLecturerInDBExtended


class QuestionBase(BaseModel):
    lecturer_course_id: uuid.UUID = Field(
        examples=["018a92b4-8db8-7c90-a7ef-e8d335a64db2"], description="uuid7"
    )
    body: str = Field(
        description="Enter your question text",
    )
    choices: list[str] = Field(description="Choices of question, normally it is 4")
    right_choice: str = Field(description="The right choice")


class QuestionInDB(QuestionBase, UUIDInDB, DateTimeBase):
    is_visible: bool


class QuestionInDBExtended(QuestionBase, UUIDInDB, DateTimeBase):
    is_visible: bool
    lecturer_course: CourseLecturerInDBExtended


class QuestionCreate(QuestionBase):
    @model_validator(mode="after")
    def check_choices_has_right_choice(self):
        """
        Validate that right_choice is included in choices
        """

        if not self.right_choice in self.choices:
            raise ValueError("choices must include the right choice")

        return self


class QuestionUpdate(BaseModel):
    choices: list[str] | None = Field(
        description="Choices of question, normally it is 4",
        default=None,
    )
    right_choice: str | None = Field(description="The right choice", default=None)
    body: str | None = Field(
        description="Enter your question text",
        default=None,
    )
    is_visible: bool | None = Field(
        description="Make question visible in next quizzes",
        default=None,
    )

    @model_validator(mode="after")
    def check_choices_has_right_choice(self):
        """
        Validate that right_choice is included in choices
        """

        if self.choices and self.right_choice:
            if not self.right_choice in self.choices:
                raise ValueError("choices must include the right choice")

        return self
