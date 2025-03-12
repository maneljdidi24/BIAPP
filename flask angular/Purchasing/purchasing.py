



    
def selectPurchase(cnxn,plant):
    plant= plant+"FULL"
    sqlQuery = f"select top 1000 * from PurchaseTable" 
    cursor = cnxn.cursor()
    cursor = cursor.execute(sqlQuery).fetchall()
    results = [tuple(row) for row in cursor]
    print("selection done Table")
    return json.dumps(results, default=str)
    
import json

def selectPurchase_Plant_Project(cnxn, plant, startdate, enddate,project):
    try:
        if plant == "TN":
            plant = 102102
        else:
            plant = 104104
        if project == "purchase":
            project = 11
        elif project == "metal":
            project = 12
        sqlQuery = f"SELECT * FROM [DBCoficab].[dbo].[PurchaseTable] where Purchase_Office like '%{project}' and Order_Date BETWEEN '{startdate}' AND '{enddate}' AND leadSite_ID = '{plant}'"
        print(sqlQuery)
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        print("Selection done for PurchaseTable")
        return json.dumps(results, default=str)
    finally:
        cnxn.close()

def updateInvestment(cnxn, Po, Poline, Receipt_Number,Receipt_Number_Lines,invest):
    try:
        sqlQuery = f"UPDATE PurchaseTable SET investment = '{invest}' WHERE PO_Number = '{Po}' AND PO_Line = '{Poline}' AND Receipt_Number = '{Receipt_Number}' AND Receipt_Number_Lines = '{Receipt_Number_Lines}';"

        cursor = cnxn.cursor()
        cursor.execute(sqlQuery)
        cnxn.commit()

        print("modif done for PurchaseTable")
        return {"msg": "Update done successfully.", "code": 200}
    finally:
        cnxn.close()