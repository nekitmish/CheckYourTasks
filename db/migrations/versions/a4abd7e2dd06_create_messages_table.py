"""Create messages table

Revision ID: a4abd7e2dd06
Revises: dac05d64689c
Create Date: 2021-02-01 16:43:02.523978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4abd7e2dd06'
down_revision = 'dac05d64689c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.VARCHAR(length=280), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['employees.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['employees.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
