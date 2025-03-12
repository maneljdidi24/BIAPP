import json


def displayEmployee(cnxn):
    try:
        
        sqlQuery = f"""SELECT [name_E],JOB.job_description,[Plant] , Department.Nom_Department
      ,[Local_Position]
      ,[HC_Type]
      ,[Scope]
      ,[Cost_Center]
      ,[Hiring_Date]
      ,[Termination_Date]
      ,[Termination_Reason]
      ,[Profil]
 FROM [HR].[dbo].Employer inner join [HR].[dbo].JOB on [HR].[dbo].Employer.ID_job = [HR].[dbo].JOB.Id_job 
 inner join [HR].[dbo].Department on [HR].[dbo].Department.ID_Department = [HR].[dbo].Employer.ID_Department  """
        
        cursor = cnxn.cursor()
        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        results = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]

        return json.dumps(results, default=str)

    finally:
        cnxn.close()  # Close the connection