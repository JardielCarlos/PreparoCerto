"""empty message

Revision ID: 2241cb2e7c67
Revises: 1bce3ee20b7c
Create Date: 2023-06-21 10:31:15.222623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2241cb2e7c67'
down_revision = '1bce3ee20b7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_preparacao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numPorcoes', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_preparacao', schema=None) as batch_op:
        batch_op.drop_column('numPorcoes')

    # ### end Alembic commands ###