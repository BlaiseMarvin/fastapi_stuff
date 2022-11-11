"""add last few columns to posts table

Revision ID: 7b3940b59c13
Revises: 47ca281106c6
Create Date: 2022-11-11 06:45:00.792726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b3940b59c13'
down_revision = '47ca281106c6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    op.add_column('posts',sa.Column('published',sa.Boolean(),server_default='TRUE'))

    


def downgrade():
    op.drop_column('posts','created_at')
    op.drop_column('posts','published')
