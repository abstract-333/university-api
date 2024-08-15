import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
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
    from models import FilesOrm, CoursesLecturersOrm


class LecturesOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    lecturer_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="courses_lecturers.id", ondelete="CASCADE", onupdate="CASCADE"
        )
    )
    file_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("files.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    title: Mapped[str] = mapped_column(__name_pos=String(length=100), nullable=False)
    body: Mapped[str] = mapped_column(__name_pos=String(length=10000), nullable=True)

    # Relationships for ORM
    file: Mapped["FilesOrm"] = relationship(
        back_populates="lectures",
    )
    lecturer_course: Mapped["CoursesLecturersOrm"] = relationship(
        back_populates="lectures",
    )
    __table_args__ = (
        UniqueConstraint(
            "lecturer_course_id",
            "file_id",
            name="non_duplicated_file_lecture_constraint",
        ),
    )

    def __str__(self) -> str:
        return f"Lecture: {self.title if len(self.title)<15 else self.title}, added_at: {datetime.datetime.fromtimestamp(self.added_at)}"
