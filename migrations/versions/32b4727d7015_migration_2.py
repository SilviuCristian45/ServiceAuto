"""Migration#2

Revision ID: 32b4727d7015
Revises: 85b2f8ef6774
Create Date: 2021-02-01 22:28:17.022595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32b4727d7015'
down_revision = '85b2f8ef6774'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fix', sa.Column('idfixType', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fix', 'fix_detail', ['idfixType'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_column('fix', 'idfixType')
    # ### end Alembic commands ###
