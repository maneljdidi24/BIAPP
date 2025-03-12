from flask import jsonify
import pyodbc   #For python3 MSSQL
import configparser
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd

import json
from sql import tn

    
    


def insertIntoTable(plant, Start, End, cnxnS, cnxnT):
    try:
        engine = create_engine('mssql+pyodbc://', creator=lambda: cnxnT)
        data_to_insert = pd.read_sql(tn.extract(plant, Start, End), cnxnS)

        if not data_to_insert.empty:
            data_to_insert.to_sql('PurTab', engine, if_exists='append', index=False)
            return f"Data extraction works! {len(data_to_insert)} lines inserted successfully."
        else:
            return "No data to be inserted."
        

    except IntegrityError as e:
        # Sample data
        try:    
            fromQuery = data_to_insert.copy()  # Selecting all columns
            # Reading only the primary key columns from PurTab
            primary_key_columns = ['PO_Number', 'PO_Line',  'PO_sqnb' ,'Receipt_Number', 'Receipt_Number_Lines','Received_Quantity']
            fromtable = pd.read_sql('SELECT PO_Number , PO_Line ,  PO_sqnb ,Receipt_Number  ,Receipt_Number_Lines , Received_Quantity from PurTab', engine)
            

            
            # Merge dataframes using an outer join based on the primary key
            merged_df = pd.merge(fromQuery, fromtable, how='outer', indicator=True, on=primary_key_columns)
            
            # Separate the data into two dataframes based on the indicator column
            not_in_fromtable = merged_df[merged_df['_merge'] == 'left_only']
           # Drop the _merge column
            not_in_fromtable = not_in_fromtable.drop('_merge', axis=1)

            if not_in_fromtable.empty:
                return "All Purchase Orders are already in the database. No data inserted."

            # Append the data to the SQL table
            not_in_fromtable.to_sql('PurTab', engine, if_exists='append', index=False)
            return f"Some Purchase Orders were missing and have been inserted. {len(not_in_fromtable)} lines inserted. Data insertion complete."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            cnxnS.close()
            cnxnT.close()
        




