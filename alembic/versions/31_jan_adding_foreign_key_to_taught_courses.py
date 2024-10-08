"""Adding foreign key to taught_courses

Revision ID: 79d28a3eeebf
Revises: f8521e18de73
Create Date: 2024-01-31 21:42:50.838992

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "79d28a3eeebf"
down_revision: Union[str, None] = "f8521e18de73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("course_id_unique", "courses", ["id"])
    op.add_column("taught_courses", sa.Column("course_id", sa.UUID(), nullable=False))
    op.create_foreign_key(
        "taught_courses_course_id_fk",
        "taught_courses",
        "courses",
        ["course_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "taught_courses_course_id_fk", "taught_courses", type_="foreignkey"
    )
    op.drop_column("taught_courses", "course_id")
    # ### end Alembic commands ###
