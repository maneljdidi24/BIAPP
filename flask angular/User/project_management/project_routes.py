from flask import jsonify, request
from flask_cors import cross_origin
from . import project_routes, project
from flask_jwt_extended import jwt_required
from dao import daoAll

@project_routes.route('/getproject', methods=['GET'])
@cross_origin()
def get_project():
    cnxnT = daoAll.getDataBaseConnection()
    if not cnxnT[0]:
        return jsonify({
            'msg': cnxnT[1],
            'code': 300
        })
    else:
        msg = project.selectTable(cnxnT[2])
        return jsonify(msg)

@project_routes.route('/addproject', methods=['POST'])
@cross_origin()
def add_project():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        project_data = request.json
        if cnxnT[0]:
            msg = project.AddProject(cnxnT[2], project_data['Code_Project'], project_data['Description'])

            return jsonify(msg)
        else:
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}', 'code': 500})
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}', 'code': 500})

@project_routes.route('/deleteproject/<project_id>', methods=['DELETE'])
@cross_origin()
def delete_project(project_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        if cnxnT[0]:
            msg = project.DeleteProject(cnxnT[2], project_id)
            return jsonify(msg)
        else:
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}', 'code': 500})
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}', 'code': 500})

@project_routes.route('/editproject/<project_id>', methods=['PUT'])
@cross_origin()
def edit_project(project_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        project_data = request.json
        if cnxnT[0]:
            msg = project.EditProject(cnxnT[2], project_id, project_data.get('Description'))

            return jsonify(msg)
        else:
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}', 'code': 500})
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}', 'code': 500})
