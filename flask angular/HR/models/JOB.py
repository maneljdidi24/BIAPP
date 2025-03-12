from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DATE,DATETIME
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = 'JOB'
    Id_job = Column(String(7), primary_key=True, nullable=False, default=None)
    job_description = Column(String(None), primary_key=False, nullable=True, default=None)


    employees = relationship('Employer', back_populates='job', lazy='dynamic')

    def to_dict(self):
        return {
            "ID": self.Id_job,
            "job_description": self.job_description,
        }
    