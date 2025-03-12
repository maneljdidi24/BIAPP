from sqlalchemy.orm import Session
from HR.models import Department,Employer
from HR.services.departmentService import DepartmentService
from HR.services.jobService import JobService
from HR.services.plantService import PlantService
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy import update
import pandas as pd
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, ProgrammingError, SQLAlchemyError, DatabaseError, StatementError
from sqlalchemy.orm import joinedload




class EmployerService:
    @staticmethod
    def get_all_employers(db: Session):
        """Fetch all employers."""
        employers =db.query(Employer).all()
        serialized_Employer = [dept.to_dict() for dept in employers]
        return serialized_Employer

    @staticmethod
    def filter_employers(db: Session, filters: dict):
        query = db.query(Employer)
        print(filters)
        # Apply filters dynamically
        for attr, value in filters.items():
            if isinstance(value, list):  # Handle list filtering (e.g., `IN` queries)
                query = query.filter(getattr(Employer, attr).in_(value))
            elif value is not None:  # Filter for non-None values
                query = query.filter(getattr(Employer, attr) == value)
        employers = query.all()
        serialized_employers = [employer.to_dict() for employer in employers]

        # Print serialized results for debugging
        print("Filtered Employers:", serialized_employers)

        return serialized_employers



    @staticmethod
    def get_employees_by_filter(db: Session, plant_list: list, start_date: datetime, end_date: datetime, department_id: str = None, job_id: str = None, costcenter_id: str = None):
        """Fetch employees based on a list of plants and hiring dates within a range, with additional filters for department, job, and cost center."""
        
        # Build the query filter dynamically
        query = db.query(Employer).filter(
            Employer.Plant.in_(plant_list),  # Filter by plant list
            Employer.Hiring_Date >= start_date,
            Employer.Hiring_Date <= end_date
        )

        # Optional filters
        if department_id:
            query = query.filter(Employer.ID_Department == department_id)

        if job_id:
            query = query.filter(Employer.ID_job == job_id)

        if costcenter_id:
            query = query.filter(Employer.CostCenter_ID == costcenter_id)

        # Execute the query with joined relationships (eager loading)
        employees = query.options(joinedload(Employer.plant), joinedload(Employer.department), joinedload(Employer.job), joinedload(Employer.costCenter)).all()

        # Serialize employee data
        serialized_Employees = [emp.to_dict() for emp in employees]
        return serialized_Employees



    @staticmethod
    def get_all_employers_with_details(db: Session):
        """Fetch all employers with their related departments, jobs, and plants."""
        employers = db.query(Employer).all()
        result = []

        for employer in employers:
            employer_data = {
                "Id_Empl": employer.Id_Empl,
                "name_E": employer.name_E
            }
            result.append(employer_data)

        return result

    @staticmethod
    def get_employer_by_id(db: Session, Id_Empl: str, Plant: str):
        """ Fetch an employer by their ID and plant."""
        return db.query(Employer).filter(Employer.Id_Empl == Id_Empl, Employer.Plant == Plant).first()



    @staticmethod
    def create_employer(db: Session, employer_data: dict, user_id: int):
        """ Create a new employer. """
        if not isinstance(employer_data, dict):
            raise ValueError("employer_data must be a dictionary")

        # Add additional fields to the dictionary
        employer_data["created_by"] = user_id
        employer_data["dateCreation"] = datetime.now()
        print("Employer Data (Before Validation):", employer_data)

        # Filter the dictionary to include only fields defined in the Employer model
        valid_fields = {col.name for col in Employer.__table__.columns}
        employer_data = {key: value for key, value in employer_data.items() if key in valid_fields}
        print("Employer Data (After Validation):", employer_data)

        try:
            # Create the new employer record
            new_employer = Employer(**employer_data)
            db.add(new_employer)
            db.commit()
            db.refresh(new_employer)
            return "Employer added successfully"
        
        # Specific SQLAlchemy exceptions
        except IntegrityError as ie:
            db.rollback()
            raise ValueError(f"Integrity error (e.g., duplicate key, constraint violation): {ie.orig}")
        except DataError as de:
            db.rollback()
            raise ValueError(f"Data error (e.g., invalid data type, out of range): {de.orig}")
        except OperationalError as oe:
            db.rollback()
            raise ValueError(f"Operational error (e.g., database unavailable, connection issue): {oe.orig}")
        except ProgrammingError as pe:
            db.rollback()
            raise ValueError(f"Programming error (e.g., SQL syntax error, invalid query): {pe.orig}")
        except StatementError as se:
            db.rollback()
            raise ValueError(f"Statement error (e.g., invalid parameter binding): {se.orig}")
        except DatabaseError as db_error:
            db.rollback()
            raise ValueError(f"Database error (general database error): {db_error.orig}")
        except SQLAlchemyError as sae:
            db.rollback()
            raise ValueError(f"SQLAlchemy error (other database issues): {sae.orig}")

        # General Python exceptions
        except TypeError as te:
            db.rollback()
            raise ValueError(f"Type error (e.g., incorrect data type): {te}")
        except ValueError as ve:
            db.rollback()
            raise ValueError(f"Value error (e.g., invalid value): {ve}")
        except KeyError as ke:
            db.rollback()
            raise ValueError(f"Key error (e.g., missing required field): {ke}")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Unexpected error: {e}")

    
    

    @staticmethod
    def create_or_update_bulk_employers(db: Session, employers_data: list, user_id: str):
        """
        Create new records, delete existing ones that need modification, and re-insert them.
        """
        try:
            print("Starting bulk employer processing...")
            employers_df = create_dataframe(employers_data)
            total = len(employers_df)
            print(f"Total employers received: {total}")
            
            existing_employers_df = fetch_existing_employers(db)
            print(f"Existing employers fetched: {len(existing_employers_df)}")
            
            to_insert, to_delete = identify_records(employers_df, existing_employers_df)
            print(f"Records to insert: {len(to_insert)}, Records to delete: {len(to_delete)}")
            
            inserted, errors = process_inserts(db, to_insert, user_id)
            deleted, delete_errors = process_deletions(db, to_delete)
            errors.extend(delete_errors)
            
            reinserted, reinsertion_errors = process_reinsertions(db, to_delete, existing_employers_df, user_id)
            inserted.extend(reinserted)
            errors.extend(reinsertion_errors)
            
            print("Successfully inserted records:", len(inserted))
            print("Successfully deleted records:", len(deleted))
            return summary(total, inserted, deleted, errors)
            
        except Exception as e:
            db.rollback()
            print("Bulk processing failed:", str(e))
            return error_summary(e, inserted, deleted, errors)




        
    @staticmethod
    def update_employer(db: Session, Id_Empl: str, Plant: str, updated_data: dict):
        """Update an existing employer."""
        employer = db.query(Employer).filter(Employer.Id_Empl == Id_Empl, Employer.Plant == Plant).first()
        if employer:
            for key, value in updated_data.items():
                setattr(employer, key, value)
            db.commit()
            db.refresh(employer)
        return employer

    @staticmethod
    def delete_employer(db: Session, Id_Empl: str, Plant: str):
        """Delete an employer."""
        employer = db.query(Employer).filter(Employer.Id_Empl == Id_Empl, Employer.Plant == Plant).first()
        if employer:
            db.delete(employer)
            db.commit()
        return employer
    

