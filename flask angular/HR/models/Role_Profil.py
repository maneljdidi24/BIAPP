from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role_profil(Base):
    __tablename__ = 'Role_Profil'
    id_profil = Column(String(3), primary_key=True, nullable=False, default=None)
    id_role = Column(String(3), primary_key=True, nullable=False, default=None)
    id_role_id = Column(Integer, ForeignKey('Role.id_role'))
    role = relationship('Role', back_populates='role_profil')
    id_profil_id = Column(Integer, ForeignKey('Profil.ID_Profil'))
    profil = relationship('Profil', back_populates='role_profil')

