"""create initial domain schema

Revision ID: 0001_initial_domain
Revises:
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_domain"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "boards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_boards_name", "boards", ["name"], unique=False)

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("availability_notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("url"),
    )
    op.create_index("ix_sources_name", "sources", ["name"], unique=False)
    op.create_index("ix_sources_url", "sources", ["url"], unique=False)

    op.create_table(
        "exams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("board_id", sa.Integer(), sa.ForeignKey("boards.id"), nullable=False),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id")),
        sa.Column("name", sa.String(length=240), nullable=False),
        sa.Column("organization", sa.String(length=240)),
        sa.Column("position", sa.String(length=240)),
        sa.Column("year", sa.Integer()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_exams_board_id", "exams", ["board_id"], unique=False)
    op.create_index("ix_exams_source_id", "exams", ["source_id"], unique=False)
    op.create_index("ix_exams_name", "exams", ["name"], unique=False)

    op.create_table(
        "source_documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("exam_id", sa.Integer(), sa.ForeignKey("exams.id")),
        sa.Column("filename", sa.String(length=260), nullable=False),
        sa.Column("storage_path", sa.String(length=2048), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("storage_path"),
        sa.UniqueConstraint("content_hash"),
    )
    op.create_index("ix_source_documents_source_id", "source_documents", ["source_id"], unique=False)
    op.create_index("ix_source_documents_exam_id", "source_documents", ["exam_id"], unique=False)
    op.create_index("ix_source_documents_content_hash", "source_documents", ["content_hash"], unique=False)

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("source_documents.id"), nullable=False),
        sa.Column("exam_id", sa.Integer(), sa.ForeignKey("exams.id")),
        sa.Column("number", sa.String(length=32), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("format", sa.String(length=32), nullable=False),
        sa.Column("source_page", sa.Integer()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_questions_document_id", "questions", ["document_id"], unique=False)
    op.create_index("ix_questions_exam_id", "questions", ["exam_id"], unique=False)
    op.create_index("ix_questions_number", "questions", ["number"], unique=False)

    op.create_table(
        "alternatives",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("questions.id"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
    )
    op.create_index("ix_alternatives_question_id", "alternatives", ["question_id"], unique=False)

    op.create_table(
        "answer_keys",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("questions.id"), nullable=False),
        sa.Column("answer", sa.String(length=32)),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("is_annulled", sa.Boolean(), nullable=False),
        sa.Column("source_reference", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_answer_keys_question_id", "answer_keys", ["question_id"], unique=False)

    op.create_table(
        "processing_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("source_documents.id")),
        sa.Column("stage", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text()),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_processing_records_document_id", "processing_records", ["document_id"], unique=False)
    op.create_index("ix_processing_records_stage", "processing_records", ["stage"], unique=False)


def downgrade() -> None:
    op.drop_table("processing_records")
    op.drop_table("answer_keys")
    op.drop_table("alternatives")
    op.drop_table("questions")
    op.drop_table("source_documents")
    op.drop_table("exams")
    op.drop_table("sources")
    op.drop_table("boards")
