"""Make device_id not null in active_sessions table

Revision ID: 20240402_17_35_06
Revises: 20240402_17_32_12
Create Date: 2024-04-02 17:35:06.971853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240402_17_35_06"
down_revision: Union[str, None] = "20240402_17_32_12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "UPDATE active_sessions SET device_name = 'UKNOWN' WHERE device_name is NULL;"
    )
    op.alter_column(
        "active_sessions",
        "device_name",
        existing_type=sa.VARCHAR(length=44),
        type_=sa.String(length=127),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "active_sessions",
        "device_name",
        existing_type=sa.String(length=127),
        type_=sa.VARCHAR(length=44),
        nullable=True,
    )
    # ### end Alembic commands ###
