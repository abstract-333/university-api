"""Renaming tables

Revision ID: d0cf2dff32b6
Revises: 24d581fe042f
Create Date: 2023-11-18 23:11:59.857683

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d0cf2dff32b6"
down_revision: Union[str, None] = "24d581fe042f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "faculties",
        sa.Column("name", sa.String(length=32), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("name"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=640), nullable=False),
        sa.Column("hashed_password", sa.String(length=256), nullable=False),
        sa.Column("birthdate", sa.Date(), nullable=False),
        sa.Column(
            "added_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=640), nullable=False),
        sa.Column("faculty_name", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["email"], ["users.email"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["faculty_name"], ["faculties.name"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "university_id", "faculty_name", name="student_faculty_constraint"
        ),
    )
    op.drop_table("student")
    op.drop_table("user")
    op.drop_table("faculty")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "faculty",
        sa.Column("name", sa.VARCHAR(length=32), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("name", name="faculty_pkey"),
        sa.UniqueConstraint("name", name="faculty_name_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "user",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid7()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "username", sa.VARCHAR(length=64), autoincrement=False, nullable=False
        ),
        sa.Column("email", sa.VARCHAR(length=640), autoincrement=False, nullable=False),
        sa.Column(
            "hashed_password",
            sa.VARCHAR(length=256),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "added_at",
            sa.INTEGER(),
            server_default=sa.text("EXTRACT(epoch FROM now())"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.INTEGER(),
            server_default=sa.text("EXTRACT(epoch FROM now())"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_verified", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("birthdate", sa.DATE(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("email", name="user_email_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "student",
        sa.Column(
            "faculty_name", sa.VARCHAR(length=32), autoincrement=False, nullable=False
        ),
        sa.Column("university_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(length=640), autoincrement=False, nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid7()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["email"],
            ["user.email"],
            name="student_email_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["faculty_name"],
            ["faculty.name"],
            name="student_faculty_name_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("university_id", "faculty_name", name="student_constraint"),
    )
    op.drop_table("students")
    op.drop_table("users")
    op.drop_table("faculties")
    # ### end Alembic commands ###
