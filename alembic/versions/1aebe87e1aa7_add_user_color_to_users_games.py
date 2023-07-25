"""add user color to users_games

Revision ID: 1aebe87e1aa7
Revises: b3191bcbe809
Create Date: 2023-07-24 16:44:41.177943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aebe87e1aa7'
down_revision = 'b3191bcbe809'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users_games", sa.Column("color", sa.Boolean))


def downgrade() -> None:
    op.drop_column("users_games", "color")
