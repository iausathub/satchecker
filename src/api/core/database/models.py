from datetime import datetime

from core import db
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TEXT, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from zoneinfo import ZoneInfo

Base = declarative_base()


class Satellite(Base):
    __tablename__ = "satellites"
    __table_args__ = {"extend_existing": True}

    id = db.Column(INTEGER, primary_key=True)
    sat_number = db.Column(INTEGER, nullable=False)
    sat_name = db.Column(TEXT, nullable=False)
    constellation = db.Column(TEXT)
    rcs_size = db.Column(TEXT)
    launch_date = db.Column(TIMESTAMP(timezone=True))
    decay_date = db.Column(TIMESTAMP(timezone=True))
    object_id = db.Column(TEXT)
    object_type = db.Column(TEXT)
    has_current_sat_number = db.Column(BOOLEAN, nullable=False, default=False)
    date_added = db.Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(ZoneInfo("UTC"))
    )
    date_modified = db.Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(ZoneInfo("UTC"))
    )
    __table_args__ = (db.UniqueConstraint("sat_number", "sat_name"),)

    # def __init__(self, sat_number, sat_name, constellation):
    #     self.sat_number = sat_number
    #     self.sat_name = sat_name
    #     self.constellation = constellation

    def __repr__(self):
        return f"<Satellite {self.sat_name}>"


class TLE(Base):
    __tablename__ = "tle"
    __table_args__ = {"extend_existing": True}

    id = db.Column(INTEGER, primary_key=True)
    sat_id = db.Column(INTEGER, db.ForeignKey("satellites.id"), nullable=False)
    date_collected = db.Column(TIMESTAMP(timezone=True), nullable=False)
    tle_line1 = db.Column(TEXT, nullable=False)
    tle_line2 = db.Column(TEXT, nullable=False)
    epoch = db.Column(TIMESTAMP(timezone=True), nullable=False)
    is_supplemental = db.Column(BOOLEAN, nullable=False)
    data_source = db.Column(TEXT, nullable=False)
    tle_satellite = db.relationship("database.models.Satellite", lazy="joined")
    __table_args__ = (db.UniqueConstraint("sat_id", "epoch", "data_source"),)

    # def __init__(
    #     self,
    #     sat_id,
    #     date_collected,
    #     tle_line1,
    #     tle_line2,
    #     is_supplemental,
    #     epoch,
    #     data_source,
    # ):
    #     self.sat_id = sat_id
    #     self.date_collected = date_collected
    #     self.tle_line1 = tle_line1
    #     self.tle_line2 = tle_line2
    #     self.is_supplemental = is_supplemental
    #     self.data_source = data_source
    #     self.epoch = epoch

    def __repr__(self):
        return f"<TLE {self.tle_satellite}>"


# Define the index on the date_collected column
Index("idx_date_collected", TLE.date_collected)
