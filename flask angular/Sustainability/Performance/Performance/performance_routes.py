from flask import jsonify, request
from flask_cors import cross_origin
from . import performance ,performance_routes
from flask_jwt_extended import  jwt_required

from dao import daoAll

@performance_routes.route('/getperformances', methods=['POST'])
@cross_origin()
@jwt_required()
def get_performances():
    
    try:
        data = request.json  # This retrieves JSON data from the request body
        cnxnT = daoAll.getDataBaseConnection()
        if cnxnT[0] == True:
            performances_list = performance.selectPerformanceTable(cnxnT[2],data)
            return jsonify(performances_list)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    


@performance_routes.route('/fromPlantGetDate/<plant>', methods=['POST'])
@cross_origin()
@jwt_required()
def fromPlantGetDate(plant):
    print('yes')
    try:
        print(plant)
        cnxnT = daoAll.getDataBaseConnection()
        if cnxnT[0] == True:
            month_year = performance.fromPlantGetDate(cnxnT[2],plant)
            return jsonify(month_year)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@performance_routes.route('/getdistinctyears', methods=['GET'])
@cross_origin()
@jwt_required()
def getdistinctyears():
    try:
        cnxnT = daoAll.getDataBaseConnection()
        if cnxnT[0] == True:
            performances_list = performance.getdistinctyears(cnxnT[2])
            return jsonify(performances_list)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@performance_routes.route('/getDdates', methods=['POST'])
@cross_origin()
@jwt_required()
def getdistinctdates():
    try:
        data = request.json 
        cnxnT = daoAll.getDataBaseConnection()
        if cnxnT[0] == True:
            performances_list = performance.getdistinctdate(cnxnT[2],data)
            return jsonify(performances_list)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    


@performance_routes.route('/modifyperformance', methods=['PUT'])
@cross_origin()
@jwt_required()
def modify_performance():
    try:
        cnxnT = daoAll.getDataBaseConnection()
        performance_data = request.json 
        if cnxnT[0] == True:  
            msg = performance.modifyPerformance(cnxnT[2], performance_data)
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}' ,"code": 500})
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', "code": 500})

@performance_routes.route('/deleteInsertPerformance', methods=['PUT'])
@cross_origin()
@jwt_required()
def deleteInsertPerformance():
    try:
        cnxnT = daoAll.getDataBaseConnection()
        performance_data = request.json 
        if cnxnT[0] == True:
           
            msg = performance.deleteInsertPerformance(cnxnT[2], performance_data)
            return jsonify(msg)
        else:
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}', "code": 500}) 
        
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}', "code": 500} ) 

@performance_routes.route('/InsertdescriptionPerformance', methods=['PUT'])
@cross_origin()
@jwt_required()
def InsertdescriptionPerformance():
    
    try:
        cnxnT = daoAll.getDataBaseConnection()
        performance_data = request.json 
        if cnxnT[0] == True:
           
            msg = performance.InsertdescriptionPerformance(cnxnT[2], performance_data)
            return jsonify(msg)
        else:
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}', "code": 500}) 
        
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}', "code": 500} )        

     
    
@performance_routes.route('/display_performance_for_update', methods=['POST'])
@cross_origin()
@jwt_required()
def display_performance_for_update():
    
    try:
        cnxnT = daoAll.getDataBaseConnection()
        performance_data = request.json 
        if cnxnT[0] == True:
           
            msg = performance.display_performance_for_update(cnxnT[2], performance_data['date'] ,performance_data['ID_Target'])
            return jsonify(msg)
        else:
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}', "code": 500}) 
        
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}', "code": 500} )      

@performance_routes.route('/addperformance', methods=['POST'])
@cross_origin()
@jwt_required()
def add_performance():
    try:
        cnxnT = daoAll.getDataBaseConnection()
        performance_data = request.json     
        if cnxnT[0] == True:
            msg = performance.addPerformance(cnxnT[2], performance_data['ID_Performance'], performance_data['Name_Performance'], performance_data['Metric'], performance_data['ID_T'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500



@performance_routes.route('/deleteperformance', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_performance():
    
    try:
        cnxnT = daoAll.getDataBaseConnection()
        performance_data = request.json     
        if cnxnT[0] == True:
            msg = performance.deletePerformance(cnxnT[2], performance_data['ID_Performance'])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
