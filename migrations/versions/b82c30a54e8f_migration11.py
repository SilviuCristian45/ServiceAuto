"""migration11

Revision ID: b82c30a54e8f
Revises: 4e0b830f0106
Create Date: 2021-02-18 12:21:32.998281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b82c30a54e8f'
down_revision = '4e0b830f0106'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_foreign_key(None, 'client', 'user', ['iduser'], ['id'])
    # op.create_foreign_key(None, 'fix', 'fix_detail', ['idfixType'], ['id'])
    # op.create_foreign_key(None, 'fix', 'user', ['iduser'], ['id'])
    # op.create_foreign_key(None, 'fix_detail', 'user', ['iduser'], ['id'])
    op.add_column('user', sa.Column('activated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
     op.drop_column('user', 'activated')
    # op.drop_constraint(None, 'fix_detail', type_='foreignkey')
    # op.drop_constraint(None, 'fix', type_='foreignkey')
    # op.drop_constraint(None, 'fix', type_='foreignkey')
    # op.drop_constraint(None, 'client', type_='foreignkey')
    # ### end Alembic commands ###
