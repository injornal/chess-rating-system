"""result to floatD

Revision ID: 06ca3045490c
Revises: 2405c6ff775a
Create Date: 2023-08-16 12:01:45.856386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06ca3045490c'
down_revision = '2405c6ff775a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("games", "result")
    op.add_column("games", sa.Column("result", sa.Float))


def downgrade() -> None:
    op.drop_column("games", "result")
    op.add_column("games", sa.Column("result", sa.Integer))

