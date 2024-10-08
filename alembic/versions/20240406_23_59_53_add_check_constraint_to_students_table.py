"""Add check constraint to students table

Revision ID: 20240406_23_59_53
Revises: 20240406_19_05_58
Create Date: 2024-04-06 23:59:53.113454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240406_23_59_53"
down_revision: Union[str, None] = "20240406_19_05_58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_check_constraint(
        "class_id_valid",
        "students",
        condition="class_id > 0 and class_id < 7",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "class_id_valid",
        "students",
    )
    # ### end Alembic commands ###
