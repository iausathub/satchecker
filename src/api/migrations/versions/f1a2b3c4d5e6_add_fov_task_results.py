"""add fov_task_results shared store

Celery's result backend is a per-pod Redis sidecar, so an async FOV task's
state is only visible on the replica that ran it. When the status request is
load-balanced to a different pod, AsyncResult reports PENDING forever. This
table persists the task's terminal status and formatted response in the shared
Postgres database so polling works from any replica.

Revision ID: f1a2b3c4d5e6
Revises: e4b9f1c72a30
Create Date: 2026-10-12 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f1a2b3c4d5e6"
down_revision = "e4b9f1c72a30"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "fov_task_results",
        sa.Column("task_id", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("task_id"),
    )
    op.create_index(
        "idx_fov_task_results_created_at", "fov_task_results", ["created_at"]
    )


def downgrade():
    op.drop_index("idx_fov_task_results_created_at", table_name="fov_task_results")
    op.drop_table("fov_task_results")
