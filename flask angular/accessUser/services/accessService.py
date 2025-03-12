""" from sqlalchemy.orm import Session
from models import Access

class AccessService:
    @staticmethod
    def get_all_access(db: Session):
        return db.query(Access).all()

    @staticmethod
    def get_access_by_id(db: Session, access_id: int):
        return db.query(Access).filter(Access.idAccess == access_id).first()

    @staticmethod
    def create_access(db: Session, access_data: dict):
        new_access = Access(
            access_desc=access_data.get('access_desc')
        )
        db.add(new_access)
        db.commit()
        db.refresh(new_access)
        return new_access

    @staticmethod
    def update_access(db: Session, access_id: int, updated_data: dict):
        access = db.query(Access).filter(Access.idAccess == access_id).first()
        if access:
            access.access_desc = updated_data.get('access_desc', access.access_desc)
            db.commit()
            db.refresh(access)
        return access

    @staticmethod
    def delete_access(db: Session, access_id: int):
        access = db.query(Access).filter(Access.idAccess == access_id).first()
        if access:
            db.delete(access)
            db.commit()
        return access
 """