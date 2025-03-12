from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'
    idProject = Column(String(3), primary_key=True, nullable=False, default=None)
    Description = Column(String(50), primary_key=False, nullable=True, default=None)

