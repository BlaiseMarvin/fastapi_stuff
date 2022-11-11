"""add foreign key to posts table

Revision ID: 47ca281106c6
Revises: 98cbe1ff21f5
Create Date: 2022-11-11 06:38:01.153036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47ca281106c6'
down_revision = '98cbe1ff21f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')



def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
