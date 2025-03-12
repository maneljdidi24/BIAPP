from datetime import datetime
from HR.models import Department
from flask_restx import Namespace, Resource, fields,marshal_with
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from dao.database import get_db, init_db
from sqlalchemy.exc import SQLAlchemyError
from ..services.employerService import EmployerService


# Define the namespace for employer-related routes
employer_controller = Namespace('employers', description='Employer management operations')

# Define sub-models for department, job, and plant
department_model = employer_controller.model('Department', {
    'ID_Department': fields.String(description='Department ID'),
    'Nom_Department': fields.String(description='Department name')
})

cost_center_model = employer_controller.model('CostCenter', {
    'idcc': fields.String(required=True, description='The unique identifier of the cost center'),
    'ccDescription': fields.String(required=False, description='The description of the cost center'),
})

job_model = employer_controller.model('Job', {
    'job_id': fields.String(description='Job ID'),
    'job_name': fields.String(description='Job title')
})

plant_model = employer_controller.model('Plant', {
    'plant_id': fields.String(description='Plant ID'),
    'plant_name': fields.String(description='Plant name')
})

# Define the Employer model for Swagger documentation
employer_model = employer_controller.model('Employer', {
    'Id_Empl': fields.String(required=True, description='Employer ID (max length 20)', example="153"),
    'name_E': fields.String(description='Employer name (max length 50)', example="aaName"),
    'Gender': fields.String(description='Gender (max length 10)', example="Male"),
    'Birth_Date': fields.Date(
        description='Birth Date in YYYY-MM-DD format (optional)',
        example="1990-01-01"
    ),
    'Age': fields.Integer(description='Age (optional)', example="22"),
    'Generation': fields.String(description='Generation (max length 50)', example="Generation Y"),
    'ID_job': fields.String(description='Job ID (max length 20)', example="LOCSC04"),
    'Local_Position': fields.String(description='Local Position (max length 255)', example="Manager"),
    'HC_Type': fields.String(description='Headcount Type (max length 20)', example="Full-time"),
    'Valuation_Level': fields.String(description='Valuation Level (max length 10)'),
    'Scope': fields.String(description='Scope (max length 20)', example="Plant / ADC"),
    'Cost_Center': fields.String(description='Cost Center (max length 20)'),
    'Hiring_Date': fields.Date(
        description='Hiring Date in YYYY-MM-DD format (optional)',
        example="2023-12-12"
    ),
    'Termination_Date': fields.Date(
        description='Termination Date in YYYY-MM-DD format (optional)',
        example="2023-12-12"
    ),
    'costCenter': fields.Nested(cost_center_model, description='Associated CostCenter'),
    'Termination_Reason': fields.String(description='Reason for Termination (max length 50)'),
    'validated': fields.Integer(description='Validation Status (0 or 1)', example=1),
    'dateValidation': fields.DateTime(
        description='Date of Validation in YYYY-MM-DD HH:MM:SS format (optional)',
        example="2023-12-12 10:30:00"
    ),
    'CostCenter_ID' : fields.String(description='Cost Center (max length 20)'),
    'created_by': fields.String(description='Created By (max length 20)', example="admin"),
    'modified_by': fields.String(description='Modified By (max length 20)', example="admin"),
    'dateCreation': fields.DateTime(
        description='Creation Date in YYYY-MM-DD HH:MM:SS format (optional)',
        example="2023-12-12 09:00:00"
    ),
    'dateModif': fields.DateTime(
        description='Modification Date in YYYY-MM-DD HH:MM:SS format (optional)',
        example="2023-12-12 11:00:00"
    ),
    'Plant': fields.String(required=True, description='Plant name (max length 50)', example="COF TN"),
    'department': fields.Nested(department_model, description='Associated Department'),
    'job': fields.Nested(job_model, description='Associated Job'),
    'plant': fields.Nested(plant_model, description='Associated Plant')
})

