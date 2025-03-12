import pyodbc
import bcrypt

def getdistinctdate(cnxn,data):
    try:
        cnxn.execute("SET LANGUAGE 'English';")

        selected_months = data["months"]
        selected_years = data["years"]
        selected_plants = data["plant"]  # Example plant patterns

        # Month name to number mapping
        month_name_to_number = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }

        # Convert month names to numbers
        selected_month_numbers = [month_name_to_number[month] for month in selected_months]

        # Construct the WHERE clause for months, years, and plants
        months_condition = " OR ".join([f"MONTH([Sustainability].[dbo].[Performance].[Date_Per]) = {month}" for month in selected_month_numbers])
        years_condition = " OR ".join([f"YEAR([Sustainability].[dbo].[Performance].[Date_Per]) = {year}" for year in selected_years])
        plants_condition = " OR ".join([f"[Sustainability].[dbo].[Target].[ID_P] LIKE '{plant}'" for plant in selected_plants])

        # Combine the conditions into the final WHERE clause
        where_clause = f"({months_condition}) AND ({years_condition}) AND ({plants_condition})"

        # Complete SQL query
        sqlQuery = f"""
        SELECT DISTINCT 
            FORMAT([Sustainability].[dbo].[Performance].[Date_Per], 'MMMM yyyy') AS [Date],
            MONTH([Sustainability].[dbo].[Performance].[Date_Per])
        FROM [Sustainability].[dbo].[Performance]
        INNER JOIN [Sustainability].[dbo].[Element] ON [Sustainability].[dbo].[Element].[ID_Element] = [Sustainability].[dbo].[Performance].[ID_E]
        INNER JOIN [Sustainability].[dbo].[Famille] ON [Sustainability].[dbo].[Element].[ID_F] = [Sustainability].[dbo].[Famille].ID_Famille
        INNER JOIN [Sustainability].[dbo].[Topic] ON [Sustainability].[dbo].[Topic].ID_Topic = [Sustainability].[dbo].[Famille].[ID_T]
        INNER JOIN [Sustainability].[dbo].[Target] ON [Sustainability].[dbo].[Performance].ID_Target = [Sustainability].[dbo].[Target].ID_Target
        WHERE {where_clause}
        ORDER BY MONTH([Sustainability].[dbo].[Performance].[Date_Per])
        """
      
        cursor = cnxn.cursor()
    
        # Execute the query and fetch all rows
        rows = cursor.execute(sqlQuery).fetchall()
       
        columns = [column[0] for column in cursor.description]
        # Convert each row to a dictionary
        elements_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
       
        return elements_list
    finally:
        cnxn.close()

    """    SELECT
                    [dbo].[Performance] .[Date_Per] 
                    ,[dbo].[Performance] .[Qty] ,[dbo].[Element].[Name_Element] ,[dbo].[Topic].ID_Topic  
                    FROM [dbo].[Performance] inner join [dbo].[Element] on [dbo].[Element].[ID_Element] = [dbo].[Performance].[ID_E]   
                     inner join [dbo].[Topic] on [dbo].[Topic].ID_Topic = [dbo].[Element].[ID_T] where [dbo].[Performance] .[Date_Per] > '2024-12-01' """


