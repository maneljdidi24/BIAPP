
from sqlalchemy.orm import Session
from ..models.Plant import Plant

class PlantService:
    @staticmethod
    def get_all_plants(db: Session):
        """Fetch all plants."""
        return db.query(Plant).all()

    @staticmethod
    def get_plant_by_id(db: Session, Plant: str):
        """Fetch a plant by its ID."""
        return db.query(Plant).filter(Plant.Plant == Plant).first()

    @staticmethod
    def create_plant(db: Session, plant_data: dict):
        """Create a new plant."""
        new_plant = Plant(**plant_data)
        db.add(new_plant)
        db.commit()
        db.refresh(new_plant)
        return new_plant

    @staticmethod
    def update_plant(db: Session, Plant: str, updated_data: dict):
        """Update an existing plant."""
        plant = db.query(Plant).filter(Plant.Plant == Plant).first()
        if plant:
            for key, value in updated_data.items():
                setattr(plant, key, value)
            db.commit()
            db.refresh(plant)
        return plant

    @staticmethod
    def delete_plant(db: Session, Plant: str):
        """Delete a plant."""
        plant = db.query(Plant).filter(Plant.Plant == Plant).first()
        if plant:
            db.delete(plant)
            db.commit()
        return plant
