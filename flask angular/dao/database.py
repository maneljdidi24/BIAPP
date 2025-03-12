from sqlalchemy import create_engine ,inspect
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
import pyodbc
from urllib.parse import quote_plus
import os
import subprocess


try:
        # Retrieve the secret from Docker secrets or environment variable
    with open('/run/secrets/flask_secret', 'r') as secret_file:
        secret = secret_file.read().strip()
        encoded_password = quote_plus(secret)
except FileNotFoundError:
    secret = os.getenv('DBSourceAzure_PWD', 'DataBase')
    encoded_password = quote_plus(secret)


# Database URL
DATABASE_URL = (f"mssql+pyodbc://userWeb:{encoded_password}@192.168.122.40"
               f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes")

# Create engine
""" engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) """

def init_db(database_name: str):
    """
    Initialize the database connection dynamically using the provided database name.
    """
    global SessionLocal
    database_url = f"{DATABASE_URL}&database={database_name}"  # Add the database name dynamically
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

# Dependency to get a session for each request
def get_db():
    db = SessionLocal()  # Open the connection when a request comes in
    try:
        yield db  # Return the session to be used in the route
    finally:
        db.close()  # Close the connection when done with the request
