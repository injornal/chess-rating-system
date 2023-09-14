"""result column from game to users_games

Revision ID: aed8d781d740
Revises: 3c7e757a82df
Create Date: 2023-09-07 12:32:56.930551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aed8d781d740'
down_revision = '3c7e757a82df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("games", "result")
    op.add_column("users_games", sa.Column("score", sa.Float, default=0))


def downgrade() -> None:
    op.drop_column("users_games", "score")
    op.add_column("game", sa.Column("result", sa.Float))
