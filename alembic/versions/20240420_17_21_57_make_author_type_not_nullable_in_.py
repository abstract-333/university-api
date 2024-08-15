"""Make author_type not nullable in comments table

Revision ID: 20240420_17_21_57
Revises: 20240420_17_18_47
Create Date: 2024-04-20 17:21:57.091722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240420_17_21_57"
down_revision: Union[str, None] = "20240420_17_18_47"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        sqltext="UPDATE comments SET author_type = 'student' WHERE author_type is NULL;"
    )
    op.alter_column(
        "comments", "author_type", existing_type=sa.VARCHAR(length=10), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "comments", "author_type", existing_type=sa.VARCHAR(length=10), nullable=True
    )
    # ### end Alembic commands ###
