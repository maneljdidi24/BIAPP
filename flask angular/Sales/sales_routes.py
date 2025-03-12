import io
import json
from flask import jsonify, request
from flask_cors import cross_origin
from . import sales_routes, sales
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from dao import daoAll,daoengine
from flask import send_file
import pandas as pd



@sales_routes.route('/SelectSalesDisplay500/<region>/<startdate>/<endDate>/<Offset>', methods=['POST'])
@cross_origin()
@jwt_required()
def SelectSalesDisplay500(region,startdate,endDate,Offset):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')
    cnxnT = daoAll.getDataBaseConnection()
    user_email = get_jwt_identity()
    if cnxnT[0]==False:
        #print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=sales.SelectSalesDisplay500(cnxnT[2],region,startdate,endDate,Offset,plants,user_email)
        return msg
    
    """ 
@sales_routes.route('/getAll/<region>/<startdate>/<endDate>', methods=['POST'])
@cross_origin()
@jwt_required()
def getsalesdataAll(region, startdate, endDate):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')
    
    # Get the database connection
    cnxnT = daoAll.getDataBaseConnection()
    user_email = get_jwt_identity()  
    
    # Check if the connection was successful
    if not cnxnT[0]:
        # Return error message, error, and code
        return {"msg": None, "error": cnxnT[1], "code": 300}
    else:
        try:
            # Execute the query function
            result = sales.selectTableAll(cnxnT[2], region, startdate, endDate, plants, user_email)
            result_dict = json.loads(result)

            # If the result contains an error, return the error message
            if "error" in result_dict:
                print(f"Error querying data from /: {result_dict['error']}")
                return {"msg": None, "error": result_dict['error'], "code": 500}

            # Return successful result
            print(f"User {user_email} finished querying all data for region: {region}. Result: done")
            return {"msg": result_dict, "error": None, "code": 200}, 200
        
        except Exception as e:
            # Capture the exception and return it in the response
            error_message = f"Error while querying the database: {str(e)}"
            print(error_message)
            return {"msg": None, "error": error_message, "code": 500} """
    
@sales_routes.route('/SelectAllSalesForCSV/<region>/<startdate>/<endDate>', methods=['POST'])
@cross_origin()
@jwt_required()
def SelectAllSalesForCSV(region, startdate, endDate):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')
    
    # Get the database connection
    cnxnT = daoengine.getDataBaseConnection()
    user_email = get_jwt_identity()  

    if not cnxnT[0]:
        return {"msg": None, "error": cnxnT[1], "code": 300}
    else:
        try:
            # Execute the query function
            df = sales.SelectAllSalesForCSV(cnxnT[2], region, startdate, endDate, plants, user_email)
            
            if df is None:
                return {"msg": None, "error": "No data found", "code": 404}

            # Create a CSV file in memory
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            return send_file(
    io.BytesIO(csv_buffer.getvalue().encode()),
    download_name=f"{region}_daaata_{startdate}_to_{endDate}.csv",  # Use download_name instead of attachment_filename
    as_attachment=True
)
        
        except Exception as e:
            error_message = f"Error while querying the database: {str(e)}"
            print(error_message)
            return {"msg": None, "error": error_message, "code": 500}


   
  
        
@sales_routes.route('/getcountsalesdata/<plant>/<startdate>/<endDate>', methods=['POST'])
@cross_origin()
@jwt_required()
def getcountsalesdata(plant,startdate,endDate):
    data = request.json  # This retrieves JSON data from the request body
    plants = data.get('plants')
    cnxnT = daoAll.getDataBaseConnection()
    user_email = get_jwt_identity()
    if cnxnT[0]==False:
      
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=sales.getcountsalesdata(cnxnT[2],plant,startdate,endDate,plants,user_email)
        print(f"User {user_email} finished counting records for region: {plant}. Result: {msg}")
        return msg        
    

@sales_routes.route('/CheckAzurServer', methods=['GET'])
@jwt_required()
@cross_origin()
def CheckAzurServer():
    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0]==False:
       
        return {"msg": cnxnT[1], "code": 300}
    else :
        return {"msg": cnxnT[1], "code": 200}
    
@sales_routes.route('/getPlantFromRegion/<plant>', methods=['GET'])
@jwt_required()
@cross_origin()
def getPlantFromRegion(plant):
    cnxnT = daoAll.getDataBaseConnection()
    user_email = get_jwt_identity()
    if cnxnT[0]==False:
        return {"msg": cnxnT[1], "code": 300}
    else:
        msg=sales.getPlantFromRegion(cnxnT[2],plant,user_email)
        print(f"User {user_email} finished querying plants for region: {plant}. result: {msg}")
        return msg