import datetime

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from utils.database import Base


class Locations(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    lat = Column(String(20), unique=False)
    lng = Column(String(20), unique=False)
    device = Column(Integer, ForeignKey("devices.id"))
    date_registered = Column(Date, default=datetime.datetime.utcnow)


    def __init__(self, lat=None, lng=None, device=None):
        self.lat = lat
        self.lng = lng
        self.device = device

    def __repr__(self):
        return '<Location %r>' % (self.id)