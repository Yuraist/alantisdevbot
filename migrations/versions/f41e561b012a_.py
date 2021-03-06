"""empty message

Revision ID: f41e561b012a
Revises: f82fe41b2e4f
Create Date: 2017-09-24 12:23:36.017122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f41e561b012a'
down_revision = 'f82fe41b2e4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('type', sa.String(length=64), nullable=True))
    op.drop_column('order', 'order_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_type', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('order', 'type')
    # ### end Alembic commands ###
