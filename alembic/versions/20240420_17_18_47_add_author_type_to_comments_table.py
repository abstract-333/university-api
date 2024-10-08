"""Add author_type  to comments table

Revision ID: 20240420_17_18_47
Revises: 20240420_16_54_43
Create Date: 2024-04-20 17:18:47.635386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240420_17_18_47"
down_revision: Union[str, None] = "20240420_16_54_43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "comments", sa.Column("author_type", sa.String(length=10), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("comments", "author_type")
    # ### end Alembic commands ###
