"""atualizando tabelas

Revision ID: b5d46ff2c043
Revises: 
Create Date: 2023-06-19 16:31:23.535086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5d46ff2c043'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_utensiliopreparacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('utensilio_id', sa.Integer(), nullable=True),
    sa.Column('preparacao_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['preparacao_id'], ['tb_preparacao.id'], ),
    sa.ForeignKeyConstraint(['utensilio_id'], ['tb_utensilio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_utensiliopreparacao')
    # ### end Alembic commands ###