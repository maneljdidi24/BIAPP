from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Training(Base):
    __tablename__ = 'Training'
    id_training = Column(Integer, primary_key=True, nullable=False, default=None)
    training_description = Column(String(None), primary_key=False, nullable=True, default=None)
    creation_date = Column(DATETIME, primary_key=False, nullable=False, default=None)
    start_date = Column(DATE, primary_key=False, nullable=True, default=None)
    end_date = Column(DATE, primary_key=False, nullable=True, default=None)
    topic = Column(String(50), primary_key=False, nullable=True, default=None)
    Provider = Column(String(50), primary_key=False, nullable=True, default=None)
    Trainer = Column(String(50), primary_key=False, nullable=True, default=None)
    training_hrs = Column(REAL, primary_key=False, nullable=True, default=None)
    cost = Column(REAL, primary_key=False, nullable=True, default=None)
    invited = Column(Integer, primary_key=False, nullable=True, default=None)
    participants = Column(Integer, primary_key=False, nullable=True, default=None)
    state = Column(String(50), primary_key=False, nullable=True, default=None)
    budget = Column(Integer, primary_key=False, nullable=True, default=None)
    mode = Column(String(50), primary_key=False, nullable=True, default=None)
    plant = Column(String(10), primary_key=False, nullable=True, default=None)
    budget_id = Column(Integer, ForeignKey('Budget.ID_Budget'))
    budget = relationship('Budget', back_populates='training')

