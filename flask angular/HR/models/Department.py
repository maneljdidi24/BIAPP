from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DATE,DATETIME
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = 'Department'

    ID_Department = Column(String(4), primary_key=True, nullable=False, default=None)
    Nom_Department = Column(String(50), primary_key=False, nullable=True, default=None)


    employees = relationship('Employer', back_populates='department', lazy='dynamic')

    def to_dict(self):
        return {
            "ID": self.ID_Department,
            "Nom_Department": self.Nom_Department,
        }
    
    # shop is the department and the product is the empl