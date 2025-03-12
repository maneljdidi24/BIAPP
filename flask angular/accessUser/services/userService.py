from accessUser.models import users
from sqlalchemy.orm import Session
import pandas as pd

class UserService:
    @staticmethod
    def get_all_users(db: Session):
        """Fetch all users."""
        users = db.query(users).all()
        serialized_users = [user.to_dict() for user in users]
        return serialized_users

    
    @staticmethod
    def get_all_users_with_access(db: Session):
        # Query all users and eagerly load their associated access using the db session
        users = db.query(users).all()  # Use db.session.query(User)
        result = []
        
        for user in users:
            user_data = {
                "ID_User_Login": user.ID_User_Login,
                "access": [{"idAccess": access.idAccess, "accessDescription": access.accessDescription} for access in user.access]
            }
            result.append(user_data)
        return result


    @staticmethod
    def get_user_by_id(db: Session, ID_User_Login: int):
        """Fetch a user by ID."""
        return db.query(users).filter(users.ID_User_Login == ID_User_Login).first()

    @staticmethod
    def create_user(db: Session, user_data: dict):
        """Create a new user."""
        new_user = users(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(db: Session, ID_User_Login: int, updated_data: dict):
        """Update an existing user."""
        user = db.query(users).filter(users.ID_User_Login == ID_User_Login).first()
        if user:
            for key, value in updated_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, ID_User_Login: int):
        """Delete a user."""
        user = db.query(users).filter(users.ID_User_Login == ID_User_Login).first()
        if user:
            db.delete(user)
            db.commit()
        return user

    @staticmethod
    def get_user_access(db: Session, ID_User_Login: int):
        """Fetch access assigned to a user."""
        user = db.query(users).filter(users.ID_User_Login == ID_User_Login).first()
        if user:
            return user.access
        return None
