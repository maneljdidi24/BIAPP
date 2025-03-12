import pyodbc   #For python3 MSSQL
import configparser
from Configuration import config
from dotenv import load_dotenv
import os

# Get the current working directory (where app.py is located)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the .env file
dotenv_path = os.path.join(current_directory, '..', 'Configuration', '.env')

# Load environment variables from .env file
load_dotenv(dotenv_path)


    

def getDataBaseConnection():
    try:
        with open('/run/secrets/flask_secret', 'r') as secret_file:
            secret = secret_file.read().strip()
            server = "ODBC Driver 18 for SQL Server"
    except FileNotFoundError:
        secret = os.getenv('DBSourceAzure_PWD', 'DataBase')
        server = "SQL Server"
    DSN = os.getenv('DBTarget_DSN', 'DSN')
    DataBase = os.getenv('DBSourceAzure_PWD', 'DataBase')
    test=False
    error=""
    try:
          cn=pyodbc.connect(f"Driver={server};" #For Connection ODBC Driver 18 for SQL Server
                    f"Server=192.168.122.40;"
                    f"UID=userWeb;"
                    f"PWD={secret};"
                    f"TrustServerCertificate=yes;")
          test=True
    except pyodbc.Error as ex:
        cn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
        elif sqlstate == '28000':
            error="Cannot open database"
        elif sqlstate == 'IM002':
            error="please check your driver"
        else: 
            error="We dont know the error"   
        print(sqlstate)       
    return (test,error,cn)        

    