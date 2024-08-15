"""Add index to speciality_course_id in taught_courses table

Revision ID: 20240403_02_47_56
Revises: 20240403_02_41_15
Create Date: 2024-04-03 02:47:56.754432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240403_02_47_56"
down_revision: Union[str, None] = "20240403_02_41_15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_taught_courses_speciality_course_id"),
        "taught_courses",
        ["speciality_course_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_taught_courses_speciality_course_id"), table_name="taught_courses"
    )
    # ### end Alembic commands ###
