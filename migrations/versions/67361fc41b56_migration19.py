"""migration19

Revision ID: 67361fc41b56
Revises: c819615a1628
Create Date: 2021-02-19 15:43:19.414085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67361fc41b56'
down_revision = 'c819615a1628'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('FixEmployee')
    op.create_foreign_key(None, 'client', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'employee', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'fix', 'user', ['iduser'], ['id'])
    op.create_foreign_key(None, 'fix', 'fix_detail', ['idfixType'], ['id'])
    op.create_foreign_key(None, 'fix_detail', 'user', ['iduser'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fix_detail', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'fix', type_='foreignkey')
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.create_table('FixEmployee',
    sa.Column('fixid', sa.INTEGER(), nullable=True),
    sa.Column('employeeid', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['employeeid'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['fixid'], ['user.id'], )
    )
    # ### end Alembic commands ###
