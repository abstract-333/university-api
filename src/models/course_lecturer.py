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
)
from models.addons.mixins import UUIDColumnMixin

if TYPE_CHECKING:
    from models import (
        TaughtCoursesOrm,
        LecturersOrm,
        QuizzesOrm,
        QuestionsOrm,
        PostsOrm,
        LecturesOrm,
    )


class CoursesLecturersOrm(BaseModelORM, UUIDColumnMixin):
    __tablename__ = "courses_lecturers"
    course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="taught_courses.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    lecturer_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="lecturers.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    # Relationships for ORM
    course: Mapped["TaughtCoursesOrm"] = relationship(
        back_populates="courses_lecturers"
    )
    lecturer: Mapped["LecturersOrm"] = relationship(back_populates="taught_courses")
    quizzes: Mapped[list["QuizzesOrm"]] = relationship(back_populates="lecturer_course")
    questions: Mapped[list["QuestionsOrm"]] = relationship(
        back_populates="lecturer_course"
    )
    posts: Mapped[list["PostsOrm"]] = relationship(back_populates="lecturer_course")
    lectures: Mapped[list["LecturesOrm"]] = relationship(
        back_populates="lecturer_course"
    )

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "lecturer_id",
            name="taught_course_id_lecturer_id_constraint",
        ),
    )

    def __str__(self) -> str:
        return f"Course Lecturer: {self.id}"
