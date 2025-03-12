import pyodbc   
import configparser

import time

import os
# Load environment variables from .env file

#**************************************************************************xpps


def getSOURCEConnectionXPPS_ma_int():
    base="X301SD"
    
    DRIVER=os.getenv('DBSource_ma_int_driver', 'driver')
    DSN = os.getenv('DBSource_ma_int_DSN', 'DSN')
    PORT = os.getenv('DBSource_ma_int_PORT', 'PORT')
    DataBase = os.getenv('DBSource_ma_int_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_ma_int_UDI', 'UDI')
    PWD = os.getenv('DBSource_ma_int_PWD', 'PWD')

    test=False
    error=""
    try:
        cnxn = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system='192.168.40.100',uid='wassim',pwd='wassim')
        print("serveur international & ma: connect to database "+base)
        return cnxn
    
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
        elif sqlstate == '42000':
            error="Cannot open database"
        elif sqlstate == 'IM002':
            error="Please check your driver"
        elif sqlstate == '28000':
            error="Check your credentials"
        else: 
            error="idk the error"
            #error=str(ex)
           # 
            print("connection error")
            exit()
        return (test,error,cnxn)  
#
def getSOURCEConnectionXPPS_kt():
    base="X301SD"
 
    DRIVER=os.getenv('DBSource_kt_driver', 'driver')
    DSN = os.getenv('DBSource_kt_DSN', 'DSN')
    PORT = os.getenv('DBSource_kt_PORT', 'PORT')
    DataBase = os.getenv('DBSource_kt_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_kt_UDI', 'UDI')
    PWD = os.getenv('DBSource_kt_PWD', 'PWD')


    test=False
    error=""
    start = time.time()
    try:      
        cnxn = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system='192.168.60.3',uid='wassim',pwd='wassim')
        
        test=True
        print("serveur KT :connect to database "+base)
        return cnxn
       
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
        elif sqlstate == '42000':
            error="Cannot open database"
        elif sqlstate == 'IM002':
            error="Please check your driver"
        elif sqlstate == '28000':
            error="Check your credentials"
        else: 
            error="idk the error"
            #error=str(ex)
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}ms') 
            print("connection error")
            exit()
#
def getSOURCEConnectionXPPS_EE():
    
    base="X30OSD"
    
    DRIVER=os.getenv('DBSource_EE', 'driver')
    DSN = os.getenv('DBSource_EE_DSN', 'DSN')
    PORT = os.getenv('DBSource_EE_PORT', 'PORT')
    DataBase = os.getenv('DBSource_EE_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_EE_UDI', 'UDI')
    PWD = os.getenv('DBSource_EE_PWD', 'PWD')

    test=False
    error=""
    start = time.time()
    
    try:      
        cnxn = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system='192.168.50.7',uid='BI',pwd='BI2023')
        test=True
        print("serveur COF EE :connect to database "+base)
        return cnxn
       
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
        elif sqlstate == '42000':
            error="Cannot open database"
        elif sqlstate == 'IM002':
            error="Please check your driver"
        elif sqlstate == '28000':
            error="Check your credentials"
        else: 
            error="idk the error"
            #error=str(ex)
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}ms') 
            print("connection  COF EE error")
            exit()

#**************************************************************************************Ln


def getSourceConnectionLn_Mexico():
    base="erplnfp9db"
    
    DSN = os.getenv('DBSource_mexico_DSN', 'DSN')
    PORT = os.getenv('DBSource_mexico_PORT', 'PORT')
    DataBase = os.getenv('DBSource_mexico_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_mexico_UDI', 'UDI')
    PWD = os.getenv('DBSource_mexico_PWD', 'PWD')
    test=False
    error=""
    start = time.time()

    
   
    try:
        cnxn = pyodbc.connect("Driver={SQL Server};"   #For Connection
                    f"Server={DSN};"
                    #f"PORT={PORT};"
                    f"Database={DataBase};"
                    f"UID={UDI};"
                    f"PWD={PWD};")
        test=True
        print("serveur Ln MEXICO:connect to database "+base)
        return cnxn
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
            print("1")  
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}s') 
            print("connection not found ")
            exit()        
        elif sqlstate == '42000':
            error="Cannot open database"            
        elif sqlstate == 'IM002':
            error="Please check your driver"          
        elif sqlstate == '28000':
            error="Check your credentials"
            print("4")
        else: 
            error="idk the error"
            print("5")
            #error=str(ex)        
        end = time.time()
        elapsed = end - start
        print(f'execution time : {elapsed:}s') 
        print("connection not found ")
        return (error)
        exit()

