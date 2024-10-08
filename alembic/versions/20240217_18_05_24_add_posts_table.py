"""Add posts table 

Revision ID: 20240217_18_05_24
Revises: 20240217_14_38_19
Create Date: 2024-02-17 18:05:24.373806

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240217_18_05_24"
down_revision: Union[str, None] = "20240217_14_38_19"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "posts",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("body", sa.String(length=50000), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posts")
    # ### end Alembic commands ###
