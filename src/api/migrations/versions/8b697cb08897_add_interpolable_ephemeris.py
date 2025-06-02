"""Add interpolable ephemeris

Revision ID: 8b697cb08897
Revises: a23d969e948e
Create Date: 2025-05-30 12:14:12.231526

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "8b697cb08897"
down_revision = "a23d969e948e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "interpolable_ephemeris",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("satellite", sa.Integer(), nullable=False),
        sa.Column("date_collected", sa.DateTime(timezone=True), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_source", sa.Text(), nullable=False),
        sa.Column("file_reference", sa.Text(), nullable=True),
        sa.Column("ephemeris_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ephemeris_stop", sa.DateTime(timezone=True), nullable=False),
        sa.Column("frame", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["satellite"],
            ["satellites.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("satellite", "generated_at", "data_source"),
    )
    op.create_index(
        "idx_ephemeris_satellite", "interpolable_ephemeris", ["satellite"], unique=False
    )
    op.create_table(
        "ephemeris_points",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ephemeris_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "position", postgresql.ARRAY(sa.Float(), dimensions=3), nullable=False
        ),
        sa.Column(
            "velocity", postgresql.ARRAY(sa.Float(), dimensions=3), nullable=False
        ),
        sa.Column(
            "covariance", postgresql.ARRAY(sa.Float(), dimensions=3), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["ephemeris_id"],
            ["interpolable_ephemeris.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ephemeris_id", "timestamp"),
    )
    op.create_index(
        "idx_ephemeris_points_ephemeris_id",
        "ephemeris_points",
        ["ephemeris_id"],
        unique=False,
    )
    op.create_index(
        "idx_ephemeris_points_timestamp",
        "ephemeris_points",
        ["timestamp"],
        unique=False,
    )
    op.create_table(
        "interpolated_splines",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("satellite", sa.Integer(), nullable=False),
        sa.Column("ephemeris", sa.Integer(), nullable=False),
        sa.Column("time_range_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("time_range_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "position_splines",
            postgresql.ARRAY(sa.Float(), dimensions=3),
            nullable=False,
        ),
        sa.Column(
            "velocity_splines",
            postgresql.ARRAY(sa.Float(), dimensions=3),
            nullable=False,
        ),
        sa.Column("chunk_size", sa.Integer(), nullable=False),
        sa.Column("overlap", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ephemeris"],
            ["interpolable_ephemeris.id"],
        ),
        sa.ForeignKeyConstraint(
            ["satellite"],
            ["satellites.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("satellite", "time_range_start", "time_range_end"),
    )
    op.create_index(
        "idx_interpolated_splines_time_range",
        "interpolated_splines",
        ["time_range_start", "time_range_end"],
        unique=False,
    )  # noqa: E501

    op.drop_index("idx_satellites_decay_date", table_name="satellites")
    op.create_index(
        "idx_satellites_decay_date", "satellites", ["decay_date"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():

    op.drop_index("idx_satellites_decay_date", table_name="satellites")
    op.create_index(
        "idx_satellites_decay_date",
        "satellites",
        [sa.text("decay_date NULLS FIRST")],
        unique=False,
    )  # noqa: E501

    op.drop_index(
        "idx_interpolated_splines_time_range", table_name="interpolated_splines"
    )
    op.drop_table("interpolated_splines")
    op.drop_index("idx_ephemeris_points_timestamp", table_name="ephemeris_points")
    op.drop_index("idx_ephemeris_points_ephemeris_id", table_name="ephemeris_points")
    op.drop_table("ephemeris_points")
    op.drop_index("idx_ephemeris_satellite", table_name="interpolable_ephemeris")
    op.drop_table("interpolable_ephemeris")
    # ### end Alembic commands ###
