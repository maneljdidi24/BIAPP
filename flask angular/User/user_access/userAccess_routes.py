from flask import jsonify, request
from flask_cors import cross_origin
from . import userAccess_routes,userAccess
from flask_jwt_extended import jwt_required
from dao import daoAll

@userAccess_routes.route('/getuseraccess', methods=['GET'])
@cross_origin()
def get_user_access():
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0] == False:
        return jsonify({
            'error': cnxnT[1],
            'server': "target",
            'plant': "102",
            'status': '300'
        })
    else:
        print("Connection works well")
        msg = userAccess.selectUserAccess(cnxnT[2])
        return jsonify(msg)
    

@userAccess_routes.route('/getdistinctusers', methods=['GET'])
@cross_origin()
def get_distinct_users():
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0] == False:
        return jsonify({
            'error': cnxnT[1],
            'server': "target",
            'plant': "102",
            'status': '300'
        })
    else:
        try:
            distinct_users = userAccess.getDistinctUsers(cnxnT[2])
            return jsonify(distinct_users)
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500




@userAccess_routes.route('/adduseraccess', methods=['POST'])
@cross_origin()
def add_user_access():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        user_access_data = request.json    
        print(user_access_data)  
        if cnxnT[0] == True:
            
            msg = userAccess.addUserAccess(cnxnT[2], user_access_data['user'], user_access_data['project'], user_access_data['plant'], user_access_data['expiration_date'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    

@userAccess_routes.route('/deleteuseraccess/<user_id>', methods=['DELETE'])
@cross_origin()
def delete_user_access(user_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        if cnxnT[0] == True:
            msg = userAccess.deleteUserAccess(cnxnT[2], user_id)

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@userAccess_routes.route('/edituseraccess/<user_id>', methods=['PUT'])
@cross_origin()
def edit_user_access(user_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        user_access_data = request.json
        if cnxnT[0] == True:
            msg = userAccess.editUserAccess(cnxnT[2], user_id, user_access_data['project'], user_access_data['plant'],
                                              user_access_data['expiration_date'])

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
