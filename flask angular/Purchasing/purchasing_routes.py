from flask import jsonify, request 
from flask_cors import  cross_origin
from . import purchasing_routes, purchasing , extraction
from Configuration import config
from dao import daoAll
from flask_jwt_extended import jwt_required
from dao import daoAll


@purchasing_routes.route('/updateInvest/<Po>/<Poline>/<Receipt_Number>/<Receipt_Number_Lines>/<invest>', methods=['PUT'])
@cross_origin()
def update_investment_route(Po, Poline, Receipt_Number, Receipt_Number_Lines, invest):
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0]==False:
        return jsonify({
        'error': cnxnT[1],
        'server': "target",
        'plant': "102",
        'code': '300'
                })
    else :
        msg=purchasing.updateInvestment(cnxnT[2], Po, Poline, Receipt_Number, Receipt_Number_Lines, invest)
        return msg
    
@purchasing_routes.route('/get/<plant>/<startdate>/<endDate>/<project>', methods=['GET'])
@cross_origin()
def selectPurchase_Plant_Project(plant,startdate,endDate,project):
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0]==False:
        return jsonify({
        'error': cnxnT[1],
        'server': "target",
        'plant': "102",
        'code': '300'
                })
    else :
        msg=purchasing.selectPurchase_Plant_Project(cnxnT[2],plant,startdate,endDate,project)
        return msg    
    

    ###testtt
@purchasing_routes.route('/get/<plant>', methods=['GET'])
@cross_origin()
def selectPurchase(plant):
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0]==False:
        return jsonify({
        'error': cnxnT[1],
        'server': "target",
        'plant': "102",
        'code': '300'
                })
    else :
        msg=purchasing.selectPurchase(cnxnT[2],plant)
        return msg    
    


@purchasing_routes.route('/extract/<plant>/<Start>/<End>', methods=['GET'])
@cross_origin()
def putRequest(plant,Start,End):
    """     req_data = request.get_json()
    req_args = request.view_args """
    #print('req_args: ', req_args)
    cnxnT = daoAll.getTargetConnection()
    cnxnS = daoAll.getSourceConnection()
    """     Start = req_data['Start']
    End = req_data['End']
    print(Start)
    print(End) """
    if cnxnT[0]==False:
        return jsonify({
        'msg': cnxnT[1],
        'server': "target",
        'code': '300'
                })
    if cnxnS[0]==False:
        return jsonify({
        'msg': cnxnS[1],
        'server': "source",
        'code': '300'
                })
    else :
        print("connexion works biennnnn")
        #extraction.truncateTable(cnxnT)
        msg=extraction.insertIntoTable(plant,Start,End,cnxnS[2],cnxnT[2])
        return jsonify({
                'plant': plant,
                'code': '200',
                'msg': msg,
              #  'req_data': req_data 
                        })    