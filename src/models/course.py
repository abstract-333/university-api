from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models import (
    BaseModelORM,
)

if TYPE_CHECKING:
    from models import SpecialityCoursesOrm


class CoursesOrm(BaseModelORM):
    name: Mapped[str] = mapped_column(
        String(length=32), nullable=False, primary_key=True
    )

    # Relationships for ORM
    speciality_courses: Mapped[list["SpecialityCoursesOrm"]] = relationship(
        back_populates="course",
    )

    def __str__(self) -> str:
        return f"Course: {self.name}"
