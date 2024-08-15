from typing import TYPE_CHECKING

from sqlalchemy import (
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
    boolFalse,
)
from models.addons.mixins import UUIDColumnMixin

if TYPE_CHECKING:
    from models import (
        StudentsOrm,
        QuizzesResultsOrm,
        TaughtCoursesOrm,
    )


class EnrolledCoursesOrm(BaseModelORM, UUIDColumnMixin):
    __tablename__ = "enrolled_courses"
    student_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="students.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    taught_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="taught_courses.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="taught_course_id_fkey",
        ),
    )
    is_banned: Mapped[boolFalse]

    # Relationships for ORM
    student: Mapped["StudentsOrm"] = relationship(back_populates="enrolled_courses")
    course: Mapped["TaughtCoursesOrm"] = relationship(
        back_populates="enrolled_courses",
    )
    quizzes_results: Mapped[list["QuizzesResultsOrm"]] = relationship(
        back_populates="enrolled_course"
    )
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "taught_course_id",
            name="student_course_unique_constraint",
        ),
    )

    def __str__(self) -> str:
        return f"Enrolled Course: {self.id}"
