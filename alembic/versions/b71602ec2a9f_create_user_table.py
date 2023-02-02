"""create user table

Revision ID: b71602ec2a9f
Revises: f60e1400ae84
Create Date: 2023-02-02 08:42:53.926406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b71602ec2a9f'
down_revision = 'f60e1400ae84'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',
                              sa.Integer(),
                              nullable=False),
                    sa.Column('email',
                              sa.String(),
                              nullable=False),
                    sa.Column('password',
                              sa.String(),
                              nullable=False),
                    sa.Column('created_at',
                              sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
