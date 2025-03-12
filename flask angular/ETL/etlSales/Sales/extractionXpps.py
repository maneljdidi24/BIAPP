from flask import jsonify
import pyodbc   #For python3 MSSQL
import configparser
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd
import json



from ETL.etlSales.sql_sales import EE,maroc
import sqlalchemy




def truncateTable(cnxn,tables):
    sqlQuery = f"truncate table {tables}"
    cursor = cnxn.cursor()
    cursor.execute(sqlQuery)
    cnxn.commit()
    print("Truncate Table "+ "***"+ tables +"***")


def insertIntoTable_kt(Start,End,cnxnS,cnxnT,tables):

    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    x=maroc.extract_kt(Start,End,cnxnS)
    x.to_sql(tables, engine, if_exists='append', index=False)
    print("insert Into Table "+"***"+tables+"***"+" done")
    cnxnT.close()    
    cnxnS.close()

#*****maroc
def insertIntoTable_ma_int(Start,End,cnxnS,cnxnT,tables):
   
    print("hello")
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
    x=maroc.extract_ma_int(Start,End,cnxnS)
    print("ok")
    
    x.to_sql(tables, engine, if_exists='append', index=False)
    print("insert Into Table "+"***"+tables+"***"+" done")
    cnxnT.close()    
    cnxnS.close()


def insertIntoTable_EE(Firm,Start,End,cnxnS,cnxnT,tables):
    print("1")
    engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)

    x=EE.extract_EE(Firm,Start,End,cnxnS)
    print ("2")
    x.to_sql(tables, engine, if_exists='append', index=False )
    print("insert Into Table "+"***"+tables+"***"+" done")
    
    cnxnT.close()    
    cnxnS.close()