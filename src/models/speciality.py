from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models import (
    BaseModelORM,
)
from models.addons.mixins import UUIDColumnMixin

if TYPE_CHECKING:
    from models import FacultiesOrm, StudentsOrm, SpecialityCoursesOrm


class SpecialitiesOrm(BaseModelORM, UUIDColumnMixin):
    name: Mapped[str] = mapped_column(
        String(length=32),
    )
    faculty_name: Mapped[str] = mapped_column(
        ForeignKey("faculties.name", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Relationships for ORM
    faculty: Mapped["FacultiesOrm"] = relationship(back_populates="specialities")
    students: Mapped[list["StudentsOrm"]] = relationship(back_populates="speciality")
    speciality_courses: Mapped[list["SpecialityCoursesOrm"]] = relationship(
        back_populates="speciality"
    )

    # speciality_courses: Mapped[list["SpecialityCoursesOrm"]] = relationship(
    #     back_populates="speciality",
    #     overlaps="taught_courses",
    # )

    # taught_courses: Mapped[list["TaughtCoursesOrm"]] = relationship(
    #     back_populates="specialities",
    #     secondary="specialities_courses",
    #     overlaps="taught_courses",
    # )

    def __str__(self):
        return f"Speciality: {self.name}"
