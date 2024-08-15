from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
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
from models.addons.mixins import TimeColumnsMixin, UUIDColumnMixin

if TYPE_CHECKING:
    from models import LecturesOrm


class FilesOrm(BaseModelORM, TimeColumnsMixin, UUIDColumnMixin):
    file_id: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(
        __name_pos=String(length=100),
        nullable=False,
    )
    size: Mapped[int] = mapped_column(nullable=True, unique=False)

    # Relationships for ORM
    lectures: Mapped[list["LecturesOrm"]] = relationship(
        back_populates="file",
    )

    __table_args__ = (
        CheckConstraint(
            "size > 0",
            "positive_size",
        ),
    )

    def __str__(self) -> str:
        return f"File: {self.name if len(self.name)<15 else self.name}"
