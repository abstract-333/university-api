"""Delete supervisors table

Revision ID: 20240731_00_53_03
Revises: 20240722_16_07_26
Create Date: 2024-07-31 00:53:03.487162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240731_00_53_03"
down_revision: Union[str, None] = "20240722_16_07_26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("supervisors")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "supervisors",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid7()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "faculty_name", sa.VARCHAR(length=32), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["faculty_name"],
            ["faculties.name"],
            name="supervisors_faculty_name_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="supervisors_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="supervisors_pkey"),
        sa.UniqueConstraint(
            "user_id", "faculty_name", name="user_id_faculty_constraint"
        ),
    )
    # ### end Alembic commands ###
