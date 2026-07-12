"""add orbital elements table

Revision ID: 371f0dee9465
Revises: 345fd9dd1e6d
Create Date: 2026-07-09 19:24:07.489338

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "371f0dee9465"
down_revision = "345fd9dd1e6d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "orbital_elements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sat_id", sa.Integer(), nullable=False),
        sa.Column("date_collected", sa.DateTime(timezone=True), nullable=False),
        sa.Column("epoch", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_source", sa.Text(), nullable=False),
        sa.Column("mean_motion", sa.Float(), nullable=False),
        sa.Column("eccentricity", sa.Float(), nullable=False),
        sa.Column("inclination", sa.Float(), nullable=False),
        sa.Column("ra_of_ascending_node", sa.Float(), nullable=False),
        sa.Column("arg_of_pericenter", sa.Float(), nullable=False),
        sa.Column("mean_anomaly", sa.Float(), nullable=False),
        sa.Column("ephemeris_type", sa.Integer(), nullable=False),
        sa.Column("classification_type", sa.String(length=1), nullable=False),
        sa.Column("element_set_no", sa.Integer(), nullable=False),
        sa.Column("rev_at_epoch", sa.Integer(), nullable=False),
        sa.Column("bstar", sa.Float(), nullable=False),
        sa.Column("mean_motion_dot", sa.Float(), nullable=False),
        sa.Column("mean_motion_ddot", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["sat_id"], ["satellites.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sat_id", "epoch", "data_source"),
    )
    op.create_index(
        "idx_orbital_elements_date_collected",
        "orbital_elements",
        ["date_collected"],
        unique=False,
    )
    op.create_index(
        "idx_orbital_elements_epoch",
        "orbital_elements",
        [sa.text("epoch DESC")],
        unique=False,
    )
    op.create_index(
        "idx_orbital_elements_epoch_sat_id",
        "orbital_elements",
        [sa.text("sat_id ASC"), sa.text("epoch DESC")],
        unique=False,
    )
    op.create_index(
        "idx_orbital_elements_sat_epoch",
        "orbital_elements",
        [sa.text("sat_id ASC"), sa.text("epoch ASC"), sa.text("data_source ASC")],
        unique=False,
    )


def downgrade():
    op.drop_index("idx_orbital_elements_sat_epoch", table_name="orbital_elements")
    op.drop_index("idx_orbital_elements_epoch_sat_id", table_name="orbital_elements")
    op.drop_index("idx_orbital_elements_epoch", table_name="orbital_elements")
    op.drop_index("idx_orbital_elements_date_collected", table_name="orbital_elements")
    op.drop_table("orbital_elements")
