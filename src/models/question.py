from models.addons.mixins import TimeColumnsMixin, UUIDColumnMixin
from models.base import BaseModelORM, uuid_type, boolTrue
from typing import TYPE_CHECKING

from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from .course_lecturer import CoursesLecturersOrm


class QuestionsOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    lecturer_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="courses_lecturers.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
    )
    body: Mapped[str] = mapped_column(
        String(length=500),
        nullable=False,
        unique=False,
    )
    choices: Mapped[list[str]] = mapped_column(
        ARRAY(item_type=String(length=50), dimensions=1),
        nullable=False,
        unique=False,
    )
    right_choice: Mapped[str] = mapped_column(
        String(length=50), nullable=False, unique=False
    )
    is_visible: Mapped[boolTrue]

    # Relationships for ORM
    lecturer_course: Mapped["CoursesLecturersOrm"] = relationship(
        back_populates="questions",
    )
    __table_args__ = (
        UniqueConstraint(
            "lecturer_course_id",
            "body",
            "choices",
            "right_choice",
            name="unique_questions_in_course",
        ),
        CheckConstraint(
            sqltext="right_choice = ANY(choices)",
            name="right_choice_in_choices_constraint",
        ),
    )

    def __str__(self) -> str:
        return f"Question: {self.body if len(self.body)<15 else self.body[:15]}"
