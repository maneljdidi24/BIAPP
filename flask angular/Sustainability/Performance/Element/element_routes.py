from flask import jsonify, request
from flask_cors import cross_origin
from . import element_routes ,element
from flask_jwt_extended import jwt_required

from dao import daoAll

@element_routes.route('/addelement', methods=['POST'])
@cross_origin()
def add_element():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        element_data = request.json     
        if cnxnT[0] == True:
            msg = element.addElement(cnxnT[2], element_data['ID_Element'], element_data['Name_Element'], element_data['Unit'], element_data['ID_T'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@element_routes.route('/modifyelement', methods=['PUT'])
@cross_origin()
def modify_element():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        element_data = request.json     
        if cnxnT[0] == True:
            msg = element.modifyElement(cnxnT[2], element_data['ID_Element'], element_data['Name_Element'], element_data['Unit'], element_data['ID_T'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@element_routes.route('/deleteelement', methods=['DELETE'])
@cross_origin()
def delete_element():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        element_data = request.json     
        if cnxnT[0] == True:
            msg = element.deleteElement(cnxnT[2], element_data['ID_Element'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@element_routes.route('/getelements', methods=['GET'])
@cross_origin()
def get_elements():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        if cnxnT[0] == True:
            elements_list = element.selectElementTable(cnxnT[2])
            return jsonify(elements_list)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

