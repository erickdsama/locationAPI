import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey

from utils.database import Base


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_code = Column(String(64), unique=True)
    short_name = Column(String(20), unique=False)
    user = Column(Integer, ForeignKey("user.id"))
    date_registered = Column(Date, default=datetime.datetime.utcnow)

    def __init__(self, id_code=None, short_name=None, user=None):
        self.id_code = id_code
        self.short_name = short_name
        self.user = user

    def __repr__(self):
        return '<Device %r>' % (self.id_code)

    def to_dict(self):
        return {
                "device": self.id_code,
                "short_name": self.short_name
            }
