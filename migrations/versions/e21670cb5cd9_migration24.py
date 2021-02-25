"""migration24

Revision ID: e21670cb5cd9
Revises: 8eec5c3a905e
Create Date: 2021-02-23 20:03:56.926846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e21670cb5cd9'
down_revision = '8eec5c3a905e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('priority',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'client', 'user', ['iduser'], ['id'])
    op.drop_column('employee', 'iduser')
    op.add_column('fix', sa.Column('idpriority', sa.Integer(), nullable=True))
    op.alter_column('fix', 'loadDate',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.create_foreign_key(None, 'fix', 'priority', ['idpriority'], ['id'])
    op.create_foreign_key(None, 'fix', 'fix_detail', ['idfixType'], ['id'])
    op.create_foreign_key(None, 'fix', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'fix_detail', 'user', ['iduser'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fix_detail', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.alter_column('fix', 'loadDate',
               existing_type=sa.DATETIME(),
               nullable=True)
    op.drop_column('fix', 'idpriority')
    op.add_column('employee', sa.Column('iduser', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_table('priority')
    # ### end Alembic commands ###