import json
import os
import pandas as pd
from sqlalchemy import create_engine

""" 
def selectTableAll(cnxn, region, startdate, enddate, plants, email):
    engine = None
    try:
        # Map the region names to the correct table names
        region_mapping = {
            "Tunisia": 'Global_Sales_Tunis',
            "Portugal": 'Global_Sales_Portugal',
            "Mexico": 'Global_Sales_Mexico',
            "Morocco": 'Global_Sales_Maroc',
            "Eastern Europe": 'Global_Sales_EE',
            "China": 'Global_Sales_Chine'
        }
        region = region_mapping.get(region, region)

        # SQL query for fetching data
        sqlQuery = f
            SELECT [Trans_Type], [Invoice_N], [Currency], [Desc_STPB], [Inv_Quantity], 
                   [Qty_Unit], [Price], [Price_Unit], [Item], [Item_Description], 
                   [Net_Line_Amount], [Ship_To_BP], [Ship_To_Description], [Mterial_Exchange], 
                   [Metal_weight_sales], [Added_value], [Metal_Rate], [Contract_N], [Shipment], 
                   [Shipment_line], [Part_Number], [Plant], [Net_Line_Amount_HC], 
                   [Home_Currency], [Reporting_Amount_Euro], [Reporting_Currency_Euro], 
                   [Reporting_Amount_USD], [Reporting_Currency_USD], [Material_Type], 
                   [Inv_Company], [Sales_Company], [Region], [Current_Inv_Date], [Client], 
                   [ItemGroupe],  [Inv_Quantity_Final], [New_QTY_unit], 
                   [New_price], [New_price_unit], [ItemGroupe_Desc], [addedvalue_price] 
            FROM [Sales].[dbo].{region} WITH (NOLOCK) 
            WHERE Current_Inv_Date BETWEEN '{startdate}' AND '{enddate}' AND Active = 1
        
        
        # Add plant filter if plants are provided
        if plants:
            sqlQuery += " AND (" + " OR ".join([f"Plant = '{plant}'" for plant in plants]) + ")"

        # Query the database using SQLAlchemy engine
        df = pd.read_sql(sqlQuery, engine)
        
        # Check if the query returned any data
        if df.empty:
            print(f"No data found for the specified query for user {email}.")
            return None

        # Generate a CSV file with the queried data
        csv_filename = f"{region}_data_{startdate}_to_{enddate}_{email}.csv".replace(" ", "_")
        df.to_csv(csv_filename, index=False)
        
        print(f"User {email} successfully generated the CSV file: {csv_filename}")
        return os.path.abspath(csv_filename)

    except Exception as e:
        print(f"Error while querying the database or generating the CSV: {e}")
        return None

    finally:
        # Close the connection
        if engine is not None:
            engine.dispose()  # Disposes the connection pool, effectively closing all connections
            print(f"Database connection closed for user {email}.")
 """

