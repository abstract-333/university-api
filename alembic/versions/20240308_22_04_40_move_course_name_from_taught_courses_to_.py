"""Move course.name from taught_courses to specialities_courses

Revision ID: 20240308_22_04_40
Revises: 20240308_21_43_52
Create Date: 2024-03-08 22:04:40.445200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240308_22_04_40"
down_revision: Union[str, None] = "20240308_21_43_52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "specialities_courses",
        sa.Column("course_name", sa.String(length=32), nullable=True),
    )
    op.execute(
        "UPDATE specialities_courses SET course_name = 'English 1' WHERE course_name IS NULL;"
    )
    op.create_foreign_key(
        "course_name_fkey",
        "specialities_courses",
        "courses",
        ["course_name"],
        ["name"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.add_column("taught_courses", sa.Column("year", sa.SmallInteger(), nullable=True))
    op.execute("UPDATE taught_courses SET year = 2 WHERE year IS NULL;")
    op.drop_constraint("course_name_fk", "taught_courses", type_="foreignkey")
    op.drop_column("taught_courses", "course_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "taught_courses",
        sa.Column(
            "course_name", sa.VARCHAR(length=32), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        "course_name_fk",
        "taught_courses",
        "courses",
        ["course_name"],
        ["name"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_column("taught_courses", "year")
    op.drop_constraint("course_name_fkey", "specialities_courses", type_="foreignkey")
    op.drop_column("specialities_courses", "course_name")
    # ### end Alembic commands ###
