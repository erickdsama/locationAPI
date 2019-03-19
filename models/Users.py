import datetime

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from utils.database import Base
from .Operator import *

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(20), unique=True)
    operator = Column(Integer, ForeignKey("operator.id"))

    def __init__(self, number=None, operator=None):
        self.number = number
        self.operator = operator

    def __repr__(self):
        return '<User %r>' % (self.number)

    def to_dict(self):
        return {
                "number": self.number,
                "operator": self.operator
            }
