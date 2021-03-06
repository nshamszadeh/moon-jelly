"""empty message

Revision ID: 1cb5073ef9b1
Revises: fd0fb00bfd08
Create Date: 2019-06-02 23:57:07.332506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cb5073ef9b1'
down_revision = 'fd0fb00bfd08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_db',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.Text(), nullable=True),
    sa.Column('last_name', sa.Text(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Days')
    op.add_column('users', sa.Column('fourth', sa.Integer(), nullable=True))
    op.drop_column('users', 'forth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('forth', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('users', 'fourth')
    op.create_table('Days',
    sa.Column('id', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('first_AM', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('first_PM', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('second', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('third', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fourth', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fith', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sixth', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('seventh', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('PostCall', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Is_Weekend', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Days_pkey')
    )
    op.drop_table('message_db')
    # ### end Alembic commands ###
