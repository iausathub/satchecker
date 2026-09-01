"""add object_id index to satellites

Ingestion demotes temporary-id rows in favor of the real catalog id for the
same object, keyed on ``object_id`` (see src/data/tle_utils.py). That lookup
runs on every ingested record, so ``satellites.object_id`` needs an index.
Built CONCURRENTLY to avoid locking the live table during ingestion.

Revision ID: e4b9f1c72a30
Revises: b7e3c1ad4f2a
Create Date: 2026-09-01 12:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e4b9f1c72a30"
down_revision = "b7e3c1ad4f2a"
branch_labels = None
depends_on = None


def upgrade():
    # CONCURRENTLY cannot run inside a transaction block.
    with op.get_context().autocommit_block():
        op.execute(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_satellites_object_id "
            "ON satellites (object_id)"
        )


def downgrade():
    with op.get_context().autocommit_block():
        op.execute("DROP INDEX CONCURRENTLY IF EXISTS idx_satellites_object_id")
