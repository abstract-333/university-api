from typing import TYPE_CHECKING, TypeVar

from pydantic import BaseModel
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
from models.addons.mixins import UUIDColumnMixin

if TYPE_CHECKING:
    from models import (
        CoursesRequestsOrm,
        SpecialitiesOrm,
        UsersOrm,
        EnrolledCoursesOrm,
        CommentsOrm,
    )


class StudentsOrm(BaseModelORM, UUIDColumnMixin):
    university_id: Mapped[int]
    user_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    speciality_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="specialities.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    class_id: Mapped[int] = mapped_column(nullable=False)
    is_freshman: Mapped[bool] = mapped_column(nullable=False)

    # Relationships for ORM
    speciality: Mapped["SpecialitiesOrm"] = relationship(back_populates="students")
    user: Mapped["UsersOrm"] = relationship(back_populates="students")
    enrolled_courses: Mapped[list["EnrolledCoursesOrm"]] = relationship(
        back_populates="student"
    )
    courses_requests: Mapped[list["CoursesRequestsOrm"]] = relationship(
        back_populates="student"
    )
    comments: Mapped[list["CommentsOrm"]] = relationship(
        back_populates="student",
    )

    __table_args__ = (
        UniqueConstraint(
            "university_id",
            "speciality_id",
            name="student_speciality_constraint",
        ),
        UniqueConstraint(
            "user_id",
            "speciality_id",
            name="user_id_speciality_constraint",
        ),
        CheckConstraint(sqltext="class_id < 7 and class_id > 0", name="class_id_valid"),
    )

    def __str__(self) -> str:
        return f"Student: {self.university_id} "
