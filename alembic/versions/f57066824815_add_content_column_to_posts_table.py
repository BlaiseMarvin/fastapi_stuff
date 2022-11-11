"""add content column to posts table

Revision ID: f57066824815
Revises: 977f57e9108d
Create Date: 2022-11-11 06:15:43.643237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f57066824815'
down_revision = '977f57e9108d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
