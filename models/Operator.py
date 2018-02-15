import datetime

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from utils.database import Base


class Operators(Base):
    __tablename__ = 'operators'

    id = Column(Integer, primary_key=True)
    number = Column(String(20), unique=True)

    def __init__(self, number=None):
        self.number = number

    def __repr__(self):
        return '<Operator %r>' % (self.number)

