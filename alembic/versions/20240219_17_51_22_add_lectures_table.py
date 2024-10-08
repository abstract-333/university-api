"""Add lectures table

Revision ID: 20240219_17_51_22
Revises: 20240219_17_17_51
Create Date: 2024-02-19 17:51:22.603539

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240219_17_51_22"
down_revision: Union[str, None] = "20240219_17_17_51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lectures",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("file_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("body", sa.String(length=10000), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["author_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["course_id"], ["taught_courses.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["file_id"], ["files.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("lectures")
    # ### end Alembic commands ###
