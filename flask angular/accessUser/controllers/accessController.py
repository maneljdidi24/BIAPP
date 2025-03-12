""" from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from dao.database import get_db, init_db
from accessUser.services.accessService import AccessService

access_controller = Blueprint('access_controller', __name__)

@access_controller.before_request
def set_database():
    init_db('bi_access_test')  # Initialize the connection to the specified database

@access_controller.route('/', methods=['GET'])
def get_all_access():

    with next(get_db()) as db:  # Get database session
        access_records = AccessService.get_all_access(db)
        return jsonify([{
            'idAccess': access.idAccess,
            'access_desc': access.access_desc
        } for access in access_records])

@access_controller.route('/<int:access_id>', methods=['GET'])
def get_access_by_id(access_id):
   
    with next(get_db()) as db:
        access = AccessService.get_access_by_id(db, access_id)
        if access:
            return jsonify({
                'idAccess': access.idAccess,
                'access_desc': access.access_desc
            })
        return jsonify({'error': 'Access record not found'}), 404

@access_controller.route('/', methods=['POST'])
def create_access():
    
    access_data = request.json
    with next(get_db()) as db:
        new_access = AccessService.create_access(db, access_data)
        return jsonify({
            'idAccess': new_access.idAccess,
            'access_desc': new_access.access_desc
        }), 201

@access_controller.route('/<int:access_id>', methods=['PUT'])
def update_access(access_id):
 
    updated_data = request.json
    with next(get_db()) as db:
        access = AccessService.update_access(db, access_id, updated_data)
        if access:
            return jsonify({
                'idAccess': access.idAccess,
                'access_desc': access.access_desc
            })
        return jsonify({'error': 'Access record not found'}), 404

@access_controller.route('/<int:access_id>', methods=['DELETE'])
def delete_access(access_id):

    with next(get_db()) as db:
        access = AccessService.delete_access(db, access_id)
        if access:
            return jsonify({'message': 'Access record deleted successfully'})
        return jsonify({'error': 'Access record not found'}), 404
 """