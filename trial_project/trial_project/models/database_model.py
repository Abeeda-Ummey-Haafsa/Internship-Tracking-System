import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
#import datetime
#import os
from typing import Optional, List, Dict, Any
import mysql.connector
from mysql.connector import Error

class DatabaseModel:
    """Handles all database operations and connections"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect_to_database()
        self.create_tables()
    
    def connect_to_database(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='trial_db',
                user='root',
                password='password'
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to MySQL database successfully")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
    
    def create_tables(self):
        """Create all necessary tables"""
        try:
            tables = {
                'users': """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        role ENUM('student', 'faculty', 'admin', 'company') NOT NULL,
                        department VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
                'companies': """
                    CREATE TABLE IF NOT EXISTS companies (
                        company_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        contact_person VARCHAR(100),
                        email VARCHAR(100),
                        phone VARCHAR(20),
                        address TEXT,
                        verified BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
                'quotas': """
                    CREATE TABLE IF NOT EXISTS quotas (
                        quota_id INT AUTO_INCREMENT PRIMARY KEY,
                        company_id INT,
                        department VARCHAR(100),
                        total_slots INT NOT NULL,
                        available_slots INT NOT NULL,
                        deadline DATE,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (company_id) REFERENCES companies(company_id)
                    )
                """,
                'applications': """
                    CREATE TABLE IF NOT EXISTS applications (
                        app_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        company_id INT,
                        quota_id INT,
                        status ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending',
                        application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        report_path VARCHAR(255),
                        self_found BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (student_id) REFERENCES users(user_id),
                        FOREIGN KEY (company_id) REFERENCES companies(company_id),
                        FOREIGN KEY (quota_id) REFERENCES quotas(quota_id)
                    )
                """,
                'reports': """
                    CREATE TABLE IF NOT EXISTS reports (
                        report_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        supervisor_id INT,
                        app_id INT,
                        grade VARCHAR(10),
                        comments TEXT,
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES users(user_id),
                        FOREIGN KEY (supervisor_id) REFERENCES users(user_id),
                        FOREIGN KEY (app_id) REFERENCES applications(app_id)
                    )
                """,
                'feedback': """
                    CREATE TABLE IF NOT EXISTS feedback (
                        feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                        company_id INT,
                        student_id INT,
                        app_id INT,
                        rating INT CHECK (rating >= 1 AND rating <= 5),
                        remarks TEXT,
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (company_id) REFERENCES companies(company_id),
                        FOREIGN KEY (student_id) REFERENCES users(user_id),
                        FOREIGN KEY (app_id) REFERENCES applications(app_id)
                    )
                """,
                'faculty_assignments': """
                    CREATE TABLE IF NOT EXISTS faculty_assignments (
                        assignment_id INT AUTO_INCREMENT PRIMARY KEY,
                        faculty_id INT,
                        student_id INT,
                        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (faculty_id) REFERENCES users(user_id),
                        FOREIGN KEY (student_id) REFERENCES users(user_id)
                    )
                """
            }
            
            for table_name, query in tables.items():
                self.cursor.execute(query)
                self.connection.commit()
            
            print("All tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    # User Management
    def create_user(self, name: str, email: str, password: str, role: str, department: str = None) -> bool:
        """Create a new user"""
        try:
            password_hash = self.hash_password(password)
            query = """
                INSERT INTO users (name, email, password_hash, role, department)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, password_hash, role, department))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        try:
            query = "SELECT * FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            user = self.cursor.fetchone()
            
            if user and self.verify_password(password, user['password_hash']):
                return user
            return None
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error getting user: {e}")
            return None
    
    # Company Management
    def create_company(self, name: str, contact_person: str, email: str, phone: str, address: str) -> bool:
        """Create a new company"""
        try:
            query = """
                INSERT INTO companies (name, contact_person, email, phone, address)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, contact_person, email, phone, address))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating company: {e}")
            return False
    
    def get_all_companies(self) -> List[Dict]:
        """Get all companies"""
        try:
            query = "SELECT * FROM companies ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting companies: {e}")
            return []
    
    # Quota Management
    def create_quota(self, company_id: int, department: str, total_slots: int, deadline: str, description: str) -> bool:
        """Create a new quota"""
        try:
            query = """
                INSERT INTO quotas (company_id, department, total_slots, available_slots, deadline, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (company_id, department, total_slots, total_slots, deadline, description))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating quota: {e}")
            return False
    
    def get_available_quotas(self, department: str = None) -> List[Dict]:
        """Get available quotas"""
        try:
            if department:
                query = """
                    SELECT q.*, c.name as company_name 
                    FROM quotas q 
                    JOIN companies c ON q.company_id = c.company_id 
                    WHERE q.available_slots > 0 AND q.department = %s AND q.deadline >= CURDATE()
                    ORDER BY q.deadline
                """
                self.cursor.execute(query, (department,))
            else:
                query = """
                    SELECT q.*, c.name as company_name 
                    FROM quotas q 
                    JOIN companies c ON q.company_id = c.company_id 
                    WHERE q.available_slots > 0 AND q.deadline >= CURDATE()
                    ORDER BY q.deadline
                """
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting quotas: {e}")
            return []
    
    # Application Management
    def create_application(self, student_id: int, company_id: int, quota_id: int = None, self_found: bool = False) -> bool:
        """Create a new application"""
        try:
            query = """
                INSERT INTO applications (student_id, company_id, quota_id, self_found)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (student_id, company_id, quota_id, self_found))
            
            # Update available slots if quota-based
            if quota_id and not self_found:
                update_query = "UPDATE quotas SET available_slots = available_slots - 1 WHERE quota_id = %s"
                self.cursor.execute(update_query, (quota_id,))
            
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating application: {e}")
            return False
    
    def get_applications_by_student(self, student_id: int) -> List[Dict]:
        """Get applications by student"""
        try:
            query = """
                SELECT a.*, c.name as company_name, q.department
                FROM applications a
                JOIN companies c ON a.company_id = c.company_id
                LEFT JOIN quotas q ON a.quota_id = q.quota_id
                WHERE a.student_id = %s
                ORDER BY a.application_date DESC
            """
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting applications: {e}")
            return []
    
    def get_pending_applications(self) -> List[Dict]:
        """Get all pending applications for admin review"""
        try:
            query = """
                SELECT a.*, u.name as student_name, u.email as student_email, 
                       c.name as company_name, q.department
                FROM applications a
                JOIN users u ON a.student_id = u.user_id
                JOIN companies c ON a.company_id = c.company_id
                LEFT JOIN quotas q ON a.quota_id = q.quota_id
                WHERE a.status = 'pending'
                ORDER BY a.application_date
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting pending applications: {e}")
            return []
    
    def update_application_status(self, app_id: int, status: str) -> bool:
        """Update application status"""
        try:
            query = "UPDATE applications SET status = %s WHERE app_id = %s"
            self.cursor.execute(query, (status, app_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating application status: {e}")
            return False
    
    # Faculty Assignment
    def assign_faculty(self, faculty_id: int, student_id: int) -> bool:
        """Assign faculty to student"""
        try:
            query = """
                INSERT INTO faculty_assignments (faculty_id, student_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE faculty_id = %s
            """
            self.cursor.execute(query, (faculty_id, student_id, faculty_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error assigning faculty: {e}")
            return False
    
    def get_faculty_users(self) -> List[Dict]:
        """Get all faculty users"""
        try:
            query = "SELECT * FROM users WHERE role = 'faculty' ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting faculty: {e}")
            return []
    
    def get_student_users(self) -> List[Dict]:
        """Get all student users"""
        try:
            query = "SELECT * FROM users WHERE role = 'student' ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting students: {e}")
            return []
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()