def selectPerformanceTable(cnxn,data):
    try:
        # Set the language to English
        try:
            cnxn.execute("SET LANGUAGE 'English';")
        except Exception as e:
            return {"msg": f"Error setting language: {e}", "code": 500}

        selected_months = data["months"]
        selected_years = data["years"]
        selected_plants = data["plant"] 

        # Convert months to their corresponding numeric values
        try:
            month_numbers = [str(i + 1) for i, month in enumerate(
                ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            ) if month in selected_months]
            month_numbers_str = ', '.join(month_numbers)
        except Exception as e:
            return {"msg": f"Error processing selected months: {e}", "code": 500}
        
        # Convert years to strings
        try:
            years_str = ', '.join(map(str, selected_years))
        except Exception as e:
            return {"msg": f"Error processing selected years: {e}", "code": 500}
        
        try:
            sqlQuery = f"""
        DECLARE @cols AS NVARCHAR(MAX),
        @query AS NVARCHAR(MAX),
        @plantPattern AS NVARCHAR(MAX),
        @selectedMonths AS NVARCHAR(MAX),
        @selectedYears AS NVARCHAR(MAX);
 
-- Set the dynamic values for plant patterns and date conditions
SET @plantPattern = '{selected_plants}'; -- Example plant pattern
SET @selectedMonths = '{month_numbers_str}'; -- Example selected months (January and February)
SET @selectedYears = '{years_str}'; -- Example selected years
 
-- Generate the column list for the pivot statement
SET @cols = STUFF(
					(
					SELECT DISTINCT ',' + QUOTENAME(FORMAT([Date_Per], 'MMMM yyyy'))
		
                   FROM [Sustainability].[dbo].[Performance] left JOIN [Sustainability].[dbo].[Target] ON [Sustainability].[dbo].[Performance].ID_Target = [Sustainability].[dbo].[Target].ID_Target 
                   WHERE (MONTH([Date_Per])
				   IN (SELECT value FROM STRING_SPLIT(@selectedMonths, ','))

                          AND YEAR([Date_Per]) 
						  IN (SELECT value FROM STRING_SPLIT(@selectedYears, ','))
                         AND [Sustainability].[dbo].[Target].[ID_P] LIKE @plantPattern)
                   FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')

				  

-- Construct the dynamic SQL query
SET @query = 'SELECT [ID_Topic], [Name_Element], [Unit], ' + @cols + '
              FROM (
                  SELECT t.[ID_Topic], e.[Name_Element], e.[Unit], FORMAT(p.[Date_Per], ''MMMM yyyy'') AS [Date], p.[Qty]
                  FROM [Sustainability].[dbo].[Topic] t
                  INNER JOIN [Sustainability].[dbo].[Famille] f ON t.[ID_Topic] = f.[ID_T]
                  LEFT JOIN [Sustainability].[dbo].[Element] e ON f.[ID_Famille] = e.[ID_F]
                  LEFT JOIN [Sustainability].[dbo].[Performance] p ON e.[ID_Element] = p.[ID_E]
				  LEFT JOIN [Sustainability].[dbo].[Target] ON p.ID_Target = [Sustainability].[dbo].[Target].ID_Target
                  WHERE (MONTH(p.[Date_Per]) IN (SELECT value FROM STRING_SPLIT(''' + @selectedMonths + ''', '',''))
                         AND YEAR(p.[Date_Per]) IN (SELECT value FROM STRING_SPLIT(''' + @selectedYears + ''', '','')))
                        AND [Sustainability].[dbo].[Target].[ID_P] LIKE ''' + @plantPattern + '''
              ) src
              PIVOT (
                  SUM([Qty])
                  FOR [Date] IN (' + @cols + ')
              ) pvt'

-- Execute the dynamic SQL query
EXECUTE(@query);

        """

        except Exception as e:
            return {"msg": f"Error constructing SQL query: {e}", "code": 500}
        
        # Execute the SQL query and fetch results
        try:
            cursor = cnxn.cursor()
            rows = cursor.execute(sqlQuery).fetchall()
            columns = [column[0] for column in cursor.description]
        except Exception as e:
            return {"msg": f"Error executing SQL query: {e}", "code": 500}
     
        # Convert the rows into a list of dictionaries
        try:
            performance_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        except Exception as e:
            return {"msg": f"Error processing SQL result: {e}", "code": 500}

        return performance_list
    
    except Exception as e:
        return {"msg": f"An unexpected error occurred: {e}", "code": 500}

    finally:
        cnxn.close()

