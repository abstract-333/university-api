import datetime
from typing import TYPE_CHECKING

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
    from models import CommentsOrm, CoursesLecturersOrm


class PostsOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    lecturer_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="courses_lecturers.id", ondelete="CASCADE", onupdate="CASCADE"
        )
    )
    body: Mapped[str] = mapped_column(String(length=50000), nullable=False)

    # Relationships for ORM
    comments: Mapped[list["CommentsOrm"]] = relationship(back_populates="post")
    lecturer_course: Mapped["CoursesLecturersOrm"] = relationship(
        back_populates="posts",
    )

    def __str__(self) -> str:
        return f"Post: {self.body if len(self.body)<15 else self.body[:15]}, added_at: {datetime.datetime.fromtimestamp(self.added_at)}"
