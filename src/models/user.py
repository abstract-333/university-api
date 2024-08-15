from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models import (
    BaseModelORM,
    boolTrue,
    boolFalse,
)
from models.addons.mixins import TimeColumnsMixin, UUIDColumnMixin

if TYPE_CHECKING:
    from models import (
        SupervisorsOrm,
        LecturersOrm,
        StudentsOrm,
        LecturersRequestsOrm,
        CoursesRequestsOrm,
        ActiveSessionsOrm,
    )


class UsersOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    first_name: Mapped[String] = mapped_column(String(length=64), nullable=False)
    last_name: Mapped[String] = mapped_column(String(length=64), nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=128 * 5),
        nullable=False,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(String(length=256), nullable=False)
    is_active: Mapped[boolTrue]
    is_verified: Mapped[boolFalse]
    is_superuser: Mapped[boolFalse]

    students: Mapped[list["StudentsOrm"]] = relationship(
        back_populates="user",
    )
    lecturers: Mapped[list["LecturersOrm"]] = relationship(back_populates="user")

    active_sessions: Mapped[list["ActiveSessionsOrm"]] = relationship(
        back_populates="user"
    )
    lecturers_requests: Mapped[list["LecturersRequestsOrm"]] = relationship(
        back_populates="user"
    )
    courses_requests: Mapped[list["CoursesRequestsOrm"]] = relationship(
        back_populates="processed_by_user"
    )

    repr_cols_num = 5
    repr_cols = ("is_active", "is_superuser")

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}"
