"""Adding token blacklists table

Revision ID: 69805b5ddbb0
Revises: 1aa74462f1c4
Create Date: 2024-01-16 01:52:46.149776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69805b5ddbb0'
down_revision: Union[str, None] = '1aa74462f1c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens_blacklist',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid7()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=512), nullable=False),
    sa.Column('added_at', sa.Integer(), server_default=sa.text('extract(epoch FROM now())'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens_blacklist')
    # ### end Alembic commands ###
