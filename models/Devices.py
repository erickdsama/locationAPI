import datetime

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from utils.database import Base


class Devices(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    id_code = Column(String(20), unique=True)
    short_name = Column(String(20), unique=False)
    user = Column(Integer, ForeignKey("users.id"))
    date_registered = Column(Date, default=datetime.datetime.utcnow)

    def __init__(self, id_code=None, short_name=None, user=None):
        self.id_code = id_code
        self.short_name = short_name
        self.user = user

    def __repr__(self):
        return '<Device %r>' % (self.id_code)