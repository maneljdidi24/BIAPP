from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from . import userManage_routes,user

from dao import daoAll


from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

online_users = {}

@userManage_routes.route('/getuser', methods=['GET'])
@jwt_required()
@cross_origin()
#@jwt_required()
def get_user():
    #current_user = get_jwt_identity()
    #print(current_user)
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0]==False:
        return jsonify({
        'error': cnxnT[1],
        'server': "target",
        'plant': "102",
        'status': '300'
                })
    else :
        print("get_user works")
        msg=user.selectTable(cnxnT[2])
        return msg


@userManage_routes.route('/adduser', methods=['POST'])
@jwt_required()
@cross_origin()
def add_user():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        user_data=request.json      
        if cnxnT[0]==True:
            msg=user.AddUser(cnxnT[2], user_data['ID_User_Login'],user_data['Password'], user_data['Position'],  user_data['Type'],  user_data['Level_'])
            return jsonify(msg)
        else:
                return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    

@userManage_routes.route('/deleteuser/<user_id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_user(user_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        if cnxnT[0] == True:
            msg = user.DeleteUser(cnxnT[2], user_id)

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    

@userManage_routes.route('/edituser/<user_id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def edit_user(user_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        user_data = request.json
        if cnxnT[0] == True:
            msg = user.ModifyUser(cnxnT[2], user_id, user_data.get('Password'), user_data.get('Position'),
                                user_data.get('Type'), user_data.get('Level_'))

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    

@userManage_routes.route('/getUserById/<user_id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_user_with_id(user_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        if cnxnT[0] == True:
            # Fetch user by ID
            user_data = user.GetUserById(cnxnT[2], user_id)
            
            if user_data:
                return jsonify(user_data), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500





           