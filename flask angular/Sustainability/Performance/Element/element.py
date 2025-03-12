import pyodbc
import bcrypt

def selectElementTable(cnxn):
    try: 
        sqlQuery = """select [Sustainability].[dbo].[Element].[ID_Element],[Sustainability].[dbo].[Element].[Name_Element] ,
        [Sustainability].[dbo].[Element].[Unit] ,[Sustainability].[dbo].[Topic].[ID_Topic] ,
[Sustainability].[dbo].[Famille].Name_Famille
from [Sustainability].[dbo].[Topic] inner join [Sustainability].[dbo].[Famille] on [Sustainability].[dbo].[Topic].[ID_Topic] = [Sustainability].[dbo].[Famille].[ID_T]
inner join [Sustainability].[dbo].[Element] on [Sustainability].[dbo].[Famille].[ID_Famille] =  [Sustainability].[dbo].[Element].[ID_F]"""
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        elements_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        return elements_list
    finally:
        cnxn.close()

def addElement(cnxn, ID_Element, Name_Element, Unit, ID_T):
    cursor = cnxn.cursor()

    # Check if element already exists
    check_query = "SELECT COUNT(*) FROM [Sustainability].[dbo].[Element] WHERE ID_Element = ?"
    cursor.execute(check_query, (ID_Element,))
    element_count = cursor.fetchone()[0]
    if element_count > 0:
        return {"msg": f"Element with ID_Element '{ID_Element}' already exists.", "code": 400}

    # If element doesn't exist, proceed with insertion
    sqlQuery = "INSERT INTO [Sustainability].[dbo].[Element] (ID_Element, Name_Element, Unit, ID_T) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(sqlQuery, (ID_Element, Name_Element, Unit, ID_T))
        cnxn.commit()
        return {"msg": "The Element has been added successfully.", "code": 200}
    finally:
        cnxn.close()

def modifyElement(cnxn, ID_Element, Name_Element, Unit, ID_T):
    cursor = cnxn.cursor()
    sqlQuery = """
        UPDATE [Sustainability].[dbo].[Element]
        SET Name_Element=?, Unit=?, ID_T=?
        WHERE ID_Element=?
    """
    try:
        cursor.execute(sqlQuery, (Name_Element, Unit, ID_T, ID_Element))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Element has been edited successfully.", "code": 200}
        else:
            return {"msg": f"No Element found with ID_Element '{ID_Element}'", "code": 404}
    finally:
        cnxn.close()

def deleteElement(cnxn, ID_Element):
    cursor = cnxn.cursor()
    sqlQuery = "DELETE FROM [Sustainability].[dbo].[Element] WHERE ID_Element = ?"
    try:
        cursor.execute(sqlQuery, (ID_Element,))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Element has been deleted successfully.", "code": 200}
        else:
            return {"msg": f"No Element found with ID_Element '{ID_Element}'", "code": 404}
    finally:
        cnxn.close()
