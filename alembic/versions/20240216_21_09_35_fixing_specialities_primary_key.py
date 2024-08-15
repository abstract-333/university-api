"""Fixing specialities primary key

Revision ID: 20240216_21_09_35
Revises: 654af25589c8
Create Date: 2024-02-16 21:09:35.025822

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240216_21_09_35"
down_revision: Union[str, None] = "654af25589c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("specialities_pkey", "specialities", type_="primary")
    op.create_primary_key("specialities_pkey", "specialities", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("specialities_pkey", "specialities", type_="primary")
    op.create_primary_key("specialities_pkey", "specialities", ["name"])
    # ### end Alembic commands ###
