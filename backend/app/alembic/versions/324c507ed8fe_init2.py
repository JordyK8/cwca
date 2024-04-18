"""init2

Revision ID: 324c507ed8fe
Revises: b03e6b74e4b9
Create Date: 2024-04-18 04:00:15.988871+10:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '324c507ed8fe'
down_revision: Union[str, None] = 'b03e6b74e4b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # change documents table, set owner_id to String
    op.drop_table("documents")
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.String, index=True),
        sa.Column("owner_id", sa.String, sa.ForeignKey("users.id")),
        sa.Column("url", sa.String),
    )


def downgrade() -> None:
    # change documents table, set owner_id to Integer
    op.drop_table("documents")
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.String, index=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("url", sa.String),
    )
    # ### end Alembic commands ###
