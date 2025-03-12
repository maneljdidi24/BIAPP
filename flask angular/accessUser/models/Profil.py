from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profil(Base):
    __tablename__ = 'Profil'
    idprofil = Column(Integer, primary_key=True, nullable=False, default=None)
    name = Column(String(50), primary_key=False, nullable=True, default=None)
    description = Column(String(100), primary_key=False, nullable=True, default=None)
    typeProfil = Column(String(10), primary_key=False, nullable=True, default=None)

