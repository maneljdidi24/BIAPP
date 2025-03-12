from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Budget(Base):
    __tablename__ = 'Budget'
    ID_Budget = Column(Integer, primary_key=True, nullable=False, default=None)
    YEAR = Column(NUMERIC(4, 0), primary_key=False, nullable=False, default=None)
    plant = Column(String(20), primary_key=False, nullable=False, default=None)
    SCOPE = Column(String(20), primary_key=False, nullable=False, default=None)
    AMMOUNT = Column(NUMERIC(18, 4), primary_key=False, nullable=True, default=None)
    STATE = Column(BIT, primary_key=False, nullable=True, default=None)

