"""complete posts table

Revision ID: c552785b8546
Revises: 00e272cf0f23
Create Date: 2023-02-02 09:46:50.059155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c552785b8546'
down_revision = '00e272cf0f23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published',
                            sa.Boolean(),
                            nullable=False,
                            server_default="TRUE"),)
    op.add_column('posts',
                  sa.Column('created_at',
                            sa.TIMESTAMP(timezone=True),
                            nullable=False,
                            server_default=sa.text("now()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
