from sqlalchemy.orm import Session
from accessUser.models.roles import Role

class RoleService:
    @staticmethod
    def get_all_roles(db: Session):
        """Fetch all roles."""
        return db.query(Role).all()

    @staticmethod
    def get_role_by_id(db: Session, id_role: str):
        """Fetch a role by its ID."""
        return db.query(Role).filter(Role.id_role == id_role).first()

    @staticmethod
    def create_role(db: Session, role_data: dict):
        """Create a new role."""
        new_role = Role(**role_data)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role

    @staticmethod
    def update_role(db: Session, id_role: str, updated_data: dict):
        """Update an existing role."""
        role = db.query(Role).filter(Role.id_role == id_role).first()
        if role:
            for key, value in updated_data.items():
                setattr(role, key, value)
            db.commit()
            db.refresh(role)
        return role

    @staticmethod
    def delete_role(db: Session, id_role: str):
        """Delete a role."""
        role = db.query(Role).filter(Role.id_role == id_role).first()
        if role:
            db.delete(role)
            db.commit()
        return role
