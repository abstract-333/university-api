import time
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, text
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
    declarative_mixin,
)

if TYPE_CHECKING:
    from models import UsersOrm


class UserRelationMixin:
    _user_id_nullable: bool = False
    _user_email_unique: bool = False
    _user_back_populates: str | None = None
    _user_on_delete: str | None = "CASCADE"
    _user_on_update: str | None = "CASCADE"

    @declared_attr
    def user_email(cls) -> Mapped[str]:
        return mapped_column(
            ForeignKey(
                "user.email",
                onupdate=cls._user_on_update,
                ondelete=cls._user_on_delete,
            ),
            unique=cls._user_email_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["UsersOrm"]:
        return relationship(
            "User", back_populates=cls._user_back_populates, lazy="joined"
        )


def get_time() -> int:
    return int(time.time())


class TimeColumnsMixin:
    @declared_attr
    def added_at(cls) -> Mapped[int]:
        return mapped_column(
            server_default=text("extract(epoch FROM now())"),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls) -> Mapped[int]:
        return mapped_column(
            server_default=text("extract(epoch FROM now())"),
            onupdate=get_time,
            nullable=False,
        )


class UUIDColumnMixin:
    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid7()"),
        )


# added_at: Mapped[timeSeconds]

# updated_at: Mapped[timeSecondsOnUpdate]
