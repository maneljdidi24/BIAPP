from sqlalchemy.orm import Session
from ..models.costCenter import costCenter  # Adjust import to match your structure

class CostCenterService:
    @staticmethod
    def get_all_cost_centers(db: Session):
        """Fetch all cost centers."""
        cost_centers = db.query(costCenter).all()
        serialized_cost_centers = [cc.to_dict() for cc in cost_centers]
        return serialized_cost_centers

    @staticmethod
    def get_cost_center_by_id(db: Session, idcc: str):
        """Fetch a cost center by its ID."""
        return db.query(costCenter).filter(costCenter.idcc == idcc).first()

    @staticmethod
    def create_cost_center(db: Session, cost_center_data: dict):
        """Create a new cost center."""
        new_cost_center = costCenter(**cost_center_data)
        db.add(new_cost_center)
        db.commit()
        db.refresh(new_cost_center)
        return new_cost_center

    @staticmethod
    def update_cost_center(db: Session, idcc: str, updated_data: dict):
        """Update an existing cost center."""
        cost_center = db.query(costCenter).filter(costCenter.idcc == idcc).first()
        if cost_center:
            for key, value in updated_data.items():
                setattr(cost_center, key, value)
            db.commit()
            db.refresh(cost_center)
        return cost_center

    @staticmethod
    def delete_cost_center(db: Session, idcc: str):
        """Delete a cost center."""
        cost_center = db.query(costCenter).filter(costCenter.idcc == idcc).first()
        if cost_center:
            db.delete(cost_center)
            db.commit()
        return cost_center
