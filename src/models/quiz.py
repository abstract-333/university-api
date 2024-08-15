from models.addons.mixins import TimeColumnsMixin, UUIDColumnMixin
from models.base import BaseModelORM
from typing import TYPE_CHECKING

from sqlalchemy import (
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

from models import (
    BaseModelORM,
    uuid_type,
)
from models.addons.mixins import TimeColumnsMixin

if TYPE_CHECKING:
    from models import CoursesLecturersOrm, QuizzesResultsOrm


class QuizzesOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    lecturer_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="courses_lecturers.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
    )
    title: Mapped[str] = mapped_column(String(length=50), nullable=False, unique=False)
    duration: Mapped[int] = mapped_column(nullable=False, unique=False)
    number_of_questions: Mapped[int] = mapped_column(nullable=False, unique=False)
    mark: Mapped[int] = mapped_column(nullable=False, unique=False)
    start_date: Mapped[int] = mapped_column(
        nullable=False,
        unique=False,
    )
    end_date: Mapped[int] = mapped_column(
        nullable=False,
        unique=False,
    )

    # Relationships for ORM
    lecturer_course: Mapped["CoursesLecturersOrm"] = relationship(
        back_populates="quizzes",
    )
    quizzes_results: Mapped[list["QuizzesResultsOrm"]] = relationship(
        back_populates="quiz"
    )
    __table_args__ = (
        UniqueConstraint(
            "title",
            "lecturer_course_id",
            name="unique_quiz_in_course",
        ),
        CheckConstraint(
            sqltext="duration > 0",
            name="duration_is_positive",
        ),
        CheckConstraint(
            sqltext="mark > 0",
            name="mark_is_postive",
        ),
    )

    def __str__(self) -> str:
        return f"Quiz: {self.title}"
