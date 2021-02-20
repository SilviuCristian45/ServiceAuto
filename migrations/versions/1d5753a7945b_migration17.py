"""migration17

Revision ID: 1d5753a7945b
Revises: 0b215a08c270
Create Date: 2021-02-19 15:17:07.017604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d5753a7945b'
down_revision = '0b215a08c270'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'FixEmployee', 'user', ['fixid'], ['id'])
    op.create_foreign_key(None, 'FixEmployee', 'fix', ['fixid'], ['id'])
    op.create_foreign_key(None, 'client', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'employee', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'fix', 'fix_detail', ['idfixType'], ['id'])
    op.create_foreign_key(None, 'fix', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'fix_detail', 'user', ['iduser'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fix_detail', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_constraint(None, 'FixEmployee', type_='foreignkey')
    op.create_foreign_key(None, 'FixEmployee', 'user', ['fixid'], ['id'])
    op.drop_constraint(None, 'FixEmployee', type_='foreignkey')
    # ### end Alembic commands ###