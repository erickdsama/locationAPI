import datetime

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from utils.database import Base
from .Operator import *

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    number = Column(String(20), unique=True)
    operator = Column(Integer, ForeignKey("operators.id"))

    def __init__(self, number=None, operator=None):
        self.number = number
        self.operator = operator

    def __repr__(self):
        return '<User %r>' % (self.number)