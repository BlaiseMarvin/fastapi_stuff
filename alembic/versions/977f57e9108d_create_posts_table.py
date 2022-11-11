"""create posts table

Revision ID: 977f57e9108d
Revises: 
Create Date: 2022-11-10 15:20:31.211884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '977f57e9108d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False))


def downgrade():
    op.drop_table('posts')
