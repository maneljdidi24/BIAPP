from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from dao import daoAll
from . import emp,HR_routes


@HR_routes.route('/get', methods=['GET'])
@cross_origin()
def getEmployeeData():

    cnxnT = daoAll.getDataBaseConnection()
    if cnxnT[0]==False:
        print(cnxnT[1])
        return {"msg": cnxnT[1], "code": 300}
    else :
        msg=emp.displayEmployee(cnxnT[2])
        return msg