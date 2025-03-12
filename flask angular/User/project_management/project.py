from flask import jsonify
import pyodbc


def selectTable(cnxn):
    try:
        sqlQuery = "SELECT * FROM [DBCoficab].[dbo].[Project]"
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        projects_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        return projects_list
    finally:
        cnxn.close()


def AddProject(cnxn, Code_Project, Description):
    try:
        cursor = cnxn.cursor()

        # Check if project already exists
        check_query = "SELECT COUNT(*) FROM [DBCoficab].[dbo].[Project] WHERE Code_Project = ?"
        cursor.execute(check_query, (Code_Project,))
        project_count = cursor.fetchone()[0]

        if project_count > 0:
            return {"msg": f"Project with Code_Project '{Code_Project}' already exists.", "code": 400}

        # If project doesn't exist, proceed with insertion
        sqlQuery = "INSERT INTO [DBCoficab].[dbo].[Project] (Code_Project, Description) VALUES (?, ?)"
        cursor.execute(sqlQuery, (Code_Project, Description))
        cnxn.commit()
        return {"msg": "The Project has been added successfully.", "code": 200}
    finally:
        cnxn.close()



def EditProject(cnxn, Code_Project, Description):
    try:
        cursor = cnxn.cursor()
        sqlQuery = """
            UPDATE [DBCoficab].[dbo].[Project]
            SET Description=?
            WHERE Code_Project=?
        """
        cursor.execute(sqlQuery, (Description, Code_Project))
        cnxn.commit()

        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Project has been edited successfully.", "code": 200}
        else:
            return {"msg": f"No project found with Code_Project '{Code_Project}'", "code": 404}
    finally:
        cnxn.close()


def DeleteProject(cnxn, Code_Project):
    try:
        cursor = cnxn.cursor()
        sqlQuery = "DELETE FROM [DBCoficab].[dbo].[Project] WHERE Code_Project=?"
        cursor.execute(sqlQuery, (Code_Project,))
        cnxn.commit()

        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Project has been deleted successfully.", "code": 200}
        else:
            return {"msg": f"No project found with Code_Project '{Code_Project}'", "code": 404}
    finally:
        cnxn.close()
