from HR.models import Department
from HR.services.departmentService import DepartmentService
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from dao.database import get_db, init_db
from sqlalchemy.exc import SQLAlchemyError


# Define the namespace for employer-related routes
department_controller = Namespace('department', description='Employer management operations')

# Define model for department
department_model = department_controller.model('Department', {
    'ID_Department': fields.String(description='Department ID'),
    'Nom_Department': fields.String(description='Department name')
})

# Function to initialize database
def set_database():
    init_db('hr2')

@jwt_required()
@department_controller.route('/')
class DepartmentList(Resource):
    @department_controller.doc('get_department')
    @department_controller.response(200, 'Success', [department_model])
    def get(self):
        """Fetch all departments with details."""
        print("Fetch all departments with details.")
        set_database()
        with next(get_db()) as db:
            departments_with_details = DepartmentService.get_all_departments(db)
            return jsonify(departments_with_details)

    @department_controller.route('/single', endpoint='create_single_department')
    class SingleEmployerResource(Resource):
        @department_controller.expect(department_model, validate=True)
        @department_controller.response(201, 'Employer created successfully', department_model)
        def post(self):
            """Create a single employer."""
            employer_data = request.json
            set_database()
            with next(get_db()) as db:
                new_employer = DepartmentService.create_employer(db, employer_data)
                return jsonify({
                    'Id_Empl': new_employer.Id_Empl,
                    'Plant': new_employer.Plant,
                    'name_E': new_employer.name_E,
                    'department': new_employer.department,
                    'job': new_employer.job,
                    'plant': new_employer.plant
                }), 201


    @department_controller.route('/bulk/<string:user_email>', endpoint='create_bulk_departments')
    class BulkEmployerResource(Resource):
        @department_controller.expect([department_model], validate=True)
        @department_controller.response(201, 'departments processed successfully')
        @department_controller.response(400, 'Bad Request')
        @department_controller.response(404, 'User not found')
        @department_controller.response(500, 'Internal Server Error')
        def post(self, user_email):
            """
            Create or update multiple departments in bulk.

            Args:
                user_email (str): The email of the user performing the action.

            Returns:
                JSON response containing details of inserted, updated, and errors.
            """
            try:
                # Retrieve the list of departments from the request body
                departments_data = request.json
                if not departments_data or not isinstance(departments_data, list):
                    return {'message': 'Invalid input. Expected a list of employer data.'}, 400

                if not departments_data or not isinstance(departments_data, list):
                    return {'message': 'Invalid input. Expected a list of employer data.'}, 400

                # Set up the database context
                set_database()

                # Using the database context manager to get the session
                with next(get_db()) as db:
                    # Call the bulk create/update service
                    result = DepartmentService.create_or_update_bulk_departments(
                        db=db,
                        departments_data=departments_data,
                        user_id=user_email
                    )

                    # Return the response as JSON
                    return result, 201

            except SQLAlchemyError as db_error:
                print(f"Database error occurred: {str(db_error)}")
                return {'message': 'Database error occurred.', 'error': str(db_error)}, 500

            except Exception as e:
                # Catch any other exception, log it, and return a structured error response
                print(f"Error processing bulk departments: {str(e)}")
                return {'message': 'An error occurred while processing the bulk departments.', 'error': str(e)}, 500

@department_controller.route('/<string:id_empl>/<string:plant>')
@department_controller.param('id_empl', 'The Employer identifier')
@department_controller.param('plant', 'The Plant name')
class Employer(Resource):
    @department_controller.doc('get_employer')
    @department_controller.response(200, 'Success', department_model)
    @department_controller.response(404, 'Employer not found')
    def get(self, id_empl, plant):
        """Fetch an employer by ID and plant."""
        with next(get_db()) as db:
            employer = DepartmentService.get_department_by_id(db, id_empl, plant)
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

    @department_controller.expect(department_model, validate=True)
    @department_controller.response(200, 'Employer updated successfully', department_model)
    @department_controller.response(404, 'Employer not found')
    def put(self, id_empl, plant):
        """Update an existing employer."""
        updated_data = request.json
        with next(get_db()) as db:
            employer = DepartmentService.update_department(db, id_empl, plant, updated_data)
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

    @department_controller.response(200, 'Employer deleted successfully')
    @department_controller.response(404, 'Employer not found')
    def delete(self, id_empl, plant):
        """Delete an employer."""
        with next(get_db()) as db:
            employer = DepartmentService.delete_employer(db, id_empl, plant)
            if employer:
                return jsonify({'message': 'Employer deleted successfully'})
            return jsonify({'error': 'Employer not found'}), 404
