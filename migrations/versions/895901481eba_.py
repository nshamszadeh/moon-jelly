"""empty message

Revision ID: 895901481eba
Revises: 197aa6549060
Create Date: 2019-05-21 16:04:32.096618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895901481eba'
down_revision = '197aa6549060'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('initial', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'initial')
    # ### end Alembic commands ###
