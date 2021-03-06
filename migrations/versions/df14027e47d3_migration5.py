"""migration5

Revision ID: df14027e47d3
Revises: 0e9b60923d8f
Create Date: 2021-02-13 17:32:01.116191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df14027e47d3'
down_revision = '0e9b60923d8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('iduser', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'client', 'user', ['iduser'], ['id'])
    op.add_column('fix', sa.Column('iduser', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fix', 'fix_detail', ['idfixType'], ['id'])
    op.create_foreign_key(None, 'fix', 'user', ['iduser'], ['id'])
    op.add_column('fix_detail', sa.Column('iduser', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fix_detail', 'user', ['iduser'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fix_detail', type_='foreignkey')
    op.drop_column('fix_detail', 'iduser')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_column('fix', 'iduser')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_column('client', 'iduser')
    # ### end Alembic commands ###
