"""add foreign key to post table

Revision ID: 00e272cf0f23
Revises: b71602ec2a9f
Create Date: 2023-02-02 08:49:35.654694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00e272cf0f23'
down_revision = 'b71602ec2a9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('user_id',
                            sa.Integer(),
                            nullable=False))
    op.create_foreign_key('post_users_fk',
                          source_table='posts',
                          referent_table="users",
                          local_cols=["user_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',
                       table_name="posts")
    op.drop_column('posts',
                   'user_id')
    pass
