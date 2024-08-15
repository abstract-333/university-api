"""Make course.name and year not null

Revision ID: 20240308_22_09_08
Revises: 20240308_22_04_40
Create Date: 2024-03-08 22:09:08.989980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240308_22_09_08"
down_revision: Union[str, None] = "20240308_22_04_40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "specialities_courses",
        "course_name",
        existing_type=sa.VARCHAR(length=32),
        nullable=False,
    )
    op.alter_column(
        "taught_courses", "year", existing_type=sa.SMALLINT(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("taught_courses", "year", existing_type=sa.SMALLINT(), nullable=True)
    op.alter_column(
        "specialities_courses",
        "course_name",
        existing_type=sa.VARCHAR(length=32),
        nullable=True,
    )
    # ### end Alembic commands ###
