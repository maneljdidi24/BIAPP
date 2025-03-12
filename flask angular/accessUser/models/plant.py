from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plant(Base):
    __tablename__ = 'plant'
    Plant = Column(String(20), primary_key=True, nullable=False, default=None)
    Region = Column(String(50), primary_key=False, nullable=True, default=None)
    InvCompany = Column(String(50), primary_key=False, nullable=True, default=None)
    SalesCompany = Column(String(50), primary_key=False, nullable=True, default=None)
    plantDescription = Column(String(50), primary_key=False, nullable=True, default=None)

