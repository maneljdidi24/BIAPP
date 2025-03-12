from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DATE,DATETIME
from sqlalchemy.orm import relationship


class costCenter(Base):
    __tablename__ = 'costCenter'  # Table name is 'costCenter'
    
    idcc = Column(String(7), primary_key=True, nullable=False, default=None)
    ccDescription = Column(String(None), nullable=True, default=None)

    # Define relationships if any
    # For example, if there are any relationships with other tables like "employees" or "job":
    employees = relationship('Employer', back_populates='costCenter', lazy='dynamic')

    def to_dict(self):
        return {
            "idcc": self.idcc,
            "ccDescription": self.ccDescription,
        }