""" import pyodbc

# Define connection parameters
server_name = 'localhost'
database_name = 'SSISDB'
job_name = 'agent'

# Connect to SQL Server
conn_str = f'Driver=ODBC Driver 17 for SQL Server;Server={server_name};Database={database_name};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)

# Get the job ID
query = f"SELECT job_id FROM msdb.dbo.sysjobs WHERE name = '{job_name}'"
cursor = conn.cursor()
cursor.execute(query)
job_id_row = cursor.fetchone()

if job_id_row:
    job_id = job_id_row[0]

    # Start the job
    query = f"EXEC msdb.dbo.sp_start_job @job_name = '{job_name}'"
    try:
        cursor.execute(query)
        print("Job started successfully.")
    except pyodbc.Error as e:
        print("Error:", e)
else:
    print("Job not found.")

# Close the connection
conn.close() 


 """