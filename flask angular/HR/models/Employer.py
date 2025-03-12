from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DATE,DATETIME
from sqlalchemy.orm import relationship



class Employer(Base):
    __tablename__ = 'Employer'
    Id_Empl = Column(String(20), primary_key=True, nullable=False, default=None)
   
    name_E = Column(String(50), primary_key=False, nullable=True, default=None)
    Gender = Column(String(10), primary_key=False, nullable=True, default=None)
    Birth_Date = Column(DATE, primary_key=False, nullable=True, default=None)
    Age = Column(Integer, primary_key=False, nullable=True, default=None)
    Generation = Column(String(50), primary_key=False, nullable=True, default=None)
    Local_Position = Column(String(None), primary_key=False, nullable=True, default=None)
    HC_Type = Column(String(20), primary_key=False, nullable=True, default=None)
    Valuation_Level = Column(String(10), primary_key=False, nullable=True, default=None)

    Scope = Column(String(20), primary_key=False, nullable=True, default=None)
    Cost_Center = Column(String(20), primary_key=False, nullable=True, default=None)

    Hiring_Date = Column(DATE, primary_key=False, nullable=True, default=None)

    Termination_Date = Column(DATE, primary_key=False, nullable=True, default=None)
    Termination_Reason = Column(String(50), primary_key=False, nullable=True, default=None)

    validated = Column(Integer, primary_key=False, nullable=True, default=None)
    dateValidation = Column(DATETIME, primary_key=False, nullable=True, default=None)

    created_by = Column(String(20), primary_key=False, nullable=True, default='')
    modified_by = Column(String(20), primary_key=False, nullable=True, default='')
    dateCreation = Column(DATETIME, primary_key=False, nullable=True, default=None)
    dateModif = Column(DATETIME, primary_key=False, nullable=True, default=None)

    Plant = Column(String(20),ForeignKey('Plant.Plant'), nullable=False, default=None)

    plant = relationship('Plant', back_populates='employees' , lazy='joined')

    ID_Department = Column(String(4),ForeignKey('Department.ID_Department'),nullable=True)

    department = relationship('Department', back_populates='employees' , lazy='joined')


    ID_job = Column(String(7), ForeignKey('JOB.Id_job'), nullable=True, default=None)

    job = relationship('Job', back_populates='employees' , lazy='joined')

    CostCenter_ID = Column(String(50), ForeignKey('costCenter.idcc'), nullable=True, default=None)

    costCenter = relationship('costCenter', back_populates='employees' , lazy='joined')



    def to_dict(self):
        return {
            "Id_Empl": self.Id_Empl,
            "plant": self.plant.to_dict() if self.plant else None,
            "name_E": self.name_E,
            "Gender": self.Gender,
            "Birth_Date": self.Birth_Date,
            "Age": self.Age,
            "Generation": self.Generation,
            "Local_Position": self.Local_Position,
            "HC_Type": self.HC_Type,
            "Valuation_Level": self.Valuation_Level,
            "Scope": self.Scope,
            "Cost_Center": self.Cost_Center,
            "Hiring_Date": self.Hiring_Date,
            "Termination_Date": self.Termination_Date,
            "Termination_Reason": self.Termination_Reason,
            "validated": self.validated,
            "dateValidation": self.dateValidation,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "dateCreation": self.dateCreation,
            "dateModif": self.dateModif,
            "CostCenter_ID":self.CostCenter_ID,
            "costCenter": self.costCenter.to_dict() if self.costCenter else None,
            "Job": self.job.to_dict() if self.job else None,  # Assuming the Department class also has a to_dict method
            "Department": self.department.to_dict() if self.department else None,  # Assuming the Department class also has a to_dict method
        }