#
def getSourceConnectionLn_Chine():
    base="erplnfp9db"
    DSN = os.getenv('DBSource_chine_DSN', 'DSN')
    PORT = os.getenv('DBSource_chine_PORT', 'PORT')
    DataBase = os.getenv('DBSource_chine_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_chine_UDI', 'UDI')
    PWD = os.getenv('DBSource_chine_PWD', 'PWD')
    test=False
    error=""
    start = time.time()
    try:
        cnxn = pyodbc.connect("Driver={SQL Server};"   #For Connection
                    f"Server={DSN};"
                    #f"PORT={PORT};"
                    f"Database={DataBase};"
                    f"UID={UDI};"
                    f"PWD={PWD};")
        test=True
        print("serveur Ln Chine:connect to database "+base)
        return cnxn
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
            print("1")  
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}s') 
            print("connection not found ")
            exit()        
        elif sqlstate == '42000':
            error="Cannot open database"            
        elif sqlstate == 'IM002':
            error="Please check your driver"          
        elif sqlstate == '28000':
            error="Check your credentials"
            print("4")
        else: 
            error="idk the error"
            print("5")
            #error=str(ex)        
        end = time.time()
        elapsed = end - start
        print(f'execution time : {elapsed:}s') 
        print("connection not found ")
        return (error)
        exit()


#
def getSourceConnectionLn_tn_med_prod():  #tunis & med
    print("You are directed to Ln")
    base="coreln"
    DSN = os.getenv('DBSource_Tunis_DSN', 'DSN')
    PORT = os.getenv('DBSource_Tunisl_PORT', 'PORT')
    DataBase = os.getenv('DBSource_Tunis_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_Tunis_UDI', 'UDI')
    PWD = os.getenv('DBSource_Tunis_PWD', 'PWD')
    test=False
    error=""
    start = time.time()
    try:
        cnxn = pyodbc.connect("Driver={SQL Server};"   #For Connection
                        f"Server={DSN};"
    #                    f"PORT={PORT};"
                        f"Database={DataBase};"
                        f"UID={UDI};"
                        f"PWD={PWD};")
        test=True
        print("serveur Ln TUNIS:connect to database "+base)
        return cnxn
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
            print("1")  
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}s') 
            print("connection not found ")
            exit()        
        elif sqlstate == '42000':
            error="Cannot open database"            
        elif sqlstate == 'IM002':
            error="Please check your driver"          
        elif sqlstate == '28000':
            error="Check your credentials"
            print("4")
        else: 
            error="idk the error"
            print("5")
            #error=str(ex)        
        end = time.time()
        elapsed = end - start
        print(f'execution time : {elapsed:}s') 
        print("connection not found ")
        return (error)
        exit()


#
def getSourceConnection_LN_DB_Portugal():  #PT
    
    print("You are directed to Ln")
    
    DSN = os.getenv('DBSource_portugal_DSN', 'DSN')
    PORT = os.getenv('DBSource_portugal_PORT', 'PORT')
    DataBase = os.getenv('DBSource_portugal_DataBase', 'DataBase')
    UDI = os.getenv('DBSource_portugal_UDI', 'UDI')
    PWD = os.getenv('DBSource_portugal_PWD', 'PWD')
    test=False
    error=""


    start = time.time()
    try:
        cnxn = pyodbc.connect("Driver={SQL Server};"   #For Connection
                        f"Server={DSN};"
    #                    f"PORT={PORT};"
                        f"Database={DataBase};"
                        f"UID={UDI};"
                        f"PWD={PWD};")
        test=True
        print("serveur Ln PORTUGAL:connect to database "+DataBase)
        return cnxn
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
            print("1")  
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}s') 
            print("connection not found ")
            exit()        
        elif sqlstate == '42000':
            error="Cannot open database"            
        elif sqlstate == 'IM002':
            error="Please check your driver"          
        elif sqlstate == '28000':
            error="Check your credentials"
            print("4")
        else: 
            error="idk the error"
            print("5")
            #error=str(ex)        
        end = time.time()
        elapsed = end - start
        print(f'execution time : {elapsed:}s') 
        print("connection not found ")
        return (error)

