
from op_gg import db

from _datetime import datetime


class Searchdb(db.Model):
    ipaddress = db.Column(db.String(50), primary_key=True, nullable=False)
    region = db.Column(db.String(5), nullable=False)
    summonername = db.Column(db.String(50), nullable=False)
    date_searched = db.Column(db.DateTime,primary_key=True, default=datetime.utcnow)


    def __repr__(self):
        return f"Searchdb('{self.ipaddress}','{self.region}','{self.summonername}','{self.date_searched}')"