def addPerformance(cnxn, ID_E, Date_Per, Qty):
    cursor = cnxn.cursor()

    # Check if performance record already exists
    check_query = "SELECT COUNT(*) FROM [Sustainability].[dbo].[Performance] WHERE ID_E = ? AND Date_Per = ?"
    cursor.execute(check_query, (ID_E, Date_Per))
    performance_count = cursor.fetchone()[0]
    if performance_count > 0:
        return {"msg": f"Performance record with ID_E '{ID_E}' and Date_Per '{Date_Per}' already exists.", "code": 400}

    # If performance record doesn't exist, proceed with insertion
    sqlQuery = "INSERT INTO [Sustainability].[dbo].[Performance] (ID_E, Date_Per, Qty) VALUES (?, ?, ?)"
    try:
        cursor.execute(sqlQuery, (ID_E, Date_Per, Qty))
        cnxn.commit()
        return {"msg": "The Performance record has been added successfully.", "code": 200}
    finally:
        cnxn.close()



""" 

def modifyPerformance(cnxn, performance):
    cursor = cnxn.cursor()
    
    # SQL query for updating the performance record
    updateQuery = 
        UPDATE [Sustainability].[dbo].[Performance]
        SET Qty = ?
        WHERE ID_E = ? AND Date_Per = ? AND ID_Target like ?
    
    
    # SQL query for inserting a new performance record
    insertQuery =
        INSERT INTO [Sustainability].[dbo].[Performance] (Qty, ID_E, Date_Per, ID_Target)
        VALUES (?, ?, ?, ?)
   
    
    try:
        for entry in performance:
            data = entry["data"]
            ID = entry["ID"]
            date = entry["date"]
            target = entry["plant"]
            
            # Try updating the record first
            print(updateQuery, data, ID, date, target)
            cursor.execute(updateQuery, (data, ID, date, target))
            
            # Check if any rows were updated
            if cursor.rowcount == 0:
                # If no records were updated, insert a new one
                print(f"No records updated. Inserting new performance record for ID: {ID}, Date: {date}, Target: {target}.")
                cursor.execute(insertQuery, (data, ID, date, target))
        
        cnxn.commit()
        print(cursor.rowcount)
        
        # Return success message
        if cursor.rowcount > 0:
            return {"msg": "The Performance record has been modified/created successfully.", "code": 200}
        else:
            return {"msg": "No Performance records were updated or created.", "code": 404}
    
    except Exception as e:
        cnxn.rollback()  # Rollback the transaction on error
        return {"msg": f"An error occurred: {e}", "code": 500}
    
    finally:
        cursor.close()  # Ensure cursor is closed properly

 """


def deleteInsertPerformance(cnxn, performance):
    cursor = cnxn.cursor()

    # SQL query to delete specific records based on ID_E, ID_Target, and Date_Per
    deleteQuery = """
        DELETE FROM [Sustainability].[dbo].[Performance]
        WHERE ID_E = ? AND ID_Target like ? AND Date_Per = ?
    """
    
    # SQL query to insert either data or description into the appropriate column
    insertQueryWithData = """
        INSERT INTO [Sustainability].[dbo].[Performance] (Qty, ID_E, Date_Per, ID_Target)
        VALUES (?, ?, ?, ?)
    """
    insertQueryWithDescription = """
        INSERT INTO [Sustainability].[dbo].[Performance] (description, ID_E, Date_Per, ID_Target)
        VALUES (?, ?, ?, ?)
    """

    try:
        for entry in performance:
            # Extract the common fields
            ID = entry["ID"]
            date = entry["date"]
            target = entry["target"]

            # Delete the existing record
            cursor.execute(deleteQuery, (ID, target, date))

            # Insert based on whether 'data' or 'description' is provided
            if "data" in entry:
                data = entry["data"]
                cursor.execute(insertQueryWithData, (data, ID, date, target))
            elif "description" in entry:
                description = entry["description"]
                cursor.execute(insertQueryWithDescription, (description, ID, date, target))

        # Commit the changes (both delete and insert operations)
        cnxn.commit()

        return {"msg": "The Performance records have been successfully modified.", "code": 200}

    except Exception as e:
        cnxn.rollback()  # Rollback the transaction on error
        return {"msg": f"An error occurred: {e}", "code": 500}

    finally:
        cursor.close()  # Ensure cursor is closed properly


