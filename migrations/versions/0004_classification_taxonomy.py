"""add classification taxonomy

Revision ID: 0004_classification_taxonomy
Revises: 0003_processing_progress
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_classification_taxonomy"
down_revision: Union[str, None] = "0003_processing_progress"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_subjects_name", "subjects", ["name"], unique=False)
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subjects.id"), nullable=False),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("topics.id")),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_topics_subject_id", "topics", ["subject_id"], unique=False)
    op.create_index("ix_topics_parent_id", "topics", ["parent_id"], unique=False)


def downgrade() -> None:
    op.drop_table("topics")
    op.drop_table("subjects")
