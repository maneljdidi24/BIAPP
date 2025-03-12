from sqlalchemy.orm import Session
from HR.models import Department

class DepartmentService:
    @staticmethod
    def get_all_departments(db: Session):
        """Fetch all departments."""
        departments = db.query(Department).all()
        serialized_departments = [dept.to_dict() for dept in departments]
        print(serialized_departments)  # For debugging
        return serialized_departments


    @staticmethod
    def get_department_by_id(db: Session, ID_Department: str):
        """Fetch a department by its ID."""
        return db.query(Department).filter(Department.ID_Department == ID_Department).first()

    @staticmethod
    def create_department(db: Session, department_data: dict):
        """Create a new department."""
        new_department = Department(**department_data)
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
        return new_department

    @staticmethod
    def update_department(db: Session, ID_Department: str, updated_data: dict):
        """Update an existing department."""
        department = db.query(Department).filter(Department.ID_Department == ID_Department).first()
        if department:
            for key, value in updated_data.items():
                setattr(department, key, value)
            db.commit()
            db.refresh(department)
        return department

    @staticmethod
    def delete_department(db: Session, ID_Department: str):
        """Delete a department."""
        department = db.query(Department).filter(Department.ID_Department == ID_Department).first()
        if department:
            db.delete(department)
            db.commit()
        return department
