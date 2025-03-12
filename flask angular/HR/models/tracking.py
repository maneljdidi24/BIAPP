from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tracking(Base):
    __tablename__ = 'tracking'
    Matricule = Column(String(20), primary_key=True, nullable=False, default=None)
    plant = Column(String(20), primary_key=True, nullable=False, default=None)
    date = Column(DATE, primary_key=True, nullable=False, default=None)
    REG = Column(String(10), primary_key=False, nullable=True, default=None)
    HB = Column(REAL, primary_key=False, nullable=True, default=None)
    H25 = Column(REAL, primary_key=False, nullable=True, default=None)
    H50 = Column(REAL, primary_key=False, nullable=True, default=None)
    H100 = Column(REAL, primary_key=False, nullable=True, default=None)
    PA = Column(REAL, primary_key=False, nullable=True, default=None)
    hnuit = Column(REAL, primary_key=False, nullable=True, default=None)
    ABS_ = Column(REAL, primary_key=False, nullable=True, default=None)
    ASS_ = Column(REAL, primary_key=False, nullable=True, default=None)
    SAL = Column(REAL, primary_key=False, nullable=True, default=None)
    H75 = Column(REAL, primary_key=False, nullable=True, default=None)
    
    Matricule_id = Column(Integer, ForeignKey('Employer.Id_Empl'))
    employer = relationship('Employer', back_populates='tracking')

