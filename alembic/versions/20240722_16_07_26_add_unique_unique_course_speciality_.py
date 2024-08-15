"""Add unique_unique_course_speciality_constraint to specialities_courses table

Revision ID: 20240722_16_07_26
Revises: 20240620_08_27_04
Create Date: 2024-07-22 16:07:26.571756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240722_16_07_26"
down_revision: Union[str, None] = "20240620_08_27_04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "speciality_id_current_class_semester_constraint",
        "specialities_courses",
        type_="unique",
    )
    op.create_unique_constraint(
        "unique_course_speciality_constraint",
        "specialities_courses",
        ["speciality_id", "course_name"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "unique_course_speciality_constraint", "specialities_courses", type_="unique"
    )
    op.create_unique_constraint(
        "speciality_id_current_class_semester_constraint",
        "specialities_courses",
        ["speciality_id", "current_class", "semester"],
    )
    # ### end Alembic commands ###
