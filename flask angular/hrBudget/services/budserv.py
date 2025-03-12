# from sqlalchemy.orm import Session
# from ..models.budget import Budget  # Assuming you have your Budget model defined in HR.models
# from sqlalchemy.exc import SQLAlchemyError

# from typing import List, Dict
# from flask import jsonify 

# class BudgetService:
#     """comment it"""
#     @staticmethod
#     def get_all_budgets(db: Session):
#         """Fetch all budget entries."""
#         budgets = db.query(Budget).all()
#         serialized_budgets = [budget.to_dict() for budget in budgets]  # Serializing each budget entry to dictionary
#         return serialized_budgets

#     @staticmethod
#     def get_budget_by_id(db: Session, idcmp: int, idcc: str, plant: str, year: int, month: int):
#         """Fetch a specific budget entry by its composite primary key."""
#         budget = db.query(Budget).filter_by(idcmp=idcmp, idcc=idcc, plant=plant, year=year, month=month).first()
#         if budget:
#             return budget.to_dict()  # Return the dictionary representation of the found budget
#         return None

#     """comment it"""

    
#     @staticmethod
#     def get_all_budgets_with_details(db: Session):
#         """Fetch all budgets with additional details (e.g., related Budget information)."""
#         budgets = db.query(Budget).all()
#         result = []

#         for budget in budgets:
#             # Assuming you want to include the `Budget` details (adjust according to your data model)
#             # Example: join budget with Budget or any other related entity you may need.
#             budget_data = {
#                 "idcmp": budget.idcmp,
#                 "idcc": budget.idcc,
#                 "plant": budget.plant,
#                 "year": budget.year,
#                 "month": budget.month,
#                 "estimatedBudget": budget.estimatedBudget
#             }
#             # You could join or fetch additional related data here if needed (e.g., related Budget or department)
#             result.append(budget_data)

#         return result
        
#     """comment"""
#     @staticmethod
#     def create_budget(db: Session, idcmp: int, idcc: str, plant: str, year: int, month: int, estimatedBudget: str):
#         """Create a new budget entry."""
#         try:
#             budget = Budget(idcmp=idcmp, idcc=idcc, plant=plant, year=year, month=month, estimatedBudget=estimatedBudget)
#             db.add(budget)
#             db.commit()
#             return budget.to_dict()  # Return the created budget's dictionary representation
#         except SQLAlchemyError as e:
#             db.rollback()
#             raise Exception(f"Error creating budget: {str(e)}")
    
#     """comment"""


#     @staticmethod
#     def create_or_update_bulk_budget(db: Session, budget_data: list, user_id: str):
#         try:
#             """ Prepare a list to hold all budget objects """
#             budgets_to_create = []
#             budgets_to_update = []

#             for data in budget_data:
#                 """ Assuming you want to extract the last 5 characters of 'idcmp' """
#                 idcc_last_5 = data['idcc'][-5:]  # Extraction des 5 derniers caractères

#                 """ Assuming 'idcmp', 'idcc', 'plant', 'year', 'month' are unique to each budget """
#                 existing_budget = db.query(Budget).filter_by(
#                     idcmp=data['idcmp'],
#                     idcc=idcc_last_5,
#                     plant=data['plant'],
#                     year=data['year'],
#                     month=data['month']
#                 ).first()

#                 if existing_budget:
#                     """ If the budget already exists, update it """
#                     existing_budget.estimatedBudget = data['estimatedBudget']
#                     #existing_budget.user_id = user_id  # If needed, track user who made the update
#                     budgets_to_update.append(existing_budget)
#                 else:
#                     """ If the budget does not exist, create a new one """
#                     new_budget = Budget(
#                         idcmp=data['idcmp'],
#                         idcc=idcc_last_5,
#                         plant=data['plant'],
#                         year=data['year'],
#                         month=data['month'],
#                         estimatedBudget=data['estimatedBudget'],
#                         #user_id=user_id  # Assuming you want to track the user who created it
#                     )
#                     budgets_to_create.append(new_budget)

#             """ Add all new budgets and commit """
#             if budgets_to_create:
#                 db.add_all(budgets_to_create)

#             """Commit the transaction after processing all the entries """
#             db.commit()

#             """ Convert budgets to dictionary and return as response""" 
#             updated_budgets = [budget.to_dict() for budget in budgets_to_update]
#             created_budgets = [budget.to_dict() for budget in budgets_to_create]
#             print({"updated_budgets": updated_budgets, "created_budgets": created_budgets})
#             return ("budgets_to_update")

#         except SQLAlchemyError as e:
#             db.rollback()
#             raise Exception(f"Error creating or updating bulk budgets: {str(e)}")








