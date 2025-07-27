"""Manually increase password_hash column length

Revision ID: ff4598297a8a
Revises: 79ad0e14cacd
Create Date: 2025-07-27 12:49:52.286792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff4598297a8a'
down_revision = '79ad0e14cacd'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
