"""add game and tournament dependencies

Revision ID: 5b3b85f23bef
Revises: 
Create Date: 2023-07-18 23:29:19.833535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b3b85f23bef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("games", sa.Column("tournament_id", sa.Integer, sa.ForeignKey("tournaments.id")))


def downgrade() -> None:
    op.drop_column("games", "tournament_id")
