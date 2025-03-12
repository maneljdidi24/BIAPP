from sqlalchemy.orm import Session
from ..models.budget import Budget  # Assuming you have your Budget model defined in HR.models
#from ..models.budget2 import Budget2
from sqlalchemy.exc import SQLAlchemyError
import calendar
from typing import List, Dict
from flask import jsonify
import pandas as pd


class BudgetService:

    @staticmethod
    def insert_budget_from_json(db: Session, data: Dict, budget_name: str):
        try:
            print("*****************************************")
            print("Received data:")
            print(data)
            print("Budget name:", budget_name)

            # Extraction du plant et de l'année à partir du nom du budget
            parts = budget_name.split(" Budget ")
            if len(parts) != 2:
                raise ValueError("Invalid budget name format. Expected 'Plant Budget Year'")
            plant = parts[0].strip()
            year = int(parts[1].strip())
            print(f"Extracted Plant: {plant}, Extracted Year: {year}")

            # Convertir les données en DataFrame
            df = pd.DataFrame(data)
            print("Generated DataFrame:")
            print(df)

            budgets_to_add = []  # Liste pour les nouveaux budgets

            for index, row in df.iterrows():
                # Récupération dynamique des champs
                idcmp = int(row.get("code"))
                idcc = row.get("cost_center", "")
                if len(idcc) > 5:
                    idcc = idcc[-5:]  # Extraire les 5 derniers caractères si nécessaire

                if not idcmp or not idcc:
                    print(f"Ligne ignorée : ID ou Cost Center manquant - {row}")
                    continue

                # Boucle pour chaque mois
                for month in range(1, 13):
                    month_name = calendar.month_name[month]  # e.g., "January"
                    month_key = f"{month_name}_budget"       # Key for estimated budget
                    month_key2 = f"{month_name}_actual"      # Key for actual budget
                    #print(month_key)
                    #print(month_key2)
                    try:
                        # Handle missing or invalid values for "budget"
                        estimated_budget_lc = float(row.get(month_key, 0))  # Default to 0 if missing
                        # Force actual budget to 0 if missing or invalid
                        actual_budget_lc = float(row.get(month_key2, 0) or 0)  # Default to 0 if missing or invalid
                    
                    except ValueError:
                        print(f"Invalid value for {month_key} or {month_key2}: {row.get(month_key)} / {row.get(month_key2)}")
                        continue                    
                    
                    # Vérifier si un budget existe déjà
                    existing_budget = db.query(Budget).filter(
                        Budget.idcmp == idcmp,
                        Budget.idcc == idcc,
                        Budget.plant == plant,
                        Budget.yearB == year,
                        Budget.monthB == month
                    ).first()

                    if existing_budget:
                        # Mise à jour si le budget existe
                        print(f"Budget existant trouvé pour Plant: {plant}, Year: {year}, Month: {month} -> {existing_budget}")
                        existing_budget.estimatedBudget_lc = estimated_budget_lc
                        existing_budget.actualBudget_lc = actual_budget_lc
                    else:
                        # Création d'un nouveau budget
                        print(f"Création d'un nouveau budget pour Plant: {plant}, Year: {year}, Month: {month}")
                        new_budget = Budget(
                            idcmp=idcmp,
                            idcc=idcc,
                            plant=plant,
                            yearB=year,
                            monthB=month,
                            estimatedBudget_lc=estimated_budget_lc,
                            actualBudget_lc=actual_budget_lc
                        )
                        budgets_to_add.append(new_budget)

            # Ajout des nouveaux budgets et validation
            if budgets_to_add:
                db.add_all(budgets_to_add)
                db.commit()
                print("Budgets insérés avec succès.")
            else:
                db.commit()
                print("Aucun nouveau budget ajouté, uniquement des mises à jour.")

            return {"message": "Budgets insérés ou mis à jour avec succès."}

        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erreur SQLAlchemy : {e}")
            return {"error": "Erreur d'insertion dans la base de données : " + str(e)}, 500

        except Exception as e:
            print(f"Erreur générale : {e}")
            return {"error": str(e)}, 400

   
    
    @staticmethod
    def create_or_update_bulk_budget_file(db: Session, newbudget_data: dict, user_id: str):
        try:
            """ Prepare a list to hold all budget objects """
            newbudgets_to_create = []
            newbudgets_to_update = []

            # Iterate over each budget entry in the data dictionary
            for budget_name, data_list in newbudget_data.items():
                # Extract the plant name and year from the budget name
                plant_name = ' '.join(budget_name.split()[:-2])  # Extract "COF MD" from "COF MD Budget 2024"
                year = budget_name.split()[-1]  # Extract "2024" from "COF MD Budget 2024"
                
                for data in data_list:
                    """ Assuming the 'cost center' is unique to each entry """
                    idcc_last_5 = data['cost_center'][-5:]  # Extract the last 5 characters from cost center
                    print(idcc_last_5)
                    """ Loop through each month (January to December)"""
                    for month in range(1, 13):  # 1 to 12 for January to December
                        # Construct the month name (e.g., "January", "February")
                        month_name = f"{['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_num-1]}"
                        print("month")
                        print(month)   
                        
                        # Build the month-specific key like "January Budget", "February Budget", etc.
                        budget_key = f"{month_name}_Budget"
                        actual_key = f"{month_name}_Actual"
                        # Check if the current month exists in the data
                        if budget_key in data:
                            # Get the budget value for the current month
                            budget_value = data[budget_key]
                            actual_value = data[actual_key]

                            # Query the database to check if this budget already exists using the primary key (idcmp, idcc, plant, year)
                            existing_budget = db.query(Budget).filter_by(
                                idcmp=data['code'],  # Assuming 'code' is the idcmp
                                idcc=idcc_last_5,  # The last 5 digits of the cost center
                                plant=plant_name,  # The plant name
                                yearB=year , # The year
                                monthB=month
                            ).first()

                            if existing_budget:
                                """ If the budget already exists, update it """
                                # We will update the budget only if it is for the correct month
                                existing_budget.estimatedBudget = budget_value
                                existing_budget.actualBudget = actual_value
                                # existing_budget.user_id = user_id  # Optionally track the user who made the update
                                newbudgets_to_update.append(existing_budget)
                            else:
                                """ If the budget does not exist, create a new one """
                                new_budget = Budget(
                                    idcmp=data['code'],  # 'code' is used as idcmp
                                    idcc=idcc_last_5,  # Last 5 digits of cost center
                                    plant=plant_name,  # Plant name
                                    yearB=year,  # Year
                                    monthB=month,  # Month (January, February, etc.)
                                    estimatedBudget=budget_value,  # Estimated budget for that month
                                    actualBudget =actual_value
                                    # user_id=user_id  # Optionally track the user who created it
                                )
                                newbudgets_to_create.append(new_budget)

            """ Add all new budgets and commit """
            if newbudgets_to_create:
                db.add_all(newbudgets_to_create)

            """ Commit the transaction after processing all the entries """
        
            db.commit()

            """ Convert budgets to dictionary and return as response """ 
            updated_budgets = [budget.to_dict() for budget in newbudgets_to_update]
            created_budgets = [budget.to_dict() for budget in newbudgets_to_create]

            
            # Return the created and updated budgets
            return {"updated_budgets": updated_budgets, "created_budgets": created_budgets}


        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating or updating bulk budgets: {str(e)}")
    
    
    @staticmethod
    def update_budget(db: Session, idcmp: int, idcc: str, plant: str, year: int, month: int, estimatedBudget: str):
        """Update an existing budget entry."""
        try:
            budget = db.query(Budget).filter_by(idcmp=idcmp, idcc=idcc, plant=plant, yearB=year, monthB=month).first()
            if budget:
                budget.estimatedBudget = estimatedBudget
                budget.actualBudget = actualBudget
                db.commit()
                return budget.to_dict()  # Return the updated budget's dictionary representation
            return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating budget: {str(e)}")

    @staticmethod
    def delete_budget(db: Session, idcmp: int, idcc: str, plant: str, year: int, month: int):
        """Delete a specific budget entry."""
        print(db)
        print(idcmp)
        print(db)
        print(idcc)
        print(plant)
        print(monthB)

        try:
            budget = db.query(Budget).filter_by(idcmp=idcmp, idcc=idcc, plant=plant, yearB=year, monthB=month).first()
            if budget:
                db.delete(budget)
                db.commit()
                return True  # Return True if the budget was deleted
            return False
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting budget: {str(e)}")


