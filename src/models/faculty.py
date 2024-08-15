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
    from models import (
        SpecialitiesOrm,
        LecturersOrm,
        SupervisorsOrm,
        LecturersRequestsOrm,
    )


class FacultiesOrm(BaseModelORM):
    name: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        autoincrement=False,
        unique=True,
    )
    max_class: Mapped[int] = mapped_column(nullable=False)

    # Relationships for ORM
    specialities: Mapped[list["SpecialitiesOrm"]] = relationship(
        back_populates="faculty"
    )
    lecturers: Mapped[list["LecturersOrm"]] = relationship(back_populates="faculty")
    lecturers_requests: Mapped[list["LecturersRequestsOrm"]] = relationship(
        back_populates="faculty"
    )

    def __str__(self) -> str:
        return f"Faculty: {self.name}"
