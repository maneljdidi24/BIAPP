from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User_hr(Base):
    __tablename__ = 'User_HR'
    user_name = Column(String(50), primary_key=True, nullable=False, default=None)
    password = Column(String(10), primary_key=False, nullable=True, default=None)
    access = Column(String(3), primary_key=False, nullable=True, default=None)
    access_id = Column(Integer, ForeignKey('Profil.ID_Profil'))
    profil = relationship('Profil', back_populates='user_hr')

