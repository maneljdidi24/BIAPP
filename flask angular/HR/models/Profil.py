from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profil(Base):
    __tablename__ = 'Profil'
    ID_Profil = Column(String(3), primary_key=True, nullable=False, default=None)
    Profil_Description = Column(String(None), primary_key=False, nullable=True, default=None)

