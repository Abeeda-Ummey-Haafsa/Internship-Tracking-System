import mysql.connector
from mysql.connector import Error

from trial_project.models.database_model import DatabaseModel

def setup_database():
    """Setup database and create initial admin user"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )
        cursor = connection.cursor()
        
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS internship_system")
        cursor.execute("USE internship_system")
        
        #print("Database created successfully")

    except Error as e:
        print(f"Database setup error: {e}")
       