"""add source permission metadata

Revision ID: 0002_source_permissions
Revises: 0001_initial_domain
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_source_permissions"
down_revision: Union[str, None] = "0001_initial_domain"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sources",
        sa.Column("permission_status", sa.String(length=32), nullable=False, server_default="unknown"),
    )
    op.add_column("sources", sa.Column("license_notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("sources", "license_notes")
    op.drop_column("sources", "permission_status")
