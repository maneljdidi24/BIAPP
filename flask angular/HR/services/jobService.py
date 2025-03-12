from sqlalchemy.orm import Session
from ..models.JOB import Job

class JobService:
    @staticmethod
    def get_all_jobs(db: Session):
        """Fetch all jobs."""
        job =db.query(Job).all()
        serialized_Job = [dept.to_dict() for dept in job]
        return serialized_Job

    @staticmethod
    def get_job_by_id(db: Session, Id_job: str):
        """Fetch a job by its ID."""
        return db.query(Job).filter(Job.Id_job == Id_job).first()

    @staticmethod
    def create_job(db: Session, job_data: dict):
        """Create a new job."""
        new_job = Job(**job_data)
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job

    @staticmethod
    def update_job(db: Session, Id_job: str, updated_data: dict):
        """Update an existing job."""
        job = db.query(Job).filter(Job.Id_job == Id_job).first()
        if job:
            for key, value in updated_data.items():
                setattr(job, key, value)
            db.commit()
            db.refresh(job)
        return job

    @staticmethod
    def delete_job(db: Session, Id_job: str):
        """Delete a job."""
        job = db.query(Job).filter(Job.Id_job == Id_job).first()
        if job:
            db.delete(job)
            db.commit()
        return job
