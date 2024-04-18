"""create account table

Revision ID: 16f389c4dd90
Revises: 324c507ed8fe
Create Date: 2024-04-19 01:23:59.686681+10:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16f389c4dd90'
down_revision: Union[str, None] = '324c507ed8fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "channels",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String, unique=True),
        sa.Column("owner_id", sa.String, sa.ForeignKey("users.id")),
    )


def downgrade() -> None:
    op.drop_table("channels")
