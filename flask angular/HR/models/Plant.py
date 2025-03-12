from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DATE,DATETIME
from sqlalchemy.orm import relationship

class Plant(Base):
    __tablename__ = 'Plant'
    Plant = Column(String(20), primary_key=True, nullable=False, default=None)
    Region = Column(String(50), primary_key=False, nullable=True, default=None)
    Inv_Company = Column(String(50), primary_key=False, nullable=True, default=None)
    Sales_Company = Column(String(50), primary_key=False, nullable=True, default=None)
    plant_Description = Column(String(50), primary_key=False, nullable=True, default=None)


    
    employees = relationship('Employer', back_populates='plant', lazy='dynamic')

    def to_dict(self):
        return {
            "Plant": self.Plant,
            "Region": self.Region,
            "plant_Description": self.plant_Description
        }
    