"""Editing students and specialities tables

Revision ID: 1e3768839bd1
Revises: 42ca0aa2d900
Create Date: 2024-01-17 15:32:11.140381

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1e3768839bd1"
down_revision: Union[str, None] = "42ca0aa2d900"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "specialities",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid7()"),
            nullable=False,
            primary_key=True,
            unique=True,
        ),
    )
    op.drop_constraint("specialities_name_key", "specialities", type_="unique")
    op.add_column("students", sa.Column("speciality_id", sa.UUID(), nullable=False))
    op.drop_constraint("student_speciality_constraint", "students", type_="unique")
    op.create_unique_constraint(
        "student_speciality_constraint", "students", ["university_id", "speciality_id"]
    )
    op.drop_constraint("user_id_speciality_constraint", "students", type_="unique")
    op.create_unique_constraint(
        "user_id_speciality_constraint", "students", ["user_id", "speciality_id"]
    )
    op.drop_constraint("students_speciality_name_fkey", "students", type_="foreignkey")
    op.create_foreign_key(
        None,
        "students",
        "specialities",
        ["speciality_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_column("students", "speciality_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "students",
        sa.Column(
            "speciality_name",
            sa.VARCHAR(length=32),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(None, "students", type_="foreignkey")
    op.create_foreign_key(
        "students_speciality_name_fkey",
        "students",
        "specialities",
        ["speciality_name"],
        ["name"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_constraint("user_id_speciality_constraint", "students", type_="unique")
    op.create_unique_constraint(
        "user_id_speciality_constraint", "students", ["user_id", "speciality_name"]
    )
    op.drop_constraint("student_speciality_constraint", "students", type_="unique")
    op.create_unique_constraint(
        "student_speciality_constraint",
        "students",
        ["university_id", "speciality_name"],
    )
    op.drop_column("students", "speciality_id")
    op.create_unique_constraint("specialities_name_key", "specialities", ["name"])
    op.drop_column("specialities", "id")
    # ### end Alembic commands ###