employer_model_filter = employer_controller.model('Employer', {
    'Id_Empl': fields.String(description='Employer ID (max length 20)', example="153"),
    'name_E': fields.String(description='Employer name (max length 50)', example="aaName"),
    'Gender': fields.String(description='Gender (max length 10)', example="Male"),
    'Birth_Date': fields.Date(
        description='Birth Date in YYYY-MM-DD format (optional)',
        example="1990-01-01"
    ),
    'Age': fields.Integer(description='Age (optional)', example="22"),
    'Generation': fields.String(description='Generation (max length 50)', example="Generation Y"),
    'ID_job': fields.String(description='Job ID (max length 20)', example="LOCSC04"),
    'Local_Position': fields.String(description='Local Position (max length 255)', example="Manager"),
    'HC_Type': fields.String(description='Headcount Type (max length 20)', example="Full-time"),
    'Valuation_Level': fields.String(description='Valuation Level (max length 10)'),
    'Scope': fields.String(description='Scope (max length 20)', example="Plant / ADC"),
    'Cost_Center': fields.String(description='Cost Center (max length 20)'),
    'Hiring_Date': fields.Date(
        description='Hiring Date in YYYY-MM-DD format (optional)',
        example="2023-12-12"
    ),
    'Termination_Date': fields.Date(
        description='Termination Date in YYYY-MM-DD format (optional)',
        example="2023-12-12"
    ),
    'costCenter': fields.Nested(cost_center_model, description='Associated CostCenter'),
    'Termination_Reason': fields.String(description='Reason for Termination (max length 50)'),
    'validated': fields.Integer(description='Validation Status (0 or 1)', example=1),
    'dateValidation': fields.DateTime(
        description='Date of Validation in YYYY-MM-DD HH:MM:SS format (optional)',
        example="2023-12-12 10:30:00"
    ),
    'CostCenter_ID' : fields.String(description='Cost Center (max length 20)'),
    'created_by': fields.String(description='Created By (max length 20)', example="admin"),
    'modified_by': fields.String(description='Modified By (max length 20)', example="admin"),
    'dateCreation': fields.DateTime(
        description='Creation Date in YYYY-MM-DD HH:MM:SS format (optional)',
        example="2023-12-12 09:00:00"
    ),
    'dateModif': fields.DateTime(
        description='Modification Date in YYYY-MM-DD HH:MM:SS format (optional)',
        example="2023-12-12 11:00:00"
    ),
    'Plant': fields.String(description='Plant name (max length 50)', example="COF TN")
})


# Define your model for filtering
employee_filter_model = employer_controller.model('EmployeeFilter', {
    'plants': fields.List(fields.String, required=True, description="List of plant names", example=["COF MA", "COF TN"]),
    'start_date': fields.String(required=False, description="Start date in MM/DD/YYYY format", example="01/01/2023"),
    'end_date': fields.String(required=False, description="End date in MM/DD/YYYY format", example="12/31/2023"),
    'department': fields.String(required=False, description="Department filter", example="Engineering"),
    'job': fields.String(required=False, description="Job filter", example="Manager"),
    'costCenter': fields.String(required=False, description="Cost center filter", example="CC12345")
})


# Function to initialize database
def set_database():
    init_db('hr2')




