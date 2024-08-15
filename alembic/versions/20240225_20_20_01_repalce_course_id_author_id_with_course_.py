"""Repalce course_id, author_id with course_lecture_id in lectures

Revision ID: 20240225_20_20_01
Revises: 20240225_20_12_14
Create Date: 2024-02-25 20:20:01.221331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240225_20_20_01"
down_revision: Union[str, None] = "20240225_20_12_14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("lectures", sa.Column("lecturer_course_id", sa.UUID(), nullable=True))
    op.drop_constraint(
        "non_duplicated_file_lecture_constraint", "lectures", type_="unique"
    )
    op.create_unique_constraint(
        "non_duplicated_file_lecture_constraint",
        "lectures",
        ["lecturer_course_id", "file_id"],
    )
    op.drop_constraint("lectures_course_id_fkey", "lectures", type_="foreignkey")
    op.drop_constraint("lectures_author_id_fkey", "lectures", type_="foreignkey")
    op.create_foreign_key(
        "lecturer_course_id_fkey",
        "lectures",
        "courses_lecturers",
        ["lecturer_course_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_column("lectures", "author_id")
    op.drop_column("lectures", "course_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "lectures",
        sa.Column("course_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "lectures",
        sa.Column("author_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_constraint("lecturer_course_id_fkey", "lectures", type_="foreignkey")
    op.create_foreign_key(
        "lectures_author_id_fkey",
        "lectures",
        "users",
        ["author_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "lectures_course_id_fkey",
        "lectures",
        "taught_courses",
        ["course_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "non_duplicated_file_lecture_constraint", "lectures", type_="unique"
    )
    op.create_unique_constraint(
        "non_duplicated_file_lecture_constraint", "lectures", ["course_id", "file_id"]
    )
    op.drop_column("lectures", "lecturer_course_id")
    # ### end Alembic commands ###
