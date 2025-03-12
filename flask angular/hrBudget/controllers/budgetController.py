from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from dao.database import get_db, init_db
from ..services.budgetService import BudgetService
from sqlalchemy.exc import SQLAlchemyError


# Define the namespace for budget-related routes
budget_controller = Namespace('budgets', description='Budget management operations')

# Define the model for the Budget #old
budget_model = budget_controller.model('Budget', {
    'idcmp': fields.String(description='Company ID', required=True),
    'idcc': fields.String(description='Cost Center ID', required=True),
    'plant': fields.String(description='Plant Name', required=True),
    'year': fields.Integer(description='Year', required=True),
    'month': fields.Integer(description='Month', required=True),
    'estimatedBudget': fields.String(description='Budget estimatedBudget', required=True)
})



# Define the model for the Budget
newbudget_model = budget_controller.model('Budget', {
        'code': fields.String(description='Company ID', required=True),
        'cost_center': fields.String(description='Cost_center (e.g., "TN30000101")', required=True),
        'January_budget': fields.String(description='January Budget', required=False),
        'January_actual': fields.String(description='January Actual', required=False),
        'February_budget': fields.String(description='February Budget', required=False),
        'February_actual': fields.String(description='February Actual', required=False),
        'March_budget': fields.String(description='March Budget', required=False),
        'March_Actual': fields.String(description='March Actual', required=False),
        'April_budget': fields.String(description='April Budget', required=False),
        'April_actual': fields.String(description='April Actual', required=False),
        'May_budget': fields.String(description='May Budget', required=False),
        'May_actual': fields.String(description='May Actual', required=False),
        'June_budget': fields.String(description='June Budget', required=False),
        'June_actual': fields.String(description='June Actual', required=False),
        'July_budget': fields.String(description='July Budget', required=False),
        'July_actual': fields.String(description='July Actual', required=False),
        'August_budget': fields.String(description='August Budget', required=False),
        'August_actual': fields.String(description='August Actual', required=False),
        'September_budget': fields.String(description='September Budget', required=False),
        'September_actual': fields.String(description='September Actual', required=False),
        'October_budget': fields.String(description='October Budget', required=False),
        'October_actual': fields.String(description='October Actual', required=False),
        'November_budget': fields.String(description='November Budget', required=False),
        'November_actual': fields.String(description='November Actual', required=False),
        'December_budget': fields.String(description='December Budget', required=False),
        'December_actual': fields.String(description='December Actual', required=False),
})



# Define a response model for messages (e.g., success/failure messages)
message_model = budget_controller.model('Message', {
    'message': fields.String(description='Response message')
})

# Function to initialize the database
def set_database():
    init_db('HR')

# Routes for Budget

@cross_origin()
@jwt_required()
@budget_controller.route('/')
class BudgetList(Resource):
    @budget_controller.doc('get_budgets')
    @budget_controller.response(200, 'Success', [newbudget_model])
    def get(self):
        """Fetch all budgets with details."""
        print("Fetching all budgets.")
        set_database()
        with next(get_db()) as db:
            budgets = BudgetService.get_all_budgets(db)
            return jsonify(budgets)

            
    @budget_controller.route('/bulk_file/<string:budget_name>', endpoint='insert_budget_from_json')
    class Bulk_fileBudgetResource(Resource):
        @budget_controller.expect([newbudget_model], validate=True)  # Expecting a list of budget items
        @budget_controller.response(201, 'Budgets created or updated successfully')
        @budget_controller.response(200, 'Budgets created or updated successfully')
        def post(self,budget_name):
            """Create or update multiple budget entries."""
            budget_data = request.json  # This will be a list of dictionaries
            set_database()  # Assuming set_database prepares the DB connection
            with next(get_db()) as db:  # Assuming get_db provides the DB session
                try:
                    print(budget_data)
                    # Call the service method to handle the bulk operation
                    result = BudgetService.insert_budget_from_json(db, budget_data,budget_name)  # Replace with actual user_id
                    print(result)
                    return result

                except SQLAlchemyError as e:
                    return {'message': f"Error creating or updating budgets: {str(e)}"}, 400


@cross_origin()
@jwt_required()
@budget_controller.route('/<int:idcmp>/<string:idcc>/<string:plant>/<int:year>/<int:month>', endpoint='get_budget')

class BudgetResource(Resource):
    @budget_controller.doc('get_budget')
    @budget_controller.response(200, 'Success', newbudget_model)
    @budget_controller.response(404, 'Budget not found')
    def get(self, idcmp, idcc, plant, year, month):
        """Fetch a single budget entry by its composite primary key."""
        print(f"Fetching budget for {idcmp}, {idcc}, {plant}, {year}, {month}.")
        set_database()
        with next(get_db()) as db:
            budget = BudgetService.get_budget_by_id(db, idcmp, idcc, plant, year, month)
            if budget:
                return jsonify(budget), 200
            return {'message': 'Budget not found'}, 404

    @budget_controller.doc('delete_budget')
    @budget_controller.response(200, 'Success', message_model)  # Use message_model here
    @budget_controller.response(404, 'Budget not found', message_model)  # Use message_model here as well
    def delete(self, idcmp, idcc, plant, year, month):
        """Delete a budget entry."""
        set_database()
        with next(get_db()) as db:
            success = BudgetService.delete_budget(db, idcmp, idcc, plant, year, month)
            if success:
                return jsonify({'message': 'Budget deleted'}), 200
            return jsonify({'message': 'Budget not found'}), 404

    @budget_controller.expect(newbudget_model, validate=True)
    @budget_controller.doc('update_budget')
    @budget_controller.response(200, 'Success', newbudget_model)
    @budget_controller.response(404, 'Budget not found')
    def put(self, idcmp, idcc, plant, year, month):
        """Update a budget entry."""
        budget_data = request.json
        set_database()
        with next(get_db()) as db:
            updated_budget = BudgetService.update_budget(
                db,
                idcmp,
                idcc,
                plant,
                year,
                month,
                budget_data['estimatedBudget'],budget_data['actualBudget']
                
            )
            if updated_budget:
                return jsonify(updated_budget), 200
            return {'message': 'Budget not found'}, 404
