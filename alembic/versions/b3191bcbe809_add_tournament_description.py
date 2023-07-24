"""add tournament description

Revision ID: b3191bcbe809
Revises: 5b3b85f23bef
Create Date: 2023-07-23 21:57:37.109722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3191bcbe809'
down_revision = '5b3b85f23bef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tournaments", sa.Column("description", sa.String(255), default="Friendly community"))


def downgrade() -> None:
    op.drop_column("tournaments", "description")
