"""user roles

Revision ID: 3c7e757a82df
Revises: 06ca3045490c
Create Date: 2023-08-23 19:36:51.209690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c7e757a82df'
down_revision = '06ca3045490c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("roles",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String(255), nullable=False))
    op.add_column("users", sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id")))


def downgrade() -> None:
    op.drop_table("roles")
    op.drop_column("users", "role_id")