def SelectAllSalesForCSV(engine, region, startdate, enddate, plants, email):
    try:
        region_mapping = {
            "Tunisia": 'Global_Sales_Tunis',
            "Portugal": 'Global_Sales_Portugal',
            "North America": 'Global_Sales_Mexico',
            "Morocco": 'Global_Sales_Maroc',
            "Eastern Europe": 'Global_Sales_EE',
            "China": 'Global_Sales_Chine'
        }
        region = region_mapping.get(region, region)

        # SQL query for fetching data
        sqlQuery = f"""select GS.[Trans_Type], GS.[Invoice_N], GS.[Currency], GS.[Sold_To_BP], GS.[Desc_STPB], GS.[Inv_Quantity], GS.[Qty_Unit], GS.[Price], GS.[Price_Unit],
                GS.[Item], GS.[Item_Description], item.[FAM],item.[WIRE]
                ,item.[COF_ID] , item.[SECTION] , item.[R_D_Brand] , item.[INDUSTRY] , item.[PRDT_END_TYP] , item.[INS_END_TYP] ,item.[XSEC_TYP] ,item.[TEMP_CLASS] 
                ,GS.[Net_Line_Amount], GS.[Ship_To_BP], GS.[Ship_To_Description], GS.[Mterial_Exchange], GS.[Metal_weight_sales],
                GS.[Added_value], GS.[Metal_Rate], GS.[Contract_N], GS.[Shipment], GS.[Shipment_line], GS.[Part_Number], GS.[Plant], GS.[Net_Line_Amount_HC], GS.[Home_Currency],
                GS.[Reporting_Amount_Euro], GS.[Reporting_Currency_Euro], GS.[Reporting_Amount_USD], GS.[Reporting_Currency_USD], GS.[Material_Type], GS.[Inv_Company],
                GS.[Sales_Company], GS.[Region], GS.[Current_Inv_Date], BPG.[CLIENT_desc],BPG.[CLIENT_G],BPG.[CLIENT_SUBG], GS.[ItemGroupe],
                  GS.[Inv_Quantity_Final], GS.[New_QTY_unit],
                GS.[New_price], GS.[New_price_unit], GS.[addedvalue_price]
                FROM [Sales].[dbo].{region} GS WITH (NOLOCK) left join [Sales].[dbo].[ITEM] item on item.[CODE_ITEM] = GS.Item 
                left join [Sales].[dbo].[MATCHING_BP_Groupe] BPG on BPG.BP = GS.Sold_To_BP and BPG.InvC = GS.Inv_Company
                WHERE (Current_Inv_Date >= '{startdate}' AND Current_Inv_Date <= '{enddate}') AND Active = '1'"""
       
         # Add filtering for plants
        if plants:
            sqlQuery += " AND (" + " OR ".join([f"Plant = '{plant}'" for plant in plants]) + ")"

        # Execute the query and load the data into a DataFrame
        df = pd.read_sql(sqlQuery, engine)

        print("***********************************************")
        print(sqlQuery)
        print("***********************************************")
        
        # Check if the DataFrame is empty
        if df.empty:
            msg = f"No data found for the specified query for user {email}."
            return  ({"msg": msg, "code": 404}),200

        # If data is found, return it with a 200 status code
        return df

    except Exception as e:
        # If an error occurs, return a 500 status code with the error message
        error_msg = f"Error while querying the database: {str(e)}"
        return ({"msg": error_msg, "code": 500}),200


def SelectSalesDisplay500 (cnxn, region, startdate, enddate, Offset, plants, email):
    try:
        # Indicate the user has started the process
        print(f"User {email} started querying data for region: {region}, from {startdate} to {enddate} with offset: {Offset}...")

        # Adjust region name based on the provided value
        if region == "Tunisia":
            region = 'Global_Sales_Tunis'
        elif region == 'Portugal':
            region = 'Global_Sales_Portugal'
        elif region == 'North America':
            region = 'Global_Sales_Mexico'
        elif region == 'Morocco':
            region = 'Global_Sales_Maroc'
        elif region == 'Eastern Europe':
            region = 'Global_Sales_EE'
        elif region == 'China':
            region = 'Global_Sales_Chine'

        # Prepare the SQL query
        sqlQuery = f"""select GS.[Trans_Type], GS.[Invoice_N], GS.[Currency], GS.[Sold_To_BP], GS.[Desc_STPB], GS.[Inv_Quantity], GS.[Qty_Unit], GS.[Price], GS.[Price_Unit],
                GS.[Item], GS.[Item_Description], item.[FAM],item.[WIRE]
                ,item.[COF_ID] , item.[SECTION] , item.[R_D_Brand] , item.[INDUSTRY] , item.[PRDT_END_TYP] , item.[INS_END_TYP] ,item.[XSEC_TYP] ,item.[TEMP_CLASS] 
                ,GS.[Net_Line_Amount], GS.[Ship_To_BP], GS.[Ship_To_Description], GS.[Mterial_Exchange], GS.[Metal_weight_sales],
                GS.[Added_value], GS.[Metal_Rate], GS.[Contract_N], GS.[Shipment], GS.[Shipment_line], GS.[Part_Number], GS.[Plant], GS.[Net_Line_Amount_HC], GS.[Home_Currency],
                GS.[Reporting_Amount_Euro], GS.[Reporting_Currency_Euro], GS.[Reporting_Amount_USD], GS.[Reporting_Currency_USD], GS.[Material_Type], GS.[Inv_Company],
                GS.[Sales_Company], GS.[Region], GS.[Current_Inv_Date], BPG.[CLIENT_desc],BPG.[CLIENT_G],BPG.[CLIENT_SUBG], GS.[ItemGroupe],
                  GS.[Inv_Quantity_Final], GS.[New_QTY_unit],
                GS.[New_price], GS.[New_price_unit], GS.[addedvalue_price]
                FROM [Sales].[dbo].{region} GS WITH (NOLOCK) left join [Sales].[dbo].[ITEM] item on item.[CODE_ITEM] = GS.Item 
                left join [Sales].[dbo].[MATCHING_BP_Groupe] BPG on BPG.BP = GS.Sold_To_BP and BPG.InvC = GS.Inv_Company
                WHERE (Current_Inv_Date >= '{startdate}' AND Current_Inv_Date <= '{enddate}') AND Active = '1'"""
        
       # Add conditions for each plant
        if plants:
            sqlQuery += " AND (" + " OR ".join([f"Plant LIKE '%{plant}%'" for plant in plants]) + ")"

        # Add offset and fetch conditions
        sqlQuery += f" ORDER BY [ID_Line] OFFSET {Offset}00 ROWS FETCH NEXT 500 ROWS ONLY;"

        print(f"Executing SQL query: {sqlQuery}")

        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        # If no data is returned, inform the user
        if not results:
            return ({"msg": f"No data found for the specified dates.", "code": 404}),200

        # Return the results with a success message
        return json.dumps(results, default=str)
    
    except Exception as e:
        # Extract the error message part (this example assumes SQL error messages)
        error_msg_full = str(e)
        
        # Find and extract the specific message (e.g., "Invalid column name 'CODE=_ITEM'.")
        # This typically appears after the last ']' in SQL Server errors
        error_msg = error_msg_full.split(']')[-1].strip() if ']' in error_msg_full else error_msg_full
        
        # Prepare the final message for the user
        user_friendly_msg = f"Error: {error_msg}"
        
        # Print the full detailed error for debugging/logging purposes
        print(f"Error while querying the database: {error_msg_full}")
        
        # Return the simplified user-friendly message with a 500 status code
        return ({"msg": user_friendly_msg, "code": 500}), 200



    finally:
        # Close the connection and print the connection close message
        cnxn.close()





