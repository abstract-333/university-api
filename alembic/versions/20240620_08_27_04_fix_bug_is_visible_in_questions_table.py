"""Fix bug is_visible in questions table

Revision ID: 20240620_08_27_04
Revises: 20240619_22_39_26
Create Date: 2024-06-20 08:27:04.779098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240620_08_27_04"
down_revision: Union[str, None] = "20240619_22_39_26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "questions", sa.Column("is_visible", sa.Boolean(), nullable=False, default=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("questions", "is_visible")
    # ### end Alembic commands ###
