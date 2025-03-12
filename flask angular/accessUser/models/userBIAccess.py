from sqlalchemy import Column, Integer, String, ForeignKey,DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Userbiaccess(Base):
    __tablename__ = 'userBIAccess'
    idUser = Column(Integer, ForeignKey('users.ID_User_Login'), primary_key=True)
    idAccess = Column(Integer, ForeignKey('access.idAccess'), primary_key=True) 
    createdBy = Column(String(50), primary_key=False, nullable=True, default=None)
    modifiedBy = Column(String(50), primary_key=False, nullable=True, default=None)
    createdAt = Column(DATETIME, primary_key=False, nullable=True, default=None)
    modifiedAt = Column(DATETIME, primary_key=False, nullable=True, default=None)
    created_at = Column(DATETIME, primary_key=False, nullable=False, default=None)
    modified_at = Column(DATETIME, primary_key=False, nullable=True, default=None)



