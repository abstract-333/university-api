import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
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
    from models import PostsOrm, StudentsOrm, LecturersOrm


class CommentsOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    post_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    body: Mapped[str] = mapped_column(__name_pos=String(length=50000), nullable=False)
    lecturer_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="lecturers.id",
            name="lecturer_id_fkey",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
    )
    student_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="students.id",
            name="student_id_fkey",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
    )
    author_type: Mapped[str] = mapped_column(
        String(length=10),
        nullable=False,
        unique=False,
    )
    # Relationships for ORM
    student: Mapped[Optional["StudentsOrm"]] = relationship(back_populates="comments")
    lecturer: Mapped[Optional["LecturersOrm"]] = relationship(back_populates="comments")
    post: Mapped["PostsOrm"] = relationship(back_populates="comments")

    def __str__(self) -> str:
        return f"Comment: {self.body if len(self.body) < 15 else self.body[:15]}, added_at: {datetime.datetime.fromtimestamp(self.added_at)}"
