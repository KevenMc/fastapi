"""create post table

Revision ID: 8b2e097a6880
Revises: 
Create Date: 2023-02-02 08:32:08.943828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b2e097a6880'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.INTEGER(),
                              nullable=False,
                              primary_key=True),
                    sa.Column('title',
                              sa.String(),
                              nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
