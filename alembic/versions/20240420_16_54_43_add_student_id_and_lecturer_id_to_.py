"""Add student_id and lecturer_id to comments table

Revision ID: 20240420_16_54_43
Revises: 20240406_23_59_53
Create Date: 2024-04-20 16:54:43.355614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240420_16_54_43"
down_revision: Union[str, None] = "20240406_23_59_53"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("comments", sa.Column("lecturer_id", sa.UUID(), nullable=True))
    op.add_column("comments", sa.Column("student_id", sa.UUID(), nullable=True))
    op.drop_constraint("comments_author_id_fkey", "comments", type_="foreignkey")
    op.create_foreign_key(
        "lecturer_id_fkey",
        "comments",
        "lecturers",
        ["lecturer_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "student_id_fkey",
        "comments",
        "students",
        ["student_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_column("comments", "author_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "comments",
        sa.Column("author_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_constraint("student_id_fkey", "comments", type_="foreignkey")
    op.drop_constraint("lecturer_id_fkey", "comments", type_="foreignkey")
    op.create_foreign_key(
        "comments_author_id_fkey",
        "comments",
        "users",
        ["author_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_column("comments", "student_id")
    op.drop_column("comments", "lecturer_id")
    # ### end Alembic commands ###
