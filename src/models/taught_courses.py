from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    Text,
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
    from models import (
        CoursesLecturersOrm,
        EnrolledCoursesOrm,
        CoursesRequestsOrm,
        SpecialityCoursesOrm,
    )


class TaughtCoursesOrm(BaseModelORM, UUIDColumnMixin, TimeColumnsMixin):
    __tablename__ = "taught_courses"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    speciality_course_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            "specialities_courses.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="speciality_course_id_fkey",
        ),
        index=True,
    )
    year: Mapped[int] = mapped_column(SmallInteger(), nullable=False)

    # Relationships for ORM

    courses_lecturers: Mapped[list["CoursesLecturersOrm"]] = relationship(
        back_populates="course"
    )
    enrolled_courses: Mapped[list["EnrolledCoursesOrm"]] = relationship(
        back_populates="course"
    )
    courses_requests: Mapped[list["CoursesRequestsOrm"]] = relationship(
        back_populates="course"
    )
    speciality_course: Mapped["SpecialityCoursesOrm"] = relationship(
        back_populates="taught_courses"
    )
    # speciality_courses: Mapped[list["SpecialityCoursesOrm"]] = relationship(
    #     back_populates="taught_course",
    #     overlaps="taught_courses",
    # )
    # specialities: Mapped[list["SpecialitiesOrm"]] = relationship(
    #     back_populates="taught_courses",
    #     secondary="specialities_courses",
    #     overlaps="speciality_courses",
    # )
    __table_args__ = (
        UniqueConstraint(
            "speciality_course_id",
            "year",
            name="unique_coures_in_year_constraint",
        ),
        CheckConstraint(sqltext="year > 2022"),
    )

    def __str__(self) -> str:
        return f"Taught Course: {self.description}"
