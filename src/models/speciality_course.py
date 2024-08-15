from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
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
    from models import TaughtCoursesOrm, CoursesOrm, SpecialitiesOrm


class SpecialityCoursesOrm(BaseModelORM, UUIDColumnMixin):
    __tablename__ = "specialities_courses"
    speciality_id: Mapped[uuid_type] = mapped_column(
        ForeignKey("specialities.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    course_name: Mapped[str] = mapped_column(
        ForeignKey(
            column="courses.name",
            name="course_name_fkey",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    current_class: Mapped[int] = mapped_column(SmallInteger(), nullable=False)
    semester: Mapped[int] = mapped_column(SmallInteger(), nullable=False)

    # Relationships for ORM

    course: Mapped["CoursesOrm"] = relationship(back_populates="speciality_courses")
    taught_courses: Mapped[list["TaughtCoursesOrm"]] = relationship(
        back_populates="speciality_course"
    )
    speciality: Mapped["SpecialitiesOrm"] = relationship(
        back_populates="speciality_courses"
    )
    # taught_course: Mapped["TaughtCoursesOrm"] = relationship(
    #     back_populates="speciality_courses", overlaps="specialities,taught_courses"
    # )
    # speciality: Mapped["SpecialitiesOrm"] = relationship(
    #     back_populates="speciality_courses",
    #     overlaps="specialities,taught_courses",
    # )

    __table_args__ = (
        UniqueConstraint(
            "speciality_id",
            "course_name",
            name="unique_course_speciality_constraint",
        ),
        CheckConstraint(
            sqltext="current_class <= 6 and current_class >=1",
            name="chech_current_class",
        ),
        CheckConstraint(sqltext="semester in (1, 2)", name="check_semester"),
    )

    def __str__(self) -> str:
        return f"Speciality Course: {self.id}"
