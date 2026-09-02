"""Add unique constraint on tdm_predictions (folder_name, track_id)

Prevents duplicate ingest of the same track from the same zip delivery.

Revision ID: b7e3c1ad4f2a
Revises: c41e8a9d02f7
Create Date: 2026-07-22 11:05:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "b7e3c1ad4f2a"
down_revision = "c41e8a9d02f7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "tdm_predictions_folder_name_track_id_key",
        "tdm_predictions",
        ["folder_name", "track_id"],
    )


def downgrade():
    op.drop_constraint(
        "tdm_predictions_folder_name_track_id_key",
        "tdm_predictions",
        type_="unique",
    )
