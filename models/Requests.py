import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from utils.database import Base


class Requests(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    device = Column(Integer, ForeignKey("devices.id"))
    user = Column(Integer, ForeignKey("users.id"))
    date_request = Column(DateTime, default=datetime.datetime.utcnow)


    def __init__(self, device=None, user=None):
        self.device = device
        self.user = user

    def __repr__(self):
        return '<Request %r>' % (self.id)