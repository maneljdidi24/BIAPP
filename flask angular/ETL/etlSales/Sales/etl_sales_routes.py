from flask import jsonify, request
from flask_cors import cross_origin
from . import etl_sales_routes, sales,etl_mj
from dao import azure



@etl_sales_routes.route('/get/<region>/<startdate>/<endDate>/<Offset>', methods=['POST'])
@cross_origin()

def getsalesdata(region,startdate,endDate,Offset):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')

    cnxnT = azure.getAzureConnection()
    if cnxnT[0]==False:
        print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=sales.selectTable2(cnxnT[2],region,startdate,endDate,Offset,plants)
        return msg
    
@etl_sales_routes.route('/getAll/<region>/<startdate>/<endDate>', methods=['POST'])
@cross_origin()

def getsalesdataAll(region,startdate,endDate):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')
    cnxnT = azure.getAzureConnection()
    if cnxnT[0]==False:
        print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=sales.selectTableAll(cnxnT[2],region,startdate,endDate ,plants)
        return  msg
  
        
@etl_sales_routes.route('/count/<plant>/<startdate>/<endDate>', methods=['POST'])
@cross_origin()

def getcountsalesdata(plant,startdate,endDate):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')
    cnxnT = azure.getAzureConnection()
    if cnxnT[0]==False:
        print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=sales.count(cnxnT[2],plant,startdate,endDate,plants)
        print("oun"+ msg)
        return msg        
    

@etl_sales_routes.route('/CheckAzurServer', methods=['GET'])
@cross_origin()

def CheckAzurServer():
    cnxnT = azure.getAzureConnection()
    if cnxnT[0]==False:
        print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        return {"msg": cnxnT[1], "code": 200}
    
@etl_sales_routes.route('/plants/<plant>', methods=['GET'])
@cross_origin()

def getdistinctplants(plant):
    cnxnT = azure.getAzureConnection()
    if cnxnT[0]==False:
        print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=sales.plants(cnxnT[2],plant)
        return msg



#*********************************************************************


#*****Manel    


@etl_sales_routes.route('/extract', methods=['POST'])
@cross_origin()
def get_data_extract():
    tt = request.json
    print(tt)
    
    rg = tt['region']
    d1 = tt['date1']
    d2 = tt['date2']
    print(rg)
    etl_mj.F_Extract(rg,d1,d2)
    return tt

