import datetime
from typing import TYPE_CHECKING

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
    from models import UsersOrm, FacultiesOrm


class LecturersRequestsOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    __tablename__ = "lecturers_requests"
    user_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    faculty_name: Mapped[str] = mapped_column(
        String(length=32),
        ForeignKey(column="faculties.name", ondelete="CASCADE", onupdate="CASCADE"),
    )
    description: Mapped[str] = mapped_column(
        String(length=50),
        nullable=True,
        unique=False,
    )
    is_accepted: Mapped[bool] = mapped_column(nullable=True, unique=False)
    processed_at: Mapped[int] = mapped_column(nullable=True, unique=False)

    # Relationships for ORM
    user: Mapped["UsersOrm"] = relationship(back_populates="lecturers_requests")
    faculty: Mapped["FacultiesOrm"] = relationship(
        back_populates="lecturers_requests",
    )

    __table_args__ = (
        CheckConstraint(
            "processed_at > 0",
            name="ensure_is_accepted_positive",
        ),
    )

    def __str__(self) -> str:
        return f"Lecturer Request: {self.description if len(self.description)<15 else self.description[:15]} is_accepted: {self.is_accepted} , added_at: {datetime.datetime.fromtimestamp(self.added_at)}"