def getcountsalesdata(cnxn, region, startdate, enddate, plants, email):
    try:
        # Indicate the user has started the process
        print(f"User {email} started counting records for region: {region}, from {startdate} to {enddate}...")

        # Adjust region name based on the provided value
        if region == "Tunisia":
            region = 'Global_Sales_Tunis'
        elif region == 'Portugal':
            region = 'Global_Sales_Portugal'
        elif region == 'North America':
            region = 'Global_Sales_Mexico'
        elif region == 'Morocco':
            region = 'Global_Sales_Maroc'
        elif region == 'Eastern Europe':
            region = 'Global_Sales_EE'
        elif region == 'China':
            region = 'Global_Sales_Chine'
        
        # Prepare the SQL query
        sqlQuery = f"SELECT count(*) FROM [Sales].[dbo].{region} WITH (NOLOCK) WHERE Current_Inv_Date BETWEEN '{startdate}' AND '{enddate}' and Active = '1' "
        
        # Add conditions for each plant
        if plants:
            sqlQuery += " AND ("
            
            # Loop through each plant and append the appropriate SQL condition
            for idx, plant in enumerate(plants):
                if idx == 0:
                    sqlQuery += f"plant like '%{plant}%'"
                else:
                    sqlQuery += f" OR plant like '%{plant}%'"
            
            # Close the parentheses for the plant condition
            sqlQuery += ")"

        print(f"Executing count SQL query: {sqlQuery}")
        cursor = cnxn.cursor()
        
        # Execute the SQL query
        cursor.execute(sqlQuery)

        # Fetch the count result
        count_result = str(cursor.fetchone()[0])  # Convert count result to string

        
        
        return count_result  # Return the count value
    
    finally:
        cnxn.close()


def getPlantFromRegion(cnxn, region, email):
    try:
        # Indicate the user has started the process
        print(f"User {email} started querying plants for region: {region}...")

        # Prepare the SQL query
        sqlQuery = f"SELECT [Plant],[plant_Description] FROM [DBCoficab].[dbo].[Aggregated_Plants] WITH (NOLOCK) WHERE Region = '{region}'"
        
        cursor = cnxn.cursor()
        
        # Execute the query and fetch all rows
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        # Return results in JSON format
        return json.dumps(results, default=str)
    
    finally:
        # Close the connection and indicate the user has closed the connection
        cnxn.close()
  