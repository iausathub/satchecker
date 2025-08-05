from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class SatelliteDesignationDb(Base):
    __tablename__ = "satellite_designation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sat_id = Column(Integer, ForeignKey("satellites.id"), nullable=False)
    sat_name = Column(Text, nullable=False)
    sat_number = Column(Integer, nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))
    date_added = Column(DateTime(timezone=True), nullable=False, default=func.now())
    date_modified = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    satellite = relationship("SatelliteDb", back_populates="designations")

    __table_args__ = (
        UniqueConstraint("sat_number", "sat_name", "sat_id"),
        Index("idx_sat_des_sat_number_sat_name", sat_number, sat_name),
        Index("idx_sat_des_valid_from", valid_from),
        Index("idx_sat_des_valid_to", valid_to),
        Index("idx_sat_des_temporal_range", valid_from, valid_to),
        Index("idx_sat_des_sat_id_temporal", sat_id, valid_from, valid_to),
    )


class SatelliteDb(Base):
    __tablename__ = "satellites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    constellation = Column(Text)
    generation = Column(Text)
    rcs_size = Column(Text)
    launch_date = Column(DateTime(timezone=True))
    decay_date = Column(DateTime(timezone=True))
    object_id = Column(Text)
    object_type = Column(Text)
    date_added = Column(DateTime(timezone=True), nullable=False, default=func.now())
    date_modified = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    designations = relationship("SatelliteDesignationDb", back_populates="satellite")

    __table_args__ = (
        UniqueConstraint("object_id", "launch_date"),
        Index(
            "idx_satellites_active",
            decay_date,
            postgresql_where="(decay_date IS NOT NULL)",
        ),
        Index("idx_satellites_decay_date", decay_date),
        Index("idx_satellites_launch_date", launch_date),
        Index("idx_satellites_active_range", launch_date, decay_date),
        Index(
            "idx_satellites_active_covering",
            launch_date,
            decay_date,
            postgresql_include=["id", "constellation", "object_id", "object_type"],
        ),
    )


class TLEDb(Base):
    __tablename__ = "tle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sat_id = Column(Integer, ForeignKey("satellites.id"), nullable=False)
    date_collected = Column(DateTime(timezone=True), nullable=False)
    tle_line1 = Column(Text, nullable=False)
    tle_line2 = Column(Text, nullable=False)
    epoch = Column(DateTime(timezone=True), nullable=False)
    is_supplemental = Column(Boolean, nullable=False)
    data_source = Column(Text, nullable=False)
    satellite = relationship("SatelliteDb", backref="tle")
    __table_args__ = (
        UniqueConstraint("sat_id", "epoch", "data_source"),
        Index("idx_tle_epoch", epoch.desc()),
        Index("idx_tle_epoch_sat_id", sat_id.asc(), epoch.desc()),
        Index("idx_date_collected", date_collected),
        Index("idx_tle_sat_epoch", sat_id.asc(), epoch.asc(), data_source.asc()),
        Index(
            "idx_tle_sat_epoch_covering",
            sat_id.asc(),
            epoch.desc(),
            postgresql_include=[
                "id",
                "tle_line1",
                "tle_line2",
                "date_collected",
                "is_supplemental",
                "data_source",
            ],
        ),
    )


class EphemerisPointDb(Base):
    __tablename__ = "ephemeris_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ephemeris_id = Column(
        Integer, ForeignKey("interpolable_ephemeris.id"), nullable=False
    )
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    position: Column[Any] = Column(PG_ARRAY(Float, dimensions=3), nullable=False)
    velocity: Column[Any] = Column(PG_ARRAY(Float, dimensions=3), nullable=False)
    covariance: Column[Any] = Column(PG_ARRAY(Float), nullable=False)

    __table_args__ = (
        UniqueConstraint("ephemeris_id", "timestamp"),
        Index("idx_ephemeris_points_timestamp", "timestamp"),
        Index("idx_ephemeris_points_ephemeris_id", "ephemeris_id"),
    )


class InterpolableEphemerisDb(Base):
    __tablename__ = "interpolable_ephemeris"

    id = Column(Integer, primary_key=True, autoincrement=True)
    satellite = Column(Integer, ForeignKey("satellites.id"), nullable=False)
    date_collected = Column(DateTime(timezone=True), nullable=False, default=func.now())
    generated_at = Column(DateTime(timezone=True), nullable=False)
    data_source = Column(Text, nullable=False)
    file_reference = Column(Text)
    ephemeris_start = Column(DateTime(timezone=True), nullable=False)
    ephemeris_stop = Column(DateTime(timezone=True), nullable=False)
    frame = Column(Text, nullable=False)  # UVW, EME2000, etc.

    # Relationship to points, ordered by timestamp
    points = relationship(
        "EphemerisPointDb",
        backref="ephemeris",
        order_by="EphemerisPointDb.timestamp",
        cascade="all, delete-orphan",
    )

    satellite_ref = relationship("SatelliteDb", backref="interpolable_ephemeris")

    __table_args__ = (
        UniqueConstraint("satellite", "generated_at", "data_source"),
        Index("idx_ephemeris_satellite", "satellite"),
    )


class InterpolatedSplineDb(Base):
    __tablename__ = "interpolated_splines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    satellite = Column(Integer, ForeignKey("satellites.id"), nullable=False)
    ephemeris = Column(Integer, ForeignKey("interpolable_ephemeris.id"), nullable=False)
    time_range_start = Column(DateTime(timezone=True), nullable=False)
    time_range_end = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    position_splines: Column[Any] = Column(
        PG_ARRAY(Float, dimensions=3), nullable=False
    )
    velocity_splines: Column[Any] = Column(
        PG_ARRAY(Float, dimensions=3), nullable=False
    )

    chunk_size = Column(Integer, nullable=False)
    overlap = Column(Integer, nullable=False)

    satellite_ref = relationship("SatelliteDb", backref="interpolated_splines")
    ephemeris_ref = relationship(
        "InterpolableEphemerisDb", backref="interpolated_splines"
    )

    __table_args__ = (
        UniqueConstraint("satellite", "time_range_start", "time_range_end"),
        Index(
            "idx_interpolated_splines_time_range", "time_range_start", "time_range_end"
        ),
    )

    def __repr__(self):
        return (
            f"<InterpolatedSplineDb(id={self.id}, satellite={self.satellite}, "
            f"time_range=[{self.time_range_start}, {self.time_range_end}])>"
        )
