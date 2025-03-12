
import pyodbc   #For python3 MSSQL
import os

# Get the current working directory (where app.py is located)
current_directory = os.path.dirname(os.path.abspath(__file__))


# Load environment variables from .env file




def getAzureConnection():

    DSN = os.getenv('DBSourceAzure_DSN', 'DSN')
    PORT = os.getenv('DBSourceAzure_PORT', 'PORT')
    DataBase = os.getenv('DBSourceAzure_DataBase', 'DataBase')
    UDI = os.getenv('DBSourceAzure_UDI', 'UDI')
    PWD = os.getenv('DBSourceAzure_PWD', 'PWD')
    test=False
    error=""
    try:
        cnxn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"   #For Connection ODBC Driver 18 for SQL Server
                    "Server=192.168.122.40;"
                    "Database=Sales;"
                    "UID=use.rWeb;"
                    "PWD=UWC0f1c@b2024;"
                    "TrustServerCertificate=yes;")
        test=True
    except pyodbc.Error as ex:
        cnxn=""
        print(ex)
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error=" Please Connect to your VPN. Server is not found or not accessible."
        elif sqlstate == '42000':
            error="Cannot open database"
        elif sqlstate == 'IM002':
            error="Please check your driver"
        elif sqlstate == '28000':
            error="Check your credentials"
        else: 
            error="idk the error"
        print("yes")    #error=str(ex)
    return (test,error,cnxn)