#     @staticmethod
#     def create_or_update_bulk_budget_file(db: Session, budget_data: dict, user_id: str):
#         try:
#             """ Prepare a list to hold all budget objects """
#             budgets_to_create = []
#             budgets_to_update = []

#             # Iterate over each budget entry in the data dictionary
#             for budget_name, data_list in budget_data.items():
#                 # Extract the plant name and year from the budget name
#                 plant_name = ' '.join(budget_name.split()[:-2])  # Extract "COF MD" from "COF MD Budget 2024"
#                 year = budget_name.split()[-1]  # Extract "2024" from "COF MD Budget 2024"

#                 for data in data_list:
#                     """ Assuming the 'cost center' is unique to each entry """
#                     idcc_last_5 = data['cost center'][-5:]  # Extract the last 5 characters from cost center

#                     """ Loop through each month (January to December)"""
#                     for month_num in range(1, 13):  # 1 to 12 for January to December
#                         # Construct the month name (e.g., "January", "February")
#                         month_name = f"{['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_num-1]}"

#                         # Build the month-specific key like "January Budget", "February Budget", etc.
#                         budget_key = f"{month_name} Budget"

#                         # Check if the current month exists in the data
#                         if budget_key in data:
#                             # Get the budget value for the current month
#                             budget_value = data[budget_key]

#                             # Query the database to check if this budget already exists using the primary key (idcmp, idcc, plant, year)
#                             existing_budget = db.query(Budget).filter_by(
#                                 idcmp=data['code'],  # Assuming 'code' is the idcmp
#                                 idcc=idcc_last_5,  # The last 5 digits of the cost center
#                                 plant=plant_name,  # The plant name
#                                 year=year  # The year
#                             ).first()

#                             if existing_budget:
#                                 """ If the budget already exists, update it """
#                                 # We will update the budget only if it is for the correct month
#                                 existing_budget.estimatedBudget = budget_value
#                                 # existing_budget.user_id = user_id  # Optionally track the user who made the update
#                                 budgets_to_update.append(existing_budget)
#                             else:
#                                 """ If the budget does not exist, create a new one """
#                                 new_budget = Budget(
#                                     idcmp=data['code'],  # 'code' is used as idcmp
#                                     idcc=idcc_last_5,  # Last 5 digits of cost center
#                                     plant=plant_name,  # Plant name
#                                     year=year,  # Year
#                                     month=month_name,  # Month (January, February, etc.)
#                                     estimatedBudget=budget_value,  # Estimated budget for that month
#                                     # user_id=user_id  # Optionally track the user who created it
#                                 )
#                                 budgets_to_create.append(new_budget)

#             """ Add all new budgets and commit """
#             if budgets_to_create:
#                 db.add_all(budgets_to_create)

#             """ Commit the transaction after processing all the entries """
#             db.commit()

#             """ Convert budgets to dictionary and return as response """ 
#             updated_budgets = [budget.to_dict() for budget in budgets_to_update]
#             created_budgets = [budget.to_dict() for budget in budgets_to_create]

#             print({"updated_budgets": updated_budgets, "created_budgets": created_budgets})

#             # Return the created and updated budgets
#             return {"updated_budgets": updated_budgets, "created_budgets": created_budgets}

#         except SQLAlchemyError as e:
#             db.rollback()
#             raise Exception(f"Error creating or updating bulk budgets: {str(e)}")





#     @staticmethod
#     def update_budget(db: Session, idcmp: int, idcc: str, plant: str, year: int, month: int, estimatedBudget: str):
#         """Update an existing budget entry."""
#         try:
#             budget = db.query(Budget).filter_by(idcmp=idcmp, idcc=idcc, plant=plant, year=year, month=month).first()
#             if budget:
#                 budget.estimatedBudget = estimatedBudget
#                 db.commit()
#                 return budget.to_dict()  # Return the updated budget's dictionary representation
#             return None
#         except SQLAlchemyError as e:
#             db.rollback()
#             raise Exception(f"Error updating budget: {str(e)}")

#     @staticmethod
#     def delete_budget(db: Session, idcmp: int, idcc: str, plant: str, year: int, month: int):
#         """Delete a specific budget entry."""
#         try:
#             budget = db.query(Budget).filter_by(idcmp=idcmp, idcc=idcc, plant=plant, year=year, month=month).first()
#             if budget:
#                 db.delete(budget)
#                 db.commit()
#                 return True  # Return True if the budget was deleted
#             return False
#         except SQLAlchemyError as e:
#             db.rollback()
#             raise Exception(f"Error deleting budget: {str(e)}")
