from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Training_historic(Base):
    __tablename__ = 'training_historic'
    id_training = Column(Integer, primary_key=True, nullable=False, default=None)
    id_employer = Column(String(20), primary_key=True, nullable=False, default=None)
    plant = Column(String(20), primary_key=True, nullable=False, default=None)
    id_employer_id = Column(Integer, ForeignKey('Employer.Id_Empl'))
    employer = relationship('Employer', back_populates='training_historic')
    id_training_id = Column(Integer, ForeignKey('Training.id_training'))
    training = relationship('Training', back_populates='training_historic')

