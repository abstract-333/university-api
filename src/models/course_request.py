import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
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
    from models import UsersOrm, TaughtCoursesOrm, StudentsOrm


class CoursesRequestsOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    __tablename__ = "courses_requests"
    student_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="students.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    taught_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="taught_courses.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="taught_course_id_fkey",
        ),
    )
    description: Mapped[str] = mapped_column(
        String(length=50),
        nullable=True,
        unique=False,
    )
    is_accepted: Mapped[bool] = mapped_column(nullable=True, unique=False)
    processed_at: Mapped[int] = mapped_column(nullable=True, unique=False)
    processed_by: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    # Relationships for ORM
    student: Mapped["StudentsOrm"] = relationship(back_populates="courses_requests")
    processed_by_user: Mapped[Optional["UsersOrm"]] = relationship(
        back_populates="courses_requests"
    )
    course: Mapped["TaughtCoursesOrm"] = relationship(
        back_populates="courses_requests",
    )
    __table_args__ = (
        CheckConstraint(
            "processed_at > 0",
            name="ensure_is_accepted_positive",
        ),
        CheckConstraint(
            "processed_by <> student_id",
            name="user_didn't_accept_itself",
        ),
    )

    def __str__(self) -> str:
        return f"Course Request: {self.description if len(self.description)<15 else self.description[:15]} is_accepted: {self.is_accepted} , added_at: {datetime.datetime.fromtimestamp(self.added_at)}"
