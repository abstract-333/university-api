"""Add time columns to taught_courses table

Revision ID: 20240308_22_17_45
Revises: 20240308_22_15_15
Create Date: 2024-03-08 22:17:45.139266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240308_22_17_45"
down_revision: Union[str, None] = "20240308_22_15_15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "taught_courses",
        sa.Column(
            "added_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "taught_courses",
        sa.Column(
            "updated_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("taught_courses", "updated_at")
    op.drop_column("taught_courses", "added_at")
    # ### end Alembic commands ###
