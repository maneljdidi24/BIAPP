from flask import jsonify, request
from flask_cors import cross_origin
from . import topic_routes ,topic
from flask_jwt_extended import jwt_required

from dao import daoAll
""" 
@topic_routes.route('/addtopic', methods=['POST'])
@cross_origin()
def add_topic():
    cnxnT = daoSUS.getDataBaseConnection()
    try:
        topic_data = request.json     
        if cnxnT[0] == True:
            msg = topic.addElement(cnxnT[2], topic_data['ID_Element'], topic_data['Name_Element'], topic_data['Unit'], topic_data['ID_T'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@topic_routes.route('/modifytopic', methods=['PUT'])
@cross_origin()
def modify_topic():
    cnxnT = daoSUS.getDataBaseConnection()
    try:
        topic_data = request.json     
        if cnxnT[0] == True:
            msg = topic.modifyElement(cnxnT[2], topic_data['ID_Element'], topic_data['Name_Element'], topic_data['Unit'], topic_data['ID_T'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500 """


@topic_routes.route('/deletetopic', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_topic():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        topic_data = request.json     
        if cnxnT[0] == True:
            msg = topic.deleteElement(cnxnT[2], topic_data['ID_Element'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@topic_routes.route('/gettopics', methods=['GET'])
@cross_origin()
def get_topics():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        if cnxnT[0] == True:
            topics_list = topic.selectTopicTable(cnxnT[2])
            return jsonify(topics_list)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

