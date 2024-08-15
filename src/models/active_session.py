import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
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
    timeOnInsert,
)
from models.addons.mixins import UUIDColumnMixin

if TYPE_CHECKING:
    from models import UsersOrm


class ActiveSessionsOrm(BaseModelORM, UUIDColumnMixin):
    __tablename__ = "active_sessions"
    user_id: Mapped[uuid_type] = mapped_column(
        ForeignKey(
            column="users.id",
            name="user_id_fkey",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    refresh_token: Mapped[str] = mapped_column(
        String(length=256), unique=True, nullable=False
    )
    device_name: Mapped[str] = mapped_column(String(length=127), nullable=False)
    device_id: Mapped[str] = mapped_column(String(length=44), nullable=False)
    added_at: Mapped[timeOnInsert]
    expire_at: Mapped[int] = mapped_column(BigInteger(), nullable=False, unique=False)

    # Relationships for ORM
    user: Mapped["UsersOrm"] = relationship(back_populates="active_sessions")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "device_id",
            name="unique_device_per_session",
        ),
        CheckConstraint(sqltext="expire_at > 0"),
        CheckConstraint(sqltext="added_at > 0"),
    )

    def __str__(self) -> str:
        return f"Session added_at: {datetime.datetime.fromtimestamp(self.added_at)}"
