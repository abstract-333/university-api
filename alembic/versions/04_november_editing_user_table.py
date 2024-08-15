"""Editing user table

Revision ID: eb2db0ed91d4
Revises: b63852030f0f
Create Date: 2023-11-04 15:17:51.976463

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eb2db0ed91d4"
down_revision: Union[str, None] = "aab1de691475"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "added_at",
        existing_type=sa.INTEGER(),
        server_default=sa.text("extract(epoch FROM now())"),
        existing_nullable=False,
    )
    op.alter_column(
        "user",
        "updated_at",
        existing_type=sa.INTEGER(),
        server_default=sa.text("extract(epoch FROM now())"),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "updated_at",
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "user",
        "added_at",
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=False,
    )
    # ### end Alembic commands ###
