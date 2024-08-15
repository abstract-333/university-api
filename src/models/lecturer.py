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
    from models import FacultiesOrm, UsersOrm, CoursesLecturersOrm, CommentsOrm


class LecturersOrm(BaseModelORM, UUIDColumnMixin):
    user_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    faculty_name: Mapped[str] = mapped_column(
        ForeignKey(column="faculties.name", ondelete="CASCADE", onupdate="CASCADE")
    )
    is_approved: Mapped[bool] = mapped_column(nullable=True, default=False)

    # Relationships for ORM
    faculty: Mapped["FacultiesOrm"] = relationship(
        back_populates="lecturers",
    )
    user: Mapped["UsersOrm"] = relationship(
        back_populates="lecturers",
    )

    taught_courses: Mapped[list["CoursesLecturersOrm"]] = relationship(
        back_populates="lecturer"
    )
    comments: Mapped[list["CommentsOrm"]] = relationship(
        back_populates="lecturer",
    )
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "faculty_name",
            name="user_id_faculty_constraints",
        ),
    )

    def __str__(self) -> str:
        return f"Lecturer: {self.faculty_name}"
