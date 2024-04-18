"""init

Revision ID: b03e6b74e4b9
Revises: 
Create Date: 2024-04-17 22:32:09.997464+10:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b03e6b74e4b9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("email", sa.String, unique=True),
        sa.Column("username", sa.String, unique=True),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
    )
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.String, index=True),
        sa.Column("owner_id", sa.String, sa.ForeignKey("users.id")),
        sa.Column("url", sa.String),
    )


def downgrade() -> None:
    op.drop_table("documents")
    op.drop_table("users")