def InsertdescriptionPerformance(cnxn, performance):
    cursor = cnxn.cursor()
    
    # SQL query to delete specific records based on ID_E, ID_Target, and Date_Per
    deleteQuery = """
        DELETE FROM [Sustainability].[dbo].[Performance]
        WHERE ID_E = ? AND ID_Target like ? AND Date_Per = ?
    """
    
    # SQL query to insert new performance records
    insertQuery = """
        INSERT INTO [Sustainability].[dbo].[Performance] (Description, ID_E, Date_Per, ID_Target)
        VALUES (?, ?, ?, ?)
    """
    
    try:
        for entry in performance:
            data = entry["data"]
            ID = entry["ID"]
            date = entry["date"]
            target = entry["target"]

            # Delete the record matching the specific ID, target, and date
            cursor.execute(deleteQuery, (ID, target, date))

            # Insert the new record
            cursor.execute(insertQuery, (data, ID, date, target))
        
        # Commit the changes (both delete and insert operations)
        cnxn.commit()
        
        return {"msg": "The Performance records have been successfully modified.", "code": 200}
    
    except Exception as e:
        cnxn.rollback()  # Rollback the transaction on error
        return {"msg": f"An error occurred: {e}", "code": 500}
    
    finally:
        cursor.close()  # Ensure cursor is closed properly        

def deletePerformance(cnxn, ID_E, Date_Per):
    cursor = cnxn.cursor()
    sqlQuery = "DELETE FROM [Sustainability].[dbo].[Performance] WHERE ID_E = ? AND Date_Per = ?"
    try:
        cursor.execute(sqlQuery, (ID_E, Date_Per))
        cnxn.commit()
        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"msg": "The Performance record has been deleted successfully.", "code": 200}
        else:
            return {"msg": f"No Performance record found with ID_E '{ID_E}' and Date_Per '{Date_Per}'", "code": 404}
    finally:
        cnxn.close()

def getdistinctyears(cnxn):
    cursor = cnxn.cursor()
    sqlQuery = "SELECT DISTINCT YEAR([Date_Per]) AS Year FROM [Sustainability].[dbo].[Performance];"
    try:
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]
        # Convert each row to a dictionary
        performance_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows] 
        return performance_list
        
    finally:
        cnxn.close()

def fromPlantGetDate(cnxn,plant):
    cursor = cnxn.cursor()
    sqlQuery = f"""
        select distinct month(Date_Per) as month, YEAR(Date_Per) as year from [Sustainability].[dbo].[Performance] where ID_Target like ?
        """
    print(sqlQuery,plant)
    try:
        rows = cursor.execute(sqlQuery,(plant)).fetchall()
        columns = [column[0] for column in cursor.description]
        # Convert each row to a dictionary
        month_year = [{columns[i]: row[i] for i in range(len(columns))} for row in rows] 
        print(month_year)
        return month_year
        
    finally:
        cnxn.close()


        


def display_performance_for_update(cnxn, date , id):
    try:
        cursor = cnxn.cursor()
        # Prepare the SQL query with parameterized inputs
        sqlQuery = f"""
        SELECT [ID_E], [Date_Per], CAST([Qty] AS DECIMAL(10, 3)) AS Qty, [ID_Target], [Description]
        FROM [Sustainability].[dbo].[Performance]
        WHERE  [Date_Per] = ? and ID_Target LIKE ? 
        """
        
        cursor.execute(sqlQuery, (date, id))


        # Fetch all rows and convert to a list of dictionaries
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        performance_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows] 
        return performance_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"msg": f"An error occurred: {e}", "code": 500}

    finally:
        # Ensure the cursor is closed properly
        if cursor:
            cursor.close()