@jwt_required()
@employer_controller.route('/')
class EmployerList(Resource):
    @employer_controller.doc('get_employers')
    @employer_controller.response(200, 'Success', [employer_model])
    def get(self):
        """Fetch all employers with details."""
        print("Fetch all employers with details.")
        set_database()
        with next(get_db()) as db:
            employers_with_details = EmployerService.get_all_employers(db)
            return jsonify(employers_with_details)


    



    @employer_controller.route('/single/<string:user_email>', endpoint='create_single_employer')
    class SingleEmployerResource(Resource):
        @employer_controller.expect(employer_model, validate=True)
        @employer_controller.response(201, 'Employer created successfully', employer_model)
        def post(self, user_email):
            """Create a single employer."""
            employer_data = request.json
            set_database()
            with next(get_db()) as db:
                new_employer = EmployerService.create_employer(db, employer_data, user_email)
                return jsonify(new_employer), 201


    @employer_controller.route('/bulk/<string:user_email>', endpoint='create_bulk_employers')
    class BulkEmployerResource(Resource):
        @employer_controller.expect([employer_model], validate=True)
        @employer_controller.response(201, 'Employers processed successfully')
        @employer_controller.response(400, 'Bad Request')
        @employer_controller.response(404, 'User not found')
        @employer_controller.response(500, 'Internal Server Error')
        def post(self, user_email):
            """
            Create or update multiple employers in bulk.
            """
            try:
                # Retrieve the list of employers from the request body
                employers_data = request.json
                if not employers_data or not isinstance(employers_data, list):
                    return {'message': 'Invalid input. Expected a list of employer data.'}, 400

                # Set up the database context
                set_database()

                # Using the database context manager to get the session
                with next(get_db()) as db:
                    # Call the bulk create/update service
                    result = EmployerService.create_or_update_bulk_employers(
                        db=db,
                        employers_data=employers_data,
                        user_id=user_email
                    )
                    # Return the response as JSON
                    return jsonify(result), 201

            except SQLAlchemyError as db_error:
                print(f"Database error occurred: {str(db_error)}")
                return {'message': 'Database error occurred.', 'error': str(db_error)}, 500

            except Exception as e:
                # Catch any other exception, log it, and return a structured error response
                print(f"Error processing bulk employers: {str(e)}")
                return {'message': 'An error occurred while processing the bulk employers.', 'error': str(e)}, 500


@employer_controller.route('/filter')  # Updated route
class EmployerFilter(Resource):
    @employer_controller.expect(employer_model_filter, validate=True)
    @employer_controller.doc('filter_employers')
    @employer_controller.response(200, 'Success', [employer_model])
    def post(self):  # Use POST for accepting a JSON body
        """Fetch employers with dynamic filters."""
        filters = request.json  # Parse the JSON payload
        set_database()
        # Validate input if necessary
        if not isinstance(filters, dict):
            return {"message": "Invalid input, JSON object expected."}, 400

        with next(get_db()) as db:
            try:

                filtered_employers = EmployerService.filter_employers(db, filters)
                return jsonify(filtered_employers)
            except Exception as e:
                return {"message": str(e)}, 500




@jwt_required()
@employer_controller.route('/employers/<string:id_empl>/<string:plant>')
@employer_controller.param('id_empl', 'The Employer identifier')
@employer_controller.param('plant', 'The Plant name')
class Employer(Resource):
    @employer_controller.doc('get_employer')
    @employer_controller.response(200, 'Success', employer_model)
    @employer_controller.response(404, 'Employer not found')
    def get(self, id_empl, plant):
        """Fetch an employer by ID and plant."""
        set_database()
        with next(get_db()) as db:
            employer = EmployerService.get_employer_by_id(db, id_empl, plant)
            if employer:
                return jsonify(employer)
            return jsonify({'error': 'Employer not found'}), 404

    @employer_controller.expect(employer_model, validate=True)
    @employer_controller.response(200, 'Employer updated successfully', employer_model)
    @employer_controller.response(404, 'Employer not found')
    def put(self, id_empl, plant):
        """Update an existing employer."""
        updated_data = request.json
        set_database()
        with next(get_db()) as db:
            employer = EmployerService.update_employer(db, id_empl, plant, updated_data)
            if employer:
                return jsonify({
                    'Id_Empl': employer.Id_Empl,
                    'Plant': employer.Plant,
                    'name_E': employer.name_E,
                    'department': employer.department,
                    'job': employer.job,
                    'plant': employer.plant
                })
            return jsonify({'error': 'Employer not found'}), 404

    @employer_controller.response(200, 'Employer deleted successfully')
    @employer_controller.response(404, 'Employer not found')
    def delete(self, id_empl, plant):
        """Delete an employer."""
        with next(get_db()) as db:
            employer = EmployerService.delete_employer(db, id_empl, plant)
            if employer:
                return jsonify({'message': 'Employer deleted successfully'})
            return jsonify({'error': 'Employer not found'}), 404

