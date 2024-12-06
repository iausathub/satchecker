from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Sequence,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SatelliteDb(Base):
    __tablename__ = "satellites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sat_number = Column(Integer, nullable=False)
    sat_name = Column(Text, nullable=False)
    constellation = Column(Text)
    rcs_size = Column(Text)
    launch_date = Column(DateTime(timezone=True))
    decay_date = Column(DateTime(timezone=True))
    object_id = Column(Text)
    object_type = Column(Text)
    has_current_sat_number = Column(Boolean, nullable=False, default=False)
    date_added = Column(DateTime(timezone=True), nullable=False, default=func.now())
    date_modified = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    __table_args__ = (UniqueConstraint("sat_number", "sat_name"),)


class TLEDb(Base):
    __tablename__ = "tle_partitioned"

    id = Column(
        Integer,
        Sequence("tle_partitioned_id_seq"),
        server_default=Sequence("tle_partitioned_id_seq", start=1).next_value(),
        primary_key=True,
    )
    sat_id = Column(Integer, ForeignKey("satellites.id"), nullable=False)
    date_collected = Column(DateTime(timezone=True), nullable=False)
    tle_line1 = Column(Text, nullable=False)
    tle_line2 = Column(Text, nullable=False)
    epoch = Column(DateTime(timezone=True), nullable=False, primary_key=True)
    is_supplemental = Column(Boolean, nullable=False)
    data_source = Column(Text, nullable=False)
    satellite = relationship("SatelliteDb", backref="tle_partitioned")
    __table_args__ = (
        UniqueConstraint("sat_id", "epoch", "data_source"),
        {"postgresql_partition_by": "RANGE (epoch)"},
    )


# Define the index on the date_collected column
Index("idx_date_collected", TLEDb.date_collected)
