"""Test

Revision ID: 5c27f74b9f65
Revises: 70d65421b0b4
Create Date: 2023-05-30 15:52:59.945833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c27f74b9f65'
down_revision = '70d65421b0b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_empresa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('proprietario_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('tb_empresa_proprietario_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'tb_proprietario', ['proprietario_id'], ['usuario_id'])
        batch_op.drop_column('proprietario')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_empresa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('proprietario', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('tb_empresa_proprietario_fkey', 'tb_proprietario', ['proprietario'], ['usuario_id'])
        batch_op.drop_column('proprietario_id')

    # ### end Alembic commands ###
