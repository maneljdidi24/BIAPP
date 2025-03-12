from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DATE,DATETIME
from sqlalchemy.orm import relationship

class Budget(Base):
    __tablename__ = 'Budget'
    
    # Define the columns
    idcmp = Column(Integer, primary_key=True, nullable=False, default=None)
    idcc = Column(String(5), primary_key=True, nullable=False, default=None)
    plant = Column(String(20), primary_key=True, nullable=False, default=None)
    yearB = Column(Integer, primary_key=True, nullable=False, default=None)
    monthB = Column(Integer, primary_key=True, nullable=False, default=None)
    estimatedBudget_lc = Column(String, nullable=True, default=None)
    actualBudget_lc = Column(String, nullable=True, default=None)
    def to_dict(self):
        return {
            "idcmp": self.idcmp,
            "idcc": self.idcc,
            "plant": self.plant,
            "yearB": self.year,
            "monthB": self.month,
            "estimatedBudget_lc": self.estimatedBudget,
            "actualBudget_lc": self.actualBudget
        }

