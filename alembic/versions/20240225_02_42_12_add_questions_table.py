"""Add questions table

Revision ID: 20240225_02_42_12
Revises: 20240219_17_57_17
Create Date: 2024-02-25 02:42:12.719530

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240225_02_42_12"
down_revision: Union[str, None] = "20240219_17_57_17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "questions",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("body", sa.String(length=500), nullable=False),
        sa.Column(
            "choices", sa.ARRAY(sa.String(length=50), dimensions=1), nullable=False
        ),
        sa.Column("right_choice", sa.String(length=50), nullable=False),
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
        sa.UniqueConstraint(
            "course_id",
            "body",
            "choices",
            "right_choice",
            name="unique_questions_in_course",
        ),
        sa.CheckConstraint(
            sqltext="right_choice = ANY(choices)",
            name="right_choice_in_choices_constraint",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("questions")
    # ### end Alembic commands ###
