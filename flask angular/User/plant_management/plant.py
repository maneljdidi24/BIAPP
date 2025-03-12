import pyodbc
from flask import jsonify

def selectTable(cnxn):
    try:
        sqlQuery = "SELECT * FROM [DBCoficab].[dbo].[Plant]"
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        plants_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        return plants_list
    finally:
        cnxn.close()


def AddPlant(cnxn, Plant, Region, Sales_Company, Inv_Company, NEW):
    try:
        cursor = cnxn.cursor()

        # Check if plant already exists
        check_query = "SELECT COUNT(*) FROM [DBCoficab].[dbo].[Plant] WHERE Plant = ?"
        cursor.execute(check_query, (Plant,))
        plant_count = cursor.fetchone()[0]

        if plant_count > 0:
            return {"msg": f"Project with Code_Project '{Plant}' already exists.", "code": 400}


        # If plant doesn't exist, proceed with insertion
        sqlQuery = "INSERT INTO [DBCoficab].[dbo].[Plant] (Plant, Region, Sales_Company, Inv_Company, NEW) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sqlQuery, (Plant, Region, Sales_Company, Inv_Company, NEW))
        cnxn.commit()
        return {"msg": "The Plant has been added successfully.", "code": 200}
    finally:
        cnxn.close()


def EditPlant(cnxn, Plant, Region, Sales_Company, Inv_Company, NEW):
    try:
        cursor = cnxn.cursor()
        sqlQuery = """
            UPDATE [DBCoficab].[dbo].[Plant]
            SET Region=?, Sales_Company=?, Inv_Company=?, NEW=?
            WHERE Plant=?
        """
        cursor.execute(sqlQuery, (Region, Sales_Company, Inv_Company, NEW, Plant))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Plant has been edited successfully.", "code": 200}
        else:
            return {"msg": f"No Plant found with Plant Id '{Plant}'", "code": 404}
    finally:
        cnxn.close()


def DeletePlant(cnxn, Plant):
    try:
        cursor = cnxn.cursor()
        sqlQuery = "DELETE FROM [DBCoficab].[dbo].[Plant] WHERE Plant=?"
        cursor.execute(sqlQuery, (Plant,))
        cnxn.commit()
                # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Plant has been deleted successfully.", "code": 200}
        else:
            return {"msg": f"No Plant found with Plant Id '{Plant}'", "code": 404}
    finally:
        cnxn.close()


def GetPlants(cnxn):
    try:
        cursor = cnxn.cursor()

        # Query to fetch distinct local areas
        cursor.execute("SELECT DISTINCT plant_Description , Plant FROM [DBCoficab].[dbo].[Aggregated_Plants]")
        local_areas = cursor.fetchall()
     
        # Convert to a list of dictionaries
        local_area_list = [{'plant_Description': area[0], 'plant': area[1]} for area in local_areas]
        
        return local_area_list
    except Exception as e:
        return jsonify({'error': str(e)})
    

    
def GetPlantsforuser(cnxn, email):
    try:
        cursor = cnxn.cursor()

        # Query to fetch distinct local areas
        query = """SELECT DISTINCT UA.Plant, AP.[plant_Description] 
FROM [DBCoficab].[dbo].[User_Access] UA
INNER JOIN [DBCoficab].[dbo].[Aggregated_Plants] AP
    ON UA.Plant COLLATE SQL_Latin1_General_CP1_CI_AS = AP.plant_Description COLLATE SQL_Latin1_General_CP1_CI_AS
WHERE UA.[User] = ?; """
        cursor.execute(query, email)

        # Fetch all rows and convert them to a list of regions
        local_areas = cursor.fetchall()
        # Convert to a list of dictionaries
        local_area_list = [{'plant_Description': area[1], 'plant': area[0]} for area in local_areas]
        
        return local_area_list
    except Exception as e:
        return jsonify({'error': str(e)})   


    
def GetRegionforuser(cnxn, email):
    try:
        cursor = cnxn.cursor()
        print('inside function')
        # Query to fetch distinct regions for the user
        query = "SELECT DISTINCT Region FROM [DBCoficab].[dbo].[User_Access] WHERE [User] = ?"
        cursor.execute(query, email)

        # Fetch all rows and convert them to a list of regions
        regions = cursor.fetchall()
        listregion = [region[0] for region in regions]  # Extract region values
        return listregion
    except Exception as e:
        return {'error': str(e)}    
    finally:
        cnxn.close()   

def GetRegion(cnxn):
    try:
        cursor = cnxn.cursor()

        # Query to fetch distinct regions
        cursor.execute("SELECT DISTINCT Region FROM [DBCoficab].[dbo].[Aggregated_Plants]")
        regions = cursor.fetchall()

        # Convert to a list of dictionaries
        region_list = [{'value': region[0], 'viewValue': region[0]} for region in regions]
        return region_list
    except Exception as e:
        return jsonify({'error': str(e)})   
    
    finally:
        cnxn.close()