from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
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
from models.addons.mixins import TimeColumnsMixin, UUIDColumnMixin

if TYPE_CHECKING:
    from models import EnrolledCoursesOrm, QuizzesOrm


class QuizzesResultsOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    __tablename__ = "quizzes_results"
    enrolled_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="enrolled_courses.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    quiz_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="quizzes.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    result: Mapped[float] = mapped_column(nullable=False, unique=False)

    # Relationships for ORM
    enrolled_course: Mapped["EnrolledCoursesOrm"] = relationship(
        back_populates="quizzes_results",
    )
    quiz: Mapped["QuizzesOrm"] = relationship(back_populates="quizzes_results")

    __table_args__ = (
        UniqueConstraint(
            "quiz_id",
            "enrolled_course_id",
            name="quiz_take_once_constraint",
        ),
    )

    def __str__(self) -> str:
        return f"Quiz Result: {self.result}"
