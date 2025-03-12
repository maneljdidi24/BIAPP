from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'Role'
    id_role = Column(String(3), primary_key=True, nullable=False, default=None)
    role = Column(String(50), primary_key=False, nullable=True, default=None)
    role_description = Column(String(None), primary_key=False, nullable=True, default=None)
    role_scope = Column(String(20), primary_key=False, nullable=True, default=None)
    role_restrictions = Column(String(3), primary_key=False, nullable=True, default=None)

