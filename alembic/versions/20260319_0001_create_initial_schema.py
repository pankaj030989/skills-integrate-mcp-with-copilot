"""create initial schema

Revision ID: 20260319_0001
Revises:
Create Date: 2026-03-19 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260319_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("schedule", sa.String(length=255), nullable=False),
        sa.Column("max_participants", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_activities_id"), "activities", ["id"], unique=False)
    op.create_index(op.f("ix_activities_name"), "activities", ["name"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "activity_id", name="uq_user_activity"),
    )
    op.create_index(op.f("ix_enrollments_id"), "enrollments", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_enrollments_id"), table_name="enrollments")
    op.drop_table("enrollments")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_activities_name"), table_name="activities")
    op.drop_index(op.f("ix_activities_id"), table_name="activities")
    op.drop_table("activities")