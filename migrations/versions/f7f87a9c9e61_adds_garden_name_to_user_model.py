"""Adds garden_name to User model

Revision ID: f7f87a9c9e61
Revises: 878f1b278e14
Create Date: 2025-08-01 03:13:53.984860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7f87a9c9e61'
down_revision = '878f1b278e14'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'garden_name',
                sa.String(),
                nullable=False,
                server_default='Your Garden'  # Add default at DB level
            )
        )
    # Remove the server default so future inserts must provide a value or use model default
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('garden_name', server_default=None)


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('garden_name')
