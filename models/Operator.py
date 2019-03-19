import datetime

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from utils.database import Base


class Operator(Base):
    __tablename__ = 'operator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(20), unique=True)

    def __init__(self, number=None):
        self.number = number

    def __repr__(self):
        return '<Operator %r>' % (self.number)

