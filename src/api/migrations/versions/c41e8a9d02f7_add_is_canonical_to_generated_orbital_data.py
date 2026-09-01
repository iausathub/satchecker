"""add is_canonical to tle and orbital_elements

Multi-set generation fits several short-window element sets per ephemeris
file for serving accuracy, plus one regular full-window set kept for
archival. ``is_canonical`` marks the archival set: retention
(``delete_expired_generated_orbital_data``) prunes only generated rows where
it is false. Catalog rows keep the default false; the flag is only
meaningful for ``data_source = 'generated'``.

Revision ID: c41e8a9d02f7
Revises: 371f0dee9465
Create Date: 2026-07-17 09:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c41e8a9d02f7"
down_revision = "371f0dee9465"
branch_labels = None
depends_on = None


def upgrade():
    for table in ("tle", "orbital_elements"):
        op.add_column(
            table,
            sa.Column(
                "is_canonical",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )
    # Pre-existing generated rows are single regular fits (one per ephemeris
    # file), i.e. exactly the archival sets this flag preserves.
    op.execute("UPDATE tle SET is_canonical = true WHERE data_source = 'generated'")
    op.execute(
        "UPDATE orbital_elements SET is_canonical = true "
        "WHERE data_source = 'generated'"
    )


def downgrade():
    for table in ("tle", "orbital_elements"):
        op.drop_column(table, "is_canonical")
