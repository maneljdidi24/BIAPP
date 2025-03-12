import json


def selectTable2(cnxn, region, startdate, enddate,Offset,plants):
    try:
        if region == "TN":
            region = 'Global_Sales_Tunis'
        elif region   == 'PT':
            region = 'Global_Sales_Portugal'
        elif region   == 'MX':
            region = 'Global_Sales_Mexico'
        elif region   == 'MA':
            region = 'Global_Sales_Maroc'
        elif region   == 'EE':
            region = 'Global_Sales_EE'
        sqlQuery = f"SELECT * FROM [Sales].[dbo].{region} where Current_Inv_Date BETWEEN '{startdate}' AND '{enddate}'" 

        # Add conditions for each plant
        for idx, plant in enumerate(plants):
            if idx == 0:
                sqlQuery += f" and plant = '{plant}'"
            else:
                sqlQuery += f" OR plant = '{plant}'"

        # Add other conditions
        sqlQuery += f" ORDER BY id_line  OFFSET {Offset}00 ROWS FETCH NEXT 1000 ROWS ONLY;"

        cursor = cnxn.cursor()
        # Fetch all rows as a list of dictionaries and Plant = '{plant}'
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        print("Selection done for PurchaseTable")
        return json.dumps(results, default=str)
    finally:
        cnxn.close()


def selectTableAll(cnxn, region, startdate, enddate,plants):
    try:
        if region == "TN":
            region = 'Global_Sales_Tunis'
        elif region   == 'PT':
            region = 'Global_Sales_Portugal'
        elif region   == 'MX':
            region = 'Global_Sales_Mexico'
        elif region   == 'MA':
            region = 'Global_Sales_Maroc'
        elif region   == 'EE':
            region = 'Global_Sales_EE'
        
        sqlQuery = f"SELECT * FROM [Sales].[dbo].{region} where Current_Inv_Date BETWEEN '{startdate}' AND '{enddate}'"

        # Add conditions for each plant
        for idx, plant in enumerate(plants):
            if idx == 0:
                sqlQuery += f" and plant = '{plant}'"
            else:
                sqlQuery += f" OR plant = '{plant}'"


        cursor = cnxn.cursor()
        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        print("Selection done for all sales")
        return json.dumps(results, default=str)
    finally:
        cnxn.close()

def count(cnxn, region, startdate, enddate,plants):
    try:
        if region == "TN":
            region = 'Global_Sales_Tunis'
        elif region == 'PT':
            region = 'Global_Sales_Portugal'
        elif region == 'MX':
            region = 'Global_Sales_Mexico'
        elif region == 'MA':
            region = 'Global_Sales_Maroc'
        elif region == 'EE':
            region = 'Global_Sales_EE'
        
        sqlQuery = f"SELECT count(*) FROM [Sales].[dbo].{region} WHERE Current_Inv_Date BETWEEN '{startdate}' AND '{enddate}'"
                # Add conditions for each plant
        for idx, plant in enumerate(plants):
            if idx == 0:
                sqlQuery += f" and plant = '{plant}'"
            else:
                sqlQuery += f" OR plant = '{plant}'"

        cursor = cnxn.cursor()
        cursor.execute(sqlQuery)
        count_result = str(cursor.fetchone()[0])  # Convert count result to string
        return count_result # Return the count value
    finally:
        cnxn.close()  # Close the connection

def plants(cnxn, region):
    try:
        if region == "TN":
            region = 'Global_Sales_Tunis'
        elif region == 'PT':
            region = 'Global_Sales_Portugal'
        elif region == 'MX':
            region = 'Global_Sales_Mexico'
        elif region == 'MA':
            region = 'Global_Sales_Maroc'
        elif region == 'EE':
            region = 'Global_Sales_EE'
        
        sqlQuery = f"SELECT distinct [Plant] FROM [Sales].[dbo].{region}"
        
        cursor = cnxn.cursor()
        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        print("Selection done for PurchaseTable")
        return json.dumps(results, default=str)

    finally:
        cnxn.close()  # Close the connection