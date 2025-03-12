
from datetime import timedelta
import json
import bcrypt
from flask import jsonify
import pyodbc
from flask_jwt_extended import create_access_token


def selectTable(cnxn):
    try: 
        sqlQuery = f"select * from [DBCoficab].[dbo].[User]" 
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        users_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        return users_list
    finally:
        cnxn.close()


def AddUser(cnxn, ID_User_Login, Password, Position, Type, Level_):
    cursor = cnxn.cursor()

    # Check if user already exists
    check_query = "SELECT COUNT(*) FROM [DBCoficab].[dbo].[User] WHERE ID_User_Login = ?"
    cursor.execute(check_query, (ID_User_Login,))
    user_count = cursor.fetchone()[0]
    if user_count > 0:
        return {"msg":f"User with ID_User_Login '{ID_User_Login}' already exists.", "code": 400}

    # If user doesn't exist, proceed with insertion
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 

    sqlQuery = "INSERT INTO [DBCoficab].[dbo].[User] (ID_User_Login, Password, Position, Type, Level_) VALUES (?, ?, ?, ?, ?)"
    try:
        cursor.execute(sqlQuery, (ID_User_Login, hashed_password, Position, Type, Level_))
        cnxn.commit()

        return {"msg": "The User has been added successfully.", "code": 200}
    finally:
        cnxn.close()



def ModifyUser(cnxn, ID_User_Login, Password, Position, Type, Level_):
    cursor = cnxn.cursor()

    # Hash the new password before updating
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 

    sqlQuery = """
        UPDATE [DBCoficab].[dbo].[User]
        SET Password=?, Position=?, Type=?, Level_=? 
        WHERE ID_User_Login=?
    """
    try:
        cursor.execute(sqlQuery, (hashed_password, Position, Type, Level_, ID_User_Login))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The User has been edited successfully.", "code": 200}
        else:
            return {"msg": f"No User found with ID_User_Login '{ID_User_Login}'", "code": 404}
    finally:
        cnxn.close()




def create_token(user_id):
    return create_access_token(identity=user_id)

def DeleteUser(cnxn, ID_User_Login):
    cursor = cnxn.cursor()
    sqlDeleteUser = "DELETE FROM [DBCoficab].[dbo].[User] WHERE ID_User_Login=?"
    sqlDeleteUserAccess = "DELETE FROM [DBCoficab].[dbo].[User_Access] WHERE [User]=?"

    try:
        # Delete from User_Access first (to avoid foreign key constraint issues)
        cursor.execute(sqlDeleteUserAccess, (ID_User_Login,))
        # Now delete from User table
        cursor.execute(sqlDeleteUser, (ID_User_Login,))
        
        cnxn.commit()

        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The User and their access records have been deleted successfully.", "code": 200}
        else:
            return {"msg": f"No User found with Id User '{ID_User_Login}'", "code": 404}
    finally:
        cnxn.close()


def check_password(plain_password, stored_hashed_password):
    # Hash the provided plain password
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
    
    # Compare the hashed password with the stored hashed password
    return hashed_password == stored_hashed_password


