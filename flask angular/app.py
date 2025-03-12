import logging
import bcrypt

from Configuration import config
from flask import Flask, render_template, request, jsonify
import os, re, datetime
from datetime import timedelta
import pyodbc   #For python3 MSSQL
import configparser
from User.user_access.userAccess_routes import userAccess_routes
from User.user_management import user
from HR.controllers.employerController import employer_controller
from accessUser.controllers.userController import user_controller
 
import jwt
from apps.routes import main_routes
from User.user_management.userManage_routes import userManage_routes
from User.project_management.project_routes import project_routes
from User.plant_management.plant_routes import plant_routes
from HR.controllers.departmentController import department_controller
from HR.controllers.jobController import job_controller
from HR.controllers.costCenterController import cost_center_controller
from Sales.sales_routes import sales_routes
from ETL.etlSales.Sales.etl_sales_routes import etl_sales_routes
from Sustainability.sustainability_routes import sustainability_routes
from Purchasing.purchasing_routes import purchasing_routes
from flask_cors import CORS, cross_origin
from flask_compress import Compress
#from security import verify_token  
from flask_bcrypt import Bcrypt
import usermodel
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from dao import daoAll
from sql import tn
from flask_restx import Api

from hrBudget.controllers.budgetController import budget_controller

secret_key ="59cac0bd2b956435f32ae836a5eb3c80c2c27f1fc8d632ca1bee97c5a8f56ba3"

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = secret_key  # Change this to your secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

@app.route('/2')
def testenv():
    try:
        # Example API call
        FLASK_ENV = os.getenv("FLASK_ENV", "NODE_ENV")
        return f"Hello World! API Response: {FLASK_ENV}"
    except Exception as e:
        return f"Error fetching data from API: {e}"


@app.route('/1')
def hello_world():
    return  jsonify({
        'error': "hello",
        'server': "source",
        'code': '300'
                })





# Initialize Flask-RESTX API
api = Api(app, version='1.0', title='User Management API', description='API for managing users')



@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    cnxnT = daoAll.getDataBaseConnection()
    try:
        user_data=request.json 
        if cnxnT[0]==True:
            msg=user.login_user(cnxnT[2], user_data['email'],user_data['password'])
                # Set up logging
            action = "login"
            logging.info(f'User {cnxnT[1]} performed action: {msg}')
            return msg 
        else:
            action = "login"
            logging.info(f'User {cnxnT[1]} performed action: {action}')
            return jsonify({'msg': f'Database connection error: {cnxnT[1]}'}), 500 
        
    except Exception as e:
        return jsonify({'msg': f'Internal server error: {str(e)}'}), 500 
    


@app.route('/protected', methods=['GET'])
@cross_origin()
@jwt_required()
def protected():
    return jsonify({'hello': 'world'}), 200

app.register_blueprint(main_routes)
app.register_blueprint(userManage_routes, url_prefix='/users')
api.add_namespace(department_controller)
api.add_namespace(employer_controller)
api.add_namespace(user_controller)

api.add_namespace(budget_controller)

api.add_namespace(job_controller)
api.add_namespace(cost_center_controller)
app.register_blueprint(project_routes, url_prefix='/projects')
app.register_blueprint(plant_routes, url_prefix='/plants')
app.register_blueprint(sales_routes, url_prefix='/sales') 
app.register_blueprint(etl_sales_routes, url_prefix='/etlsales')
               
app.register_blueprint(userAccess_routes, url_prefix='/access')
app.register_blueprint(purchasing_routes, url_prefix='/purchasing')
app.register_blueprint(sustainability_routes, url_prefix='/sustainablity')



if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port=5000)








     

    















#if __name__ == '__main__':
  #  app.run(debug=True)

