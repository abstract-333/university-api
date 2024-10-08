"""Make lecturer_course_id not null in lectures

Revision ID: 20240225_20_20_49
Revises: 20240225_20_20_01
Create Date: 2024-02-25 20:20:49.945186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240225_20_20_49"
down_revision: Union[str, None] = "20240225_20_20_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "UPDATE lectures SET lecturer_course_id = (SELECT id FROM courses_lecturers limit 1); "
    )
    op.alter_column(
        "lectures", "lecturer_course_id", existing_type=sa.UUID(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "lectures", "lecturer_course_id", existing_type=sa.UUID(), nullable=True
    )
    # ### end Alembic commands ###
