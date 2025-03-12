from .base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class users(Base):
    __tablename__ = 'users'
    ID_User_Login = Column(String(50), primary_key=True, nullable=False, default=None)
    Password = Column(String(200), primary_key=False, nullable=True, default=None)
    Position = Column(String(100), primary_key=False, nullable=True, default=None)
    Type = Column(String(50), primary_key=False, nullable=True, default=None)


    user_accesses = relationship('userWebAccess', back_populates='users', lazy='dynamic')

    def to_dict(self):
        return {
            "ID_User_Login": self.ID_User_Login,
            "Password": self.Password,
            "Position": self.Position,
            "Type": self.Type,
        }