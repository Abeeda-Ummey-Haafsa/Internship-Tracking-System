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
        
        print("Database created successfully")
        
        
        model = DatabaseModel()
        
        
        admin_created = model.create_user(
            name="System Administrator",
            email="admin@system.com",
            password="admin123",
            role="admin",
            department="Administration"
        )
        
        if admin_created:
            print("Default admin user created:")
            print("Email: admin@system.com")
            print("Password: admin123")
        
        
        model.create_company(
            name="Tech Corp",
            contact_person="John Doe",
            email="john@techcorp.com",
            phone="+1234567890",
            address="123 Tech Street, Tech City"
        )
        
        
        model.create_quota(
            company_id=1,
            department="Computer Science",
            total_slots=5,
            deadline="2025-12-31",
            description="Software Development Internship"
        )
        
        print("Sample data created successfully")
        
        model.close_connection()
        connection.close()
        
    except Error as e:
        print(f"Database setup error: {e}")