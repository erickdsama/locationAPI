import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from utils.database import Base, CRUD


class Request(Base, CRUD):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(Integer, ForeignKey("device.id"))
    user = Column(Integer, ForeignKey("user.id"))
    status = Column(String(1), default='R')
    message = Column(Text)
    response = Column(Text)
    request_type = Column(String(1))
    date_request = Column(DateTime, default=datetime.datetime.utcnow)
    date_received = Column(DateTime, default=datetime.datetime.utcnow)
    date_sent = Column(DateTime, default=datetime.datetime.utcnow)



    def __init__(self, device=None, user=None, status=None, message=None, response=None,
                 request_type=None, date_request=None, date_received=None, date_sent=None):
        self.device = device
        self.user = user
        self.status = status
        self.response = response
        self.message = message
        self.request_type = request_type
        self.date_request = date_request
        self.date_received = date_received
        self.date_sent = date_sent

    def __repr__(self):
        return '<Request %r>' % (self.id)