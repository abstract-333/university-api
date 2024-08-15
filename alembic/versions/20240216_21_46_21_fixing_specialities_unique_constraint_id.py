"""Fixing specialities unique constraint id

Revision ID: 20240216_21_46_21
Revises: 20240216_21_28_24
Create Date: 2024-02-16 21:46:21.317740

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240216_21_46_21"
down_revision: Union[str, None] = "20240216_21_28_24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        constraint_name="speciality_id_students_fk",
        table_name="students",
        type_="foreignkey",
    )
    op.drop_constraint(
        constraint_name="speciality_id_courses_fk",
        table_name="courses",
        type_="foreignkey",
    )
    op.drop_constraint(
        constraint_name="specialities_courses_speciality_id_fkey",
        table_name="specialities_courses",
        type_="foreignkey",
    )
    op.drop_constraint(
        constraint_name="specialities_id_unique",
        table_name="specialities",
        type_="unique",
    )
    op.create_foreign_key(
        constraint_name="speciality_id_students_fk",
        source_table="students",
        referent_table="specialities",
        local_cols=["speciality_id"],
        remote_cols=["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        constraint_name="speciality_id_courses_fk",
        source_table="courses",
        referent_table="specialities",
        local_cols=["speciality_id"],
        remote_cols=["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        constraint_name="specialities_courses_speciality_id_fkey",
        source_table="specialities_courses",
        referent_table="specialities",
        local_cols=["speciality_id"],
        remote_cols=["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("specialities_id_unique", "specialities", ["id"])
    # ### end Alembic commands ###
