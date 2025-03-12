from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class accessWeb(Base):
    __tablename__ = 'accessWeb'
    idAccess = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(50), nullable=True)


    user_accesses = relationship('userWebAccess', back_populates='accessWeb', lazy='dynamic')

    def to_dict(self):
        return {
            "idAccess": self.idAccess,
            "Name": self.Name,
        }
