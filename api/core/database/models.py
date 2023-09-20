from core import db

class Satellite(db.Model):
    __tablename__ = 'satellites'

    id = db.Column(db.Integer, primary_key=True)
    sat_number = db.Column(db.String())
    sat_name = db.Column(db.String())
    constellation = db.Column(db.String())

    def __init__(self, sat_number, sat_name, constellation):
        self.sat_number = sat_number
        self.sat_name = sat_name
        self.constellation = constellation

    def __repr__(self):
        return f"<Satellite {self.sat_name}>"

class TLE(db.Model):
    __tablename__ = 'tle'

    id = db.Column(db.Integer, primary_key=True)
    sat_id = db.Column(db.Integer(), db.ForeignKey('satellites.id'))
    date_collected = db.Column(db.DateTime())
    tle_line1 = db.Column(db.String())
    tle_line2 = db.Column(db.String())
    is_supplemental = db.Column(db.Boolean())
    epoch = db.Column(db.DateTime())
    tle_satellite = db.relationship("database.models.Satellite",lazy='joined')


    def __init__(self, sat_id, date_collected, tle_line1, tle_line2, is_supplemental, epoch):
        self.sat_id = sat_id
        self.date_collected = date_collected
        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2
        self.is_supplemental = is_supplemental
        self.epoch = epoch

    def __repr__(self):
        return f"<TLE {self.tle_satellite}>"
