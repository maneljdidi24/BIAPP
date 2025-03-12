import pyodbc
import bcrypt

def selectTopicTable(cnxn):
    try: 
        sqlQuery = "SELECT [ID_Topic], [Name_T], Materials_topics_GRH FROM [Sustainability].[dbo].[Topic]"
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        topics_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        return topics_list
    finally:
        cnxn.close()

def addTopic(cnxn, ID_Topic, Name_T, Materials_topics_GRH):
    cursor = cnxn.cursor()

    # Check if topic already exists
    check_query = "SELECT COUNT(*) FROM [Sustainability].[dbo].[Topic] WHERE ID_Topic = ?"
    cursor.execute(check_query, (ID_Topic,))
    topic_count = cursor.fetchone()[0]
    if topic_count > 0:
        return {"msg": f"Topic with ID_Topic '{ID_Topic}' already exists.", "code": 400}

    # If topic doesn't exist, proceed with insertion
    sqlQuery = "INSERT INTO [Sustainability].[dbo].[Topic] (ID_Topic, Name_T, [Materials topics-GRH]) VALUES (?, ?, ?)"
    try:
        cursor.execute(sqlQuery, (ID_Topic, Name_T, Materials_topics_GRH))
        cnxn.commit()
        return {"msg": "The Topic has been added successfully.", "code": 200}
    finally:
        cnxn.close()

def modifyTopic(cnxn, ID_Topic, Name_T, Materials_topics_GRH):
    cursor = cnxn.cursor()
    sqlQuery = """
        UPDATE [Sustainability].[dbo].[Topic]
        SET Name_T=?, [Materials topics-GRH]=?
        WHERE ID_Topic=?
    """
    try:
        cursor.execute(sqlQuery, (Name_T, Materials_topics_GRH, ID_Topic))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Topic has been edited successfully.", "code": 200}
        else:
            return {"msg": f"No Topic found with ID_Topic '{ID_Topic}'", "code": 404}
    finally:
        cnxn.close()
