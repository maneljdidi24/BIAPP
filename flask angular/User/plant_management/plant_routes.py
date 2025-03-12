from flask import jsonify, request
from flask_cors import cross_origin
from . import plant_routes, plant
from flask_jwt_extended import jwt_required
from dao import daoAll

@plant_routes.route('/getplant', methods=['GET'])
@cross_origin()
def get_plant():
    cnxnT = daoAll.getDataBaseConnection()
    if not cnxnT[0]:
        return jsonify({
            'error': cnxnT[1],
            'server': "target",
            'plant': "102",
            'status': '300'
        })
    else:
        print("Connection works well")
        msg = plant.selectTable(cnxnT[2])
        return msg

@plant_routes.route('/addplant', methods=['POST'])
@cross_origin()
def add_plant():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        plant_data = request.json
        if cnxnT[0]:
            msg = plant.AddPlant(cnxnT[2], plant_data['Plant'], plant_data['Region'], plant_data['Sales_Company'], plant_data['Inv_Company'], plant_data['NEW'])

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@plant_routes.route('/deleteplant/<plant_id>', methods=['DELETE'])
@cross_origin()
def delete_plant(plant_id):
    cnxnT =  daoAll.getDataBaseConnection()
    try:
        if cnxnT[0]:
            msg = plant.DeletePlant(cnxnT[2], plant_id)

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@plant_routes.route('/editplant/<plant_id>', methods=['PUT'])
@cross_origin()
def edit_plant(plant_id):
    cnxnT = daoAll.getDataBaseConnection()
    try:
        plant_data = request.json
        if cnxnT[0]:
            msg = plant.EditPlant(cnxnT[2], plant_id, plant_data.get('Region'), plant_data.get('Sales_Company'), plant_data.get('Inv_Company'), plant_data.get('NEW'))

            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@plant_routes.route('/getplants', methods=['GET'])
@jwt_required()
@cross_origin()
def getplant():
    cnxnT =  daoAll.getDataBaseConnection()
    try:
        if cnxnT[0]:
            msg = plant.GetPlants(cnxnT[2])
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500    

@plant_routes.route('/GetPlantsforuser', methods=['POST'])
@jwt_required()
@cross_origin()
def GetPlantsforuser():
    cnxnT =  daoAll.getDataBaseConnection()
    data = request.json.get('data')
    try:
        if cnxnT[0]:
            msg = plant.GetPlantsforuser(cnxnT[2],data)
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500   

@plant_routes.route('/GetRegionforuser', methods=['POST'])
@jwt_required()
@cross_origin()
def GetRegionforuser():
    cnxnT =  daoAll.getDataBaseConnection()
    data = request.json.get('data')
    try:
        if cnxnT[0]:
            msg = plant.GetRegionforuser(cnxnT[2],data)
            return jsonify(msg)
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500     


@plant_routes.route('/getRegions', methods=['GET'])
@jwt_required()
@cross_origin()
def getregion():
    cnxnT =  daoAll.getDataBaseConnection()
    try:
        if cnxnT[0]:
            msg = plant.GetRegion(cnxnT[2])
            return jsonify(msg)
            
        else:
            return jsonify({'error': f'Database connection error: {cnxnT[1]}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500    