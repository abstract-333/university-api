"""Add unique constraint to courses_lecturers migration

Revision ID: 20240217_14_38_19
Revises: 20240217_13_55_30
Create Date: 2024-02-17 14:38:19.624291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240217_14_38_19"
down_revision: Union[str, None] = "20240217_13_55_30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "courses_lecturers", "course_id", existing_type=sa.UUID(), nullable=False
    )
    op.create_unique_constraint(
        "taught_course_id_lecturer_id_constraint",
        "courses_lecturers",
        ["course_id", "lecturer_id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "taught_course_id_lecturer_id_constraint", "courses_lecturers", type_="unique"
    )
    op.alter_column(
        "courses_lecturers", "course_id", existing_type=sa.UUID(), nullable=True
    )
    # ### end Alembic commands ###
