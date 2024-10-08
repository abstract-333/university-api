"""Add lecturers_requests table

Revision ID: 20240228_00_24_12
Revises: 20240227_01_31_14
Create Date: 2024-02-28 00:24:12.368030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240228_00_24_12"
down_revision: Union[str, None] = "20240227_01_31_14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lecturers_requests",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("faculty_name", sa.String(length=32), nullable=False),
        sa.Column("description", sa.String(length=50), nullable=True),
        sa.Column("is_accepted", sa.Boolean(), nullable=True),
        sa.Column("processed_at", sa.Integer(), nullable=True),
        sa.Column(
            "added_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.CheckConstraint("processed_at > 0", name="processed_at_positive"),
        sa.ForeignKeyConstraint(
            ["faculty_name"],
            ["faculties.name"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            name="faculty_name_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            name="user_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("lecturers_requests")
    # ### end Alembic commands ###
