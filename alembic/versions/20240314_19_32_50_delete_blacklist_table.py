"""Delete blacklist table

Revision ID: 20240314_19_32_50
Revises: 20240313_00_27_33
Create Date: 2024-03-14 19:32:50.641448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20240314_19_32_50"
down_revision: Union[str, None] = "20240313_00_27_33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tokens_blacklist")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tokens_blacklist",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid7()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("token", sa.VARCHAR(length=512), autoincrement=False, nullable=False),
        sa.Column(
            "added_at",
            sa.INTEGER(),
            server_default=sa.text("EXTRACT(epoch FROM now())"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="tokens_blacklist_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="tokens_blacklist_pkey"),
        sa.UniqueConstraint("token", name="tokens_blacklist_token_key"),
    )
    # ### end Alembic commands ###
