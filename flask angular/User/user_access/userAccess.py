
from flask import  jsonify

def selectUserAccess(cnxn):
    try:
        sqlQuery = "SELECT * FROM [DBCoficab].[dbo].[User_Access]"

        query = "SELECT * FROM [DBCoficab].[dbo].[User_Access]"
        cursor = cnxn.cursor()
        cursor.execute(query)
        
        user_data = {}
        
        for row in cursor.fetchall():

            user, project, plant , Expiration_Date = row.User, row.Project, row.Plant , row.Expiration_Date
            if user not in user_data:
                user_data[user] = {
                    'projects': set(),
                    'plants': set(), 
                    'Expiration_Date' : set()
                }
            user_data[user]['projects'].add(project)
            user_data[user]['plants'].add(plant)
            user_data[user]['Expiration_Date'].add(Expiration_Date)
        
        # Convert sets to lists for JSON serialization
        user_access_list = [{'user': user_id, 'projects': list(data['projects']), 'plants': list(data['plants']) , 'Expiration_Date' :  list(data['Expiration_Date'])}
                        for user_id, data in user_data.items()]
        

        return user_access_list
        

    finally:
        cnxn.close()



def getDistinctUsers(cnxn):
    try:
        sqlQuery = "SELECT DISTINCT [User] FROM [DBCoficab].[dbo].[User_Access]"
        cursor = cnxn.cursor()

        # Fetch all rows as a list
        users = [row[0] for row in cursor.execute(sqlQuery).fetchall()]
        return users
    finally:
        cnxn.close()




def addUserAccess(cnxn, user, project, plant, expiration_date):
    try:
        cursor = cnxn.cursor()

        # Step 1: Fetch the region from the Aggregated_Plants table based on the plant
        region_query = "SELECT DISTINCT Region FROM [DBCoficab].[dbo].[Aggregated_Plants] WHERE [plant_Description] = ?"
        cursor.execute(region_query, plant)
        region = cursor.fetchone()
        
        if region is None:
            return f"Plant '{plant}' does not exist in Aggregated_Plants."
        region = region[0]  # Extract the region value from the result

        # Step 2: Check if user access already exists
        check_query = "SELECT COUNT(*) FROM [DBCoficab].[dbo].[User_Access] WHERE [User] = ? AND Project = ? AND Plant = ?"
        cursor.execute(check_query, (user, project, plant))
        user_access_count = cursor.fetchone()[0]
        
        if user_access_count > 0:
            return f"User Access for [User: {user}, Project: {project}, Plant: {plant}] already exists."

        # Step 3: Insert the user access with the region
        sqlQuery = """
            INSERT INTO [DBCoficab].[dbo].[User_Access] ([User], Project, Plant, Region, Expiration_Date) 
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sqlQuery, (user, project, plant, region, expiration_date))
        cnxn.commit()

        return {"msg": "The User Access has been added successfully.", "code": 200}
    
    except Exception as e:
        return {"msg": str(e), "code": 500}
    finally:
        cnxn.close()
    

def editUserAccess(cnxn, user_id, projects, plants, expiration_date):
    try:
        cursor = cnxn.cursor()
        
        # Step 1: Delete existing user access records for the provided user ID
        delete_query = "DELETE FROM [DBCoficab].[dbo].[User_Access] WHERE [User] = ?"
        cursor.execute(delete_query, (user_id,))
        cnxn.commit()

        # Step 2: Insert new User Access records with region
        for project in projects:
            for plant in plants:
                
                # Fetch the region from the Aggregated_Plants table based on the plant
                region_query = "SELECT DISTINCT Region FROM [DBCoficab].[dbo].[Aggregated_Plants] WHERE Plant = ?"
                cursor.execute(region_query, (plant['plant'],))
                region = cursor.fetchone()

                if region is None:
                    return {"msg": f"Plant '{plant['plant']}' does not exist in Aggregated_Plants.", "code": 404}

                region = region[0]  # Extract the region value from the result

                insert_query = """
                    INSERT INTO [DBCoficab].[dbo].[User_Access] ([User], Project, Plant, Region, Expiration_Date)
                    VALUES (?, ?, ?, ?, ?)
                """
                
                cursor.execute(insert_query, (user_id, project['Description'], plant['plant'], region, expiration_date))
        
        cnxn.commit()

        # Return success message
        return {"msg": "User Access has been updated successfully.", "code": 200}

    except Exception as e:
        return {"msg": str(e), "code": 500}
    
    finally:
        cnxn.close()









def deleteUserAccess(cnxn, user, project, plant):
    try:
        cursor = cnxn.cursor()
        sqlQuery = "DELETE FROM [DBCoficab].[dbo].[User_Access] WHERE [User]=? AND Project=? AND Plant=?"
        cursor.execute(sqlQuery, (user, project, plant))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Access has been deleted successfully.", "code": 200}
        else:
            return {"msg": f"No Access found with id '{user}'", "code": 404}
    
    finally:
        cnxn.close()

     
