from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class userWebAccess(Base):
    __tablename__ = 'userWebAccess'
    idUserWeb = Column(String(50), ForeignKey('users.ID_User_Login'), primary_key=True, nullable=False)
    idAccessWeb = Column(Integer, ForeignKey('AccessWeb.idAccess'), primary_key=True, nullable=False)

    # Relationships
    user = relationship('users', back_populates='user_accesses', lazy='dynamic')
    access = relationship('accessWeb', back_populates='user_accesses', lazy='dynamic')

    def to_dict(self):
        return {
            "idUserWeb": self.idUserWeb,
            "idAccessWeb": self.idAccessWeb,
            "user": self.user.to_dict() if self.user else None,
            "access": self.access.to_dict() if self.access else None,
        }

