"""empty message

Revision ID: f27a96c98b0b
Revises: 4648466a15ff
Create Date: 2021-02-13 17:39:57.711172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f27a96c98b0b'
down_revision = '4648466a15ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
