"""Delete specialities_courses relations with taught_courses

Revision ID: 20240308_21_36_46
Revises: 20240308_21_21_42
Create Date: 2024-03-08 21:36:46.435538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240308_21_36_46"
down_revision: Union[str, None] = "20240308_21_21_42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "specialities_courses",
        sa.Column("current_class", sa.SmallInteger(), nullable=True),
    )
    op.execute("UPDATE specialities_courses SET current_class = 1;")
    op.add_column(
        "specialities_courses",
        sa.Column(
            "semester",
            sa.SmallInteger(),
            nullable=True,
        ),
    )
    op.execute("UPDATE specialities_courses SET semester = 1;")

    op.drop_constraint(
        "taught_course_id_speciality_id_constraint",
        "specialities_courses",
        type_="unique",
    )
    op.create_unique_constraint(
        "speciality_id_current_class_semester_constraint",
        "specialities_courses",
        ["speciality_id", "current_class", "semester"],
    )
    op.drop_constraint(
        "specialities_courses_taught_course_id_fkey",
        "specialities_courses",
        type_="foreignkey",
    )
    op.drop_column("specialities_courses", "taught_course_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "specialities_courses",
        sa.Column("taught_course_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "specialities_courses_taught_course_id_fkey",
        "specialities_courses",
        "taught_courses",
        ["taught_course_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "speciality_id_current_class_semester_constraint",
        "specialities_courses",
        type_="unique",
    )
    op.create_unique_constraint(
        "taught_course_id_speciality_id_constraint",
        "specialities_courses",
        ["taught_course_id", "speciality_id"],
    )
    op.drop_column("specialities_courses", "semester")
    op.drop_column("specialities_courses", "current_class")
    # ### end Alembic commands ###
