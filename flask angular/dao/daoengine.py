from sqlalchemy import create_engine
import os
import pyodbc
from urllib.parse import quote_plus

def getDataBaseConnection():
    error = ""
    test = False
    engine = None

    try:
        # Retrieve the secret from Docker secrets or environment variable
        with open('/run/secrets/flask_secret', 'r') as secret_file:
            secret = secret_file.read().strip()
            encoded_password = quote_plus(secret)
    except FileNotFoundError:
        secret = os.getenv('DBSourceAzure_PWD', 'DataBase')
        encoded_password = quote_plus(secret)

    try:
        # Create a SQLAlchemy engine using the ODBC driver
        connection_string = (
            f"mssql+pyodbc://userWeb:{encoded_password}@192.168.122.40/Sales"
            f"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        )
        # Create the SQLAlchemy engine
        engine = create_engine(connection_string)
        
        
        # Test the connection
        with engine.connect() as conn:
            test = True  # Connection is successful
            print("Connection to the database established successfully.")
        
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error = "Server is not found or not accessible"
        elif sqlstate == '28000':
            error = "Cannot open database"
        elif sqlstate == 'IM002':
            error = "Please check your ODBC driver"
        else:
            error = "Unknown error occurred"
        engine = None
    except Exception as e:
        error = f"An error occurred: {e}"
        engine = None

    return (test, error, engine)