def create_dataframe(employers_data: list) -> pd.DataFrame:
    return pd.DataFrame(employers_data)


def fetch_existing_employers(db: Session) -> pd.DataFrame:
    return pd.read_sql(
        db.query(Employer.Id_Empl, Employer.dateCreation, Employer.created_by).statement,
        db.bind
    )


def identify_records(employers_df: pd.DataFrame, existing_employers_df: pd.DataFrame) -> tuple:
    employers_df["exists"] = employers_df["Id_Empl"].isin(existing_employers_df["Id_Empl"])
    to_insert = employers_df[~employers_df["exists"]].copy()
    to_delete = employers_df[employers_df["exists"]].copy()
    return to_insert, to_delete


def process_inserts(db: Session, to_insert: pd.DataFrame, user_id: str) -> tuple:
    inserted = []
    errors = []
    if not to_insert.empty:
        print("Processing inserts...")
        to_insert["created_by"] = user_id
        to_insert["dateCreation"] = datetime.now()
        to_insert.drop(columns=["exists"], inplace=True)
        try:
            to_insert.to_sql(
                name=Employer.__tablename__,
                con=db.bind,
                if_exists="append",
                index=False,
                method="multi"
            )
            inserted.extend(to_insert["Id_Empl"].tolist())
        except SQLAlchemyError as db_error:
            db.rollback()
            errors.append({'error': str(db_error)})
    return inserted, errors


def process_deletions(db: Session, to_delete: pd.DataFrame) -> tuple:
    deleted = []
    errors = []
    if not to_delete.empty:
        print("Processing deletions...")
        try:
            employer_ids_to_delete = to_delete["Id_Empl"].tolist()
            db.query(Employer).filter(Employer.Id_Empl.in_(employer_ids_to_delete)).delete(synchronize_session='fetch')
            db.commit()
            deleted.extend(employer_ids_to_delete)
        except SQLAlchemyError as db_error:
            db.rollback()
            errors.append({'error': str(db_error)})
    return deleted, errors


def process_reinsertions(db: Session, to_delete: pd.DataFrame, existing_employers_df: pd.DataFrame, user_id: str) -> tuple:
    reinserted = []
    errors = []
    if not to_delete.empty:
        print("Re-inserting modified records...")
        to_delete = to_delete.merge(existing_employers_df[['Id_Empl', 'dateCreation', 'created_by']], on="Id_Empl", how="left")
        to_delete["original_created_by"] = to_delete["created_by"]
        to_delete["original_dateCreation"] = to_delete["dateCreation"]
        to_delete["modified_by"] = user_id
        to_delete["dateModif"] = datetime.now()
        to_delete["created_by"] = to_delete["original_created_by"]
        to_delete["dateCreation"] = to_delete["original_dateCreation"]
        to_delete.drop(columns=["exists", "original_created_by", "original_dateCreation"], inplace=True)
        try:
            to_delete.to_sql(
                name=Employer.__tablename__,
                con=db.bind,
                if_exists="append",
                index=False,
                method="multi"
            )
            reinserted.extend(to_delete["Id_Empl"].tolist())
        except SQLAlchemyError as db_error:
            db.rollback()
            errors.append({'error': str(db_error)})
    return reinserted, errors


def summary(total, inserted, deleted, errors) -> dict:
    return {
        'total_processed': total,
        'inserted': len(inserted),
        'deleted': len(deleted),
        'errors': len(errors)
    }


def error_summary(exception: Exception, inserted: list, deleted: list, errors: list) -> dict:
    return {
        'message': 'An error occurred during processing.',
        'error': str(exception),
        'inserted': len(inserted),
        'deleted': len(deleted),
        'errors': len(errors)
    }    
