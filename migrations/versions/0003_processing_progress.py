"""add processing progress and attempts

Revision ID: 0003_processing_progress
Revises: 0002_source_permissions
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_processing_progress"
down_revision: Union[str, None] = "0002_source_permissions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "processing_records",
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "processing_records",
        sa.Column("attempt", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("processing_records", "attempt")
    op.drop_column("processing_records", "progress")
