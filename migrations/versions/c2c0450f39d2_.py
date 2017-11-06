"""empty message

Revision ID: c2c0450f39d2
Revises: b52300f212f5
Create Date: 2017-11-06 14:36:35.341781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2c0450f39d2'
down_revision = 'b52300f212f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('childservice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('association',
    sa.Column('childservice_id', sa.Integer(), nullable=True),
    sa.Column('roles_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['childservice_id'], ['childservice.id'], ),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_table('childservice')
    # ### end Alembic commands ###