def login_user(cnxn, email, password):
    try:
        with cnxn.cursor() as cursor:
            # Check if email exists
            cursor.execute("SELECT * FROM [DBCoficab].[dbo].[User] WHERE ID_User_Login = ?", (email,))
            user = cursor.fetchone()
            if user is None:
                return {"msg": "Email does not exist.", "code": 401}
            
            # Verify password
            hashed_password = user[1].encode('utf-8')  # Ensure hashed_password is bytes
            password_bytes = password.encode('utf-8')  # Ensure password is bytes

            if bcrypt.checkpw(password_bytes, hashed_password):
                # Password matches, return user object (excluding password)
                # Convert user to dictionary
                cursor.execute("select Project , plant FROM [DBCoficab].[dbo].[User_Access] where [User] = ?", (email,))
                access = cursor.fetchall()
                # Extracting projects and plants from the access list
                projects = list(set([item[0] for item in access]))
                plants = list(set([item[1] for item in access]))
                user_dict = {
                    "ID_User_Login": user[0],
                    "Position": user[2],
                    "Plant":plants,
                    "Type":user[3],
                    "resetpassword":user[5],
                    "Projects":projects
                }
                access_token = create_access_token(identity=user[0])
                return {"msg": "all good.","user":user_dict,"access_token":str(access_token) , "code":200} 
            else:
                return {"msg": "Incorrect password.", "code": 401}
    except pyodbc.Error as e:
        print(f"An error occurred: {e}")
        return {"msg": "An error occurred while logging in.", "code": 500}
    finally:
        cnxn.close() 
    """ try:
        print(email)
        with cnxn.cursor() as cursor:
            # Check if email exists
            cursor.execute("SELECT * FROM [DBCoficab].[dbo].[User] WHERE ID_User_Login = ?", (email,))
            user = cursor.fetchone()
            if user is None:
                return {"msg": "Email does not exist.", "code": 401}
            
            # Verify password
            hashed_password = user[1].encode('utf-8')  # Ensure hashed_password is bytes
            password_bytes = password.encode('utf-8')  # Ensure password is bytes

            if bcrypt.checkpw(password_bytes, hashed_password):
                # Password matches, return user object (excluding password)
                # Convert user to dictionary
                cursor.execute("select Project , plant FROM [DBCoficab].[dbo].[User_Access] where [User] = ?", (email,))
                access = cursor.fetchall()
                # Extracting projects and plants from the access list
                projects = list(set([item[0] for item in access]))
                plants = list(set([item[1] for item in access]))
                user_dict = {
                    "ID_User_Login": user[0],
                    "Position": user[2],
                    "Plant":plants,
                    "Type":user[3],
                    "Projects":projects
                }
                access_token = create_access_token(identity=user[0])
                return {"msg": "all good.","user":user_dict,"access_token":str(access_token) , "code":200} 
            else:
                return {"msg": "Incorrect password.", "code": 401}
    except pyodbc.Error as e:
        print(f"An error occurred: {e}")
        return {"msg": "An error occurred while logging in.", "code": 500}
    finally:
        cnxn.close()  """
    

def GetUserById(cnxn, ID_User_Login):
    cursor = cnxn.cursor()

    try:
        # SQL query to fetch the user details from the User table
        sqlQueryUser = "SELECT ID_User_Login, Password, Position, Type, Level_ FROM [DBCoficab].[dbo].[User] WHERE ID_User_Login = ?"
        
        # Execute the user query
        cursor.execute(sqlQueryUser, (ID_User_Login,))
        user_result = cursor.fetchone()

        # If the user is found, proceed to fetch the access details
        if user_result:
            user_data = {
                'ID_User_Login': user_result[0],
                'Password': user_result[1],  # Optionally omit this for security reasons
                'Position': user_result[2],
                'Type': user_result[3],
                'Level_': user_result[4],
                'Plants': [],
                'Regions': [],
                'Projects': []
            }

            # SQL query to fetch distinct Plants, Regions, and Projects from the User_Access table
            sqlQueryAccess = """
                SELECT DISTINCT Plant, Region, Project 
                FROM [DBCoficab].[dbo].[User_Access]
                WHERE [User] = ?
            """
            
            # Execute the access query
            cursor.execute(sqlQueryAccess, (ID_User_Login,))
            access_results = cursor.fetchall()

            # Separate Plants, Regions, and Projects into their respective lists
            if access_results:
                plants = set()
                regions = set()
                projects = set()

                for row in access_results:
                    plants.add(row[0])   # Add unique plants
                    regions.add(row[1])  # Add unique regions
                    projects.add(row[2]) # Add unique projects

                # Convert sets to lists and assign to the user_data
                user_data['Plants'] = list(plants)
                user_data['Regions'] = list(regions)

                # Convert projects to a list of dictionaries
                user_data['Projects'] = [{'Description': project} for project in projects]

            return user_data
        else:
            # If no user is found
            return {"msg": f"User with ID_User_Login '{ID_User_Login}' not found.", "code": 404}
    
    finally:
        # Ensure the connection is closed
        cnxn.close()