#**********************************************************************************localhost


def getTargetConnection():
    DSN = os.getenv('DBTARGET_DSN', 'DSN')
    DataBase ='SALES'
    print(DSN,DataBase)
    error=""

    try:
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};" #For Connection
                    f"Server={DSN};"
                    f"Database={DataBase};"
                    "trusted_connection=yes;")
        print("connect to localhost ")
        return cnxn
        
    except pyodbc.Error as ex:
        print("connection error")

#  
def getAZUREConnection():
    base="Sales"
    DSN = os.getenv('DBAZURE_DSN', 'DSN')
    PORT = os.getenv('DBAZURE_PORT', 'PORT')
    DataBase = os.getenv('DBAZURE_DataBase', 'DataBase')
    UDI = os.getenv('DBAZURE_UDI', 'UDI')
    PWD = os.getenv('DBAZURE_PWD', 'PWD')
    test=False
    error=""
 
    start = time.time()
    try:
        cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"   #For Connection
                    f"Server={DSN};"
                    f"PORT={PORT};"
                    f"Database={DataBase};"
                    f"UID={UDI};"
                    f"PWD={PWD};")
        test=True
        print("serveur Azure :connect to database "+base)
        return cnxn
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
            print("1")  
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}s') 
            print("connection not found ")
            exit()        
        elif sqlstate == '42000':
            error="Cannot open database"            
        elif sqlstate == 'IM002':
            error="Please check your driver"          
        elif sqlstate == '28000':
            error="Check your credentials"
            print("4")
        else: 
            error="idk the error"
            print("5")
            #error=str(ex)        
        end = time.time()
        elapsed = end - start
        print(f'execution time : {elapsed:}s') 
        print("connection Azure not found ")
        return (error)
        exit()
        #source_engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={source_connection_string}', fast_executemany=True)
        #print("Connected to source database.")


#
def getAZURE_Connection2(base):
    
    DSN = os.getenv('DBAZURE_DSN', 'DSN')
    PORT = os.getenv('DBAZURE_PORT', 'PORT')
    DataBase = os.getenv('DBAZURE_DataBase', 'DataBase')
    UDI = os.getenv('DBAZURE_UDI', 'UDI')
    PWD = os.getenv('DBAZURE_PWD', 'PWD')
    test=False
    error=""

    start = time.time()
    try:
        cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"   #For Connection
                    f"Server={DSN};"
                    f"PORT={PORT};"
                    f"Database={DataBase};"
                    f"UID={UDI};"
                    f"PWD={PWD};")
        test=True
        print("serveur Azure :connect to database "+DataBase)
        return cnxn
    except pyodbc.Error as ex:
        cnxn=""
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            error="Server is not found or not accessible"
            print("1")  
            end = time.time()
            elapsed = end - start
            print(f'execution time : {elapsed:}s') 
            print("connection not found ")
            exit()        
        elif sqlstate == '42000':
            error="Cannot open database"            
        elif sqlstate == 'IM002':
            error="Please check your driver"          
        elif sqlstate == '28000':
            error="Check your credentials"
            print("sqlstate == '28000'")
        else: 
            error="idk the error"
            print("5")
            #error=str(ex)        
        end = time.time()
        elapsed = end - start
        print(f'execution time : {elapsed:}s') 
        print("connection Azure not found ")
        return (error)
        exit()


        


        


