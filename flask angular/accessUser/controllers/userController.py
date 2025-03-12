from flask_restx import Namespace, Resource, fields
from flask import request, jsonify

from sqlalchemy.orm import Session
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
import pandas as pd
from dao.database import get_db, init_db
from accessUser.services.userService import UserService

# Define the namespace for user-related routes
user_controller = Namespace('users', description='User management operations')

# Define a User model for Swagger documentation
user_model = user_controller.model('User', {
    'ID_User_Login': fields.String(required=True, description='User login ID'),
    'Position': fields.String(description='User position'),
    'Type': fields.String(description='User type')
})


def set_database():
    init_db('bi_access_test') 


@cross_origin()  
@jwt_required() 
@user_controller.route('/')
class UserList(Resource):
    @user_controller.doc('get_users')
    @user_controller.response(200, 'Success', [user_model])
    def get(self):
        """Fetch all users."""
        set_database()
        #document_tables_and_relationships()
        #generate_models('bi_access_test') 
        with next(get_db()) as db:
            users_with_access = UserService.get_all_users_with_access(db)
            return jsonify(users_with_access)

    @user_controller.expect(user_model, validate=True)
    @user_controller.response(201, 'User created successfully', user_model)
    def post(self):
        """Create a new user."""
        user_data = request.json
        with next(get_db()) as db:
            new_user = UserService.create_user(db, user_data)
            return jsonify({
                'ID_User_Login': new_user.ID_User_Login,
                'Position': new_user.Position,
                'Type': new_user.Type
            }), 201

@user_controller.route('/<int:user_id>')
@user_controller.param('user_id', 'The User identifier')
class User(Resource):
    @user_controller.doc('get_user')
    @user_controller.response(200, 'Success', user_model)
    @user_controller.response(404, 'User not found')
    def get(self, user_id):
        """Fetch a user by ID."""
        with next(get_db()) as db:
            user = UserService.get_user_by_id(db, user_id)
            if user:
                return jsonify({
                    'ID_User_Login': user.ID_User_Login,
                    'Position': user.Position,
                    'Type': user.Type
                })
            return jsonify({'error': 'User not found'}), 404

    @user_controller.expect(user_model, validate=True)
    @user_controller.response(200, 'User updated successfully', user_model)
    @user_controller.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user."""
        updated_data = request.json
        with next(get_db()) as db:
            user = UserService.update_user(db, user_id, updated_data)
            if user:
                return jsonify({
                    'ID_User_Login': user.ID_User_Login,
                    'Position': user.Position,
                    'Type': user.Type
                })
            return jsonify({'error': 'User not found'}), 404

    @user_controller.response(200, 'User deleted successfully')
    @user_controller.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user."""
        with next(get_db()) as db:
            user = UserService.delete_user(db, user_id)
            if user:
                return jsonify({'message': 'User deleted successfully'})
            return jsonify({'error': 'User not found'}), 404
