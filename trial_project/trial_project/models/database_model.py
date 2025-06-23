import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
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
                'department': """
                    CREATE TABLE IF NOT EXISTS department (
                        department_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
                'students': """
                    CREATE TABLE IF NOT EXISTS students (
                        student_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        cgpa DECIMAL(3,2) CHECK (cgpa >= 2.00 AND cgpa <= 4.00),
                        department_id INT,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (department_id) REFERENCES department(department_id)
                    )
                """,
                'faculties': """
                    CREATE TABLE IF NOT EXISTS faculties (
                        faculty_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        department_id INT,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (department_id) REFERENCES department(department_id)
                    )
                """,
                'secretaries': """
                    CREATE TABLE IF NOT EXISTS secretaries (
                        secretary_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        faculty_id INT,
                        department_id INT,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id),
                        FOREIGN KEY (department_id) REFERENCES department(department_id)
                    )
                """,
                'admins': """
                    CREATE TABLE IF NOT EXISTS admins (
                        admin_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
                'companies': """
                    CREATE TABLE IF NOT EXISTS companies (
                        company_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        contact_person VARCHAR(100),
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        phone VARCHAR(20),
                        address TEXT,
                        registered BOOLEAN DEFAULT TRUE,
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
                        FOREIGN KEY (student_id) REFERENCES students(student_id),
                        FOREIGN KEY (company_id) REFERENCES companies(company_id),
                        FOREIGN KEY (quota_id) REFERENCES quotas(quota_id)
                    )
                """,
                'reports': """
                    CREATE TABLE IF NOT EXISTS reports (
                        report_id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        faculty_id INT,
                        app_id INT,
                        grade VARCHAR(10),
                        comments TEXT,
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(student_id),
                        FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id),
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
                        FOREIGN KEY (student_id) REFERENCES students(student_id),
                        FOREIGN KEY (app_id) REFERENCES applications(app_id)
                    )
                """,
                'faculty_assignments': """
                    CREATE TABLE IF NOT EXISTS faculty_assignments (
                        assignment_id INT AUTO_INCREMENT PRIMARY KEY,
                        faculty_id INT,
                        student_id INT,
                        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id),
                        FOREIGN KEY (student_id) REFERENCES students(student_id)
                    )
                """
            }
            
            for table_name, query in tables.items():
                self.cursor.execute(query)
                self.connection.commit()
            
            # Insert default departments if they don't exist
            self.insert_default_departments()
            
            print("All tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def insert_default_departments(self):
        """Insert default departments"""
        try:
            departments = ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 
                          'Civil Engineering', 'Business Administration']
            
            for dept in departments:
                query = "INSERT IGNORE INTO department (name) VALUES (%s)"
                self.cursor.execute(query, (dept,))
            
            self.connection.commit()
        except Error as e:
            print(f"Error inserting departments: {e}")
    
    def get_department_id(self, department_name: str) -> Optional[int]:
        """Get department ID by name"""
        try:
            query = "SELECT department_id FROM department WHERE name = %s"
            self.cursor.execute(query, (department_name,))
            result = self.cursor.fetchone()
            return result['department_id'] if result else None
        except Error as e:
            print(f"Error getting department ID: {e}")
            return None
    
    def get_all_departments(self) -> List[Dict]:
        """Get all departments"""
        try:
            query = "SELECT * FROM department ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting departments: {e}")
            return []
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    # User Management based on roles
    def create_user_by_role(self, role: str, **kwargs) -> bool:
        """Create user based on role"""
        try:
            password_hash = self.hash_password(kwargs['password'])
            
            if role.lower() == 'student':
                return self.create_student(
                    name=kwargs['full_name'],
                    email=kwargs['email'],
                    password_hash=password_hash,
                    department=kwargs['department'],
                    cgpa=float(kwargs['cgpa'])
                )
            elif role.lower() == 'faculty':
                return self.create_faculty(
                    name=kwargs['full_name'],
                    email=kwargs['email'],
                    password_hash=password_hash,
                    department=kwargs['department']
                )
            elif role.lower() == 'secretary':
                return self.create_secretary(
                    name=kwargs['full_name'],
                    email=kwargs['email'],
                    password_hash=password_hash,
                    department=kwargs['department'],
                    faculty_id=kwargs.get('faculty_id')
                )
            elif role.lower() == 'company':
                return self.create_company_user(
                    name=kwargs['full_name'],
                    email=kwargs['email'],
                    password_hash=password_hash
                )
            elif role.lower() == 'admin':
                return self.create_admin(
                    name=kwargs['full_name'],
                    email=kwargs['email'],
                    password_hash=password_hash
                )
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def create_student(self, name: str, email: str, password_hash: str, department: str, cgpa: float) -> bool:
        """Create a new student"""
        try:
            dept_id = self.get_department_id(department)
            if not dept_id:
                return False
            
            query = """
                INSERT INTO students (name, email, password_hash, department_id, cgpa)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, password_hash, dept_id, cgpa))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating student: {e}")
            return False
    
    def create_faculty(self, name: str, email: str, password_hash: str, department: str) -> bool:
        """Create a new faculty"""
        try:
            dept_id = self.get_department_id(department)
            if not dept_id:
                return False
            
            query = """
                INSERT INTO faculties (name, email, password_hash, department_id)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, password_hash, dept_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating faculty: {e}")
            return False
    
    def create_secretary(self, name: str, email: str, password_hash: str, department: str, faculty_id: int = None) -> bool:
        """Create a new secretary"""
        try:
            dept_id = self.get_department_id(department)
            if not dept_id:
                return False
            
            query = """
                INSERT INTO secretaries (name, email, password_hash, department_id, faculty_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, password_hash, dept_id, faculty_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating secretary: {e}")
            return False
    
    def create_company_user(self, name: str, email: str, password_hash: str) -> bool:
        """Create a new company user"""
        try:
            query = """
                INSERT INTO companies (name, email, password_hash, contact_person)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, password_hash, name))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating company: {e}")
            return False
    
    def create_admin(self, name: str, email: str, password_hash: str) -> bool:
        """Create a new admin"""
        try:
            query = """
                INSERT INTO admins (name, email, password_hash)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (name, email, password_hash))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating admin: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str, role: str) -> Optional[Dict]:
        """Authenticate user login based on role"""
        try:
            table_map = {
                'student': 'students',
                'faculty': 'faculties', 
                'secretary': 'secretaries',
                'company': 'companies',
                'admin': 'admins'
            }
            
            table = table_map.get(role.lower())
            if not table:
                return None
            
            # Get ID field name based on table
            id_field = f"{role.lower()}_id"
            
            query = f"SELECT * FROM {table} WHERE email = %s"
            self.cursor.execute(query, (email,))
            user = self.cursor.fetchone()
            
            if user and self.verify_password(password, user['password_hash']):
                user['role'] = role.lower()
                user['user_id'] = user[id_field]  # Standardize user_id field
                return user
            return None
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_id_and_role(self, user_id: int, role: str) -> Optional[Dict]:
        """Get user by ID and role"""
        try:
            table_map = {
                'student': 'students',
                'faculty': 'faculties',
                'secretary': 'secretaries', 
                'company': 'companies',
                'admin': 'admins'
            }
            
            table = table_map.get(role.lower())
            if not table:
                return None
            
            id_field = f"{role.lower()}_id"
            query = f"SELECT * FROM {table} WHERE {id_field} = %s"
            self.cursor.execute(query, (user_id,))
            user = self.cursor.fetchone()
            
            if user:
                user['role'] = role.lower()
                user['user_id'] = user[id_field]
            
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            return None
    
    # Company Management
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
                SELECT a.*, s.name as student_name, s.email as student_email, 
                       c.name as company_name, q.department
                FROM applications a
                JOIN students s ON a.student_id = s.student_id
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
            query = "SELECT * FROM faculties ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting faculty: {e}")
            return []
    
    def get_student_users(self) -> List[Dict]:
        """Get all student users"""
        try:
            query = "SELECT * FROM students ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting students: {e}")
            return []
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()