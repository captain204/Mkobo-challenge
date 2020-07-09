"""empty message

Revision ID: f37b4800b7c2
Revises: 5a8a895f1f54
Create Date: 2020-07-09 15:41:46.955220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f37b4800b7c2'
down_revision = '5a8a895f1f54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('account_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'account_number')
    # ### end Alembic commands ###