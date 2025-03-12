from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .userBIAccess import Userbiaccess

Base = declarative_base()

class Access(Base):
    __tablename__ = 'access'
    idAccess = Column(Integer, primary_key=True, nullable=False, default=None)
    accessDescription = Column(String(100), primary_key=False, nullable=True, default=None)

    # Relationship with UserBiAccess (many-to-many)
    user_bi_accesses = relationship('UserBiAccess', backref='access', lazy=True)
    users = relationship('users', secondary='user_bi_access', back_populates='accesses')