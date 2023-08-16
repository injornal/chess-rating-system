"""add rounds table

Revision ID: 2405c6ff775a
Revises: 1aebe87e1aa7
Create Date: 2023-08-15 12:16:04.607054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2405c6ff775a'
down_revision = '1aebe87e1aa7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rounds",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("round", sa.Integer, nullable=False),
        sa.Column("tournament_id", sa.Integer, nullable=False)
    )

    op.drop_column("games", "tournament_id")
    op.add_column("games", sa.Column("round_id", sa.Integer, sa.ForeignKey("rounds.id")))


def downgrade() -> None:
    op.drop_table("rounds")
    op.drop_column("games", "round_id")
    op.add_column("games", sa.Column("tournament_id", sa.Integer, sa.ForeignKey("tournaments.id")))
