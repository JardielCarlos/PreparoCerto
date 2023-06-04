"""Update

Revision ID: 42b732da8e8b
Revises: 60f5987cb164
Create Date: 2023-06-04 12:42:49.615373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42b732da8e8b'
down_revision = '60f5987cb164'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_cardapiorefeicao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cardapio_id', sa.Integer(), nullable=True),
    sa.Column('preparacao_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cardapio_id'], ['tb_cardapio.id'], ),
    sa.ForeignKeyConstraint(['preparacao_id'], ['tb_preparacao.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_cardapiorefeicao')
    # ### end Alembic commands ###