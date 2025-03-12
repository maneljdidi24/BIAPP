from dao.database import init_db
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from sqlalchemy.orm import Session
from ..services.CostCenterService import CostCenterService
from dao.database import get_db, init_db

cost_center_controller = Namespace('costCenters', description='Cost Center Management API')

# Cost Center Model for Swagger
cost_center_model = cost_center_controller.model('CostCenter', {
    'idcc': fields.String(required=True, description='The unique identifier of the cost center'),
    'ccDescription': fields.String(required=False, description='The description of the cost center'),
})

# Function to initialize the database
def set_database():
    init_db('hr2')

# API Routes
@cost_center_controller.route('/')
class CostCenterList(Resource):
    @cost_center_controller.doc('get_all_cost_centers')
    @cost_center_controller.response(200, 'Success', [cost_center_model])
    def get(self):
        """Fetch all cost centers."""
        set_database()
        with next(get_db()) as db:  # Open database session
            cost_centers = CostCenterService.get_all_cost_centers(db)
            return jsonify(cost_centers)

    @cost_center_controller.doc('create_cost_center')
    @cost_center_controller.expect(cost_center_model, validate=True)
    @cost_center_controller.response(201, 'Cost Center created successfully', cost_center_model)
    def post(self):
        """Create a new cost center."""
        cost_center_data = request.json
        set_database()
        with next(get_db()) as db:  # Open database session
            new_cost_center = CostCenterService.create_cost_center(db, cost_center_data)
            return jsonify(new_cost_center), 201


@cost_center_controller.route('/<string:idcc>')
@cost_center_controller.param('idcc', 'The unique identifier of the cost center')
class CostCenterDetail(Resource):
    @cost_center_controller.doc('get_cost_center_by_id')
    @cost_center_controller.response(200, 'Success', cost_center_model)
    @cost_center_controller.response(404, 'Cost Center not found')
    def get(self, idcc):
        """Fetch a cost center by its ID."""
        set_database()
        with next(get_db()) as db:  # Open database session
            cost_center = CostCenterService.get_cost_center_by_id(db, idcc)
            if cost_center:
                return jsonify(cost_center)
            return {'message': 'Cost Center not found'}, 404

    @cost_center_controller.doc('update_cost_center')
    @cost_center_controller.expect(cost_center_model, validate=False)
    @cost_center_controller.response(200, 'Cost Center updated successfully', cost_center_model)
    @cost_center_controller.response(404, 'Cost Center not found')
    def put(self, idcc):
        """Update an existing cost center."""
        set_database()
        updated_data = request.json
        with next(get_db()) as db:  # Open database session
            updated_cost_center = CostCenterService.update_cost_center(db, idcc, updated_data)
            if updated_cost_center:
                return jsonify(updated_cost_center)
            return {'message': 'Cost Center not found'}, 404

    @cost_center_controller.doc('delete_cost_center')
    @cost_center_controller.response(204, 'Cost Center deleted successfully')
    @cost_center_controller.response(404, 'Cost Center not found')
    def delete(self, idcc):
        """Delete a cost center."""
        set_database()
        with next(get_db()) as db:  # Open database session
            deleted_cost_center = CostCenterService.delete_cost_center(db, idcc)
            if deleted_cost_center:
                return '', 204
            return {'message': 'Cost Center not found'}, 404
