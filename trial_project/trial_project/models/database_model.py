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
                        registered BOOLEAN DEFAULT FALSE,
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
                return self.create_company(
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
    
    def create_company(self, name: str, email: str, password_hash: str) -> bool:
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
                user['user_id'] = user[id_field] 
                return user
            return None
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
    
    # Admin Management
    
    def get_all_faculty_with_department(self):
        query = """
            SELECT f.faculty_id, f.name, f.email, f.created_at, d.name AS department
            FROM faculties f
            LEFT JOIN department d ON f.department_id = d.department_id
            ORDER BY f.name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_total_students_for_faculty(self, faculty_id):
        query = """
            SELECT COUNT(*) AS total
            FROM faculty_assignments
            WHERE faculty_id = %s
        """
        self.cursor.execute(query, (faculty_id,))
        result = self.cursor.fetchone()
        return result["total"] if result else 0
    def get_faculties_by_department(self, department_id):
        query = """
            SELECT f.faculty_id, f.name, f.email, d.name AS department, f.created_at
            FROM faculties f
            JOIN department d ON f.department_id = d.department_id
            WHERE f.department_id = %s
        """
        self.cursor.execute(query, (department_id,))
        return self.cursor.fetchall()
    def get_all_departments(self):
        self.cursor.execute("SELECT department_id, name FROM department ORDER BY name")
        return self.cursor.fetchall()
    def delete_faculty_by_id(self, faculty_id):
        try:
            # Remove dependencies first
            self.cursor.execute("DELETE FROM faculty_assignments WHERE faculty_id = %s", (faculty_id,))
            self.cursor.execute("DELETE FROM secretaries WHERE faculty_id = %s", (faculty_id,))
            self.cursor.execute("DELETE FROM reports WHERE faculty_id = %s", (faculty_id,))

            # Delete from faculties
            self.cursor.execute("DELETE FROM faculties WHERE faculty_id = %s", (faculty_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
    def set_faculty_verified(self, faculty_id):
        try:
            self.cursor.execute("UPDATE faculties SET verified = TRUE WHERE faculty_id = %s", (faculty_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        
    # TAB-02: Related To 'View Secretary' Tab
    def get_all_secretary_with_department(self):
        query = """
        SELECT s.secretary_id, s.name, s.email, d.name AS department, s.created_at
        FROM secretaries s
        LEFT JOIN department d ON s.department_id = d.department_id
        ORDER BY s.name
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
    def get_secretaries_by_department(self, department_id):
        query = """
            SELECT s.secretary_id, s.name, s.email, d.name AS department, s.created_at
            FROM secretaries s
            LEFT JOIN department d ON s.department_id = d.department_id
            WHERE s.department_id = %s
            ORDER BY s.name
        """
        self.cursor.execute(query, (department_id,))
        return self.cursor.fetchall()
    def delete_secretary_by_id(self, secretary_id):
        try:
            self.cursor.execute("DELETE FROM secretaries WHERE secretary_id = %s", (secretary_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    # TAB-03: Related To 'View Company' Tab
    def get_all_companies(self):
        query = """
            SELECT company_id, name, contact_person, email, phone, address, registered
            FROM companies
            ORDER BY name
        """
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    

    def get_companies_by_registration(self, is_registered):
        query = """
            SELECT company_id, name, contact_person, email, phone, address, registered
            FROM companies
            WHERE registered = %s
            ORDER BY name
        """
        self.cursor.execute(query, (is_registered,))
        return [dict(row) for row in self.cursor.fetchall()]

    def delete_company_by_id(self, company_id):
        try:
            self.cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def set_company_verified(self, company_id):
        try:
            self.cursor.execute("UPDATE companies SET registered = TRUE WHERE company_id = %s", (company_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

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
    
    # Faculty Management 
    def get_students_assigned_to_faculty(self, faculty_id: int) -> List[Dict]:
        try:
            query = """
                SELECT DISTINCT s.student_id, s.name, s.email, s.cgpa, d.name AS department
                FROM faculty_assignments fa
                JOIN students s ON fa.student_id = s.student_id
                JOIN department d ON s.department_id = d.department_id
                JOIN applications a ON s.student_id = a.student_id
                WHERE fa.faculty_id = %s AND a.status = 'approved'
            """
            self.cursor.execute(query, (faculty_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving assigned students: {e}")
            return []

    def get_reports_assigned_to_faculty(self, faculty_id: int) -> List[Dict]:
        try:
            query = """
                SELECT r.report_id, s.name as student_name, r.grade, r.comments, r.submitted_at
                FROM reports r
                JOIN students s ON r.student_id = s.student_id
                WHERE r.faculty_id = %s
            """
            self.cursor.execute(query, (faculty_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving reports: {e}")
            return []
        
    def grade_student_report(self, report_id: int, grade: str, comments: str) -> bool:
        try:
            query = "UPDATE reports SET grade = %s, comments = %s WHERE report_id = %s"
            self.cursor.execute(query, (grade, comments, report_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error grading report: {e}")
            return False

    # Secretary Management
    #TAB-2: related to "Assign Faculty" tab
    def get_faculty_users_by_secretary(self, secretary_id: int) -> List[Dict]:
        """Get faculty from the secretary's department"""
        try:
            query = """
                SELECT f.faculty_id, f.name
                FROM faculties f
                JOIN secretaries s ON f.department_id = s.department_id
                WHERE s.secretary_id = %s
                ORDER BY f.faculty_id
            """
            self.cursor.execute(query, (secretary_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting faculty by secretary: {e}")
            return []

    def get_approved_unassigned_students_by_secretary(self, secretary_id: int) -> List[Dict]:
        """Get approved and unassigned students from secretary's department"""
        try:
            query = """
                SELECT DISTINCT s.student_id, s.name
                FROM students s
                JOIN applications a ON s.student_id = a.student_id
                LEFT JOIN faculty_assignments fa ON s.student_id = fa.student_id
                JOIN secretaries sec ON s.department_id = sec.department_id
                WHERE a.status = 'approved' AND fa.student_id IS NULL
                AND sec.secretary_id = %s
                ORDER BY s.name
            """
            self.cursor.execute(query, (secretary_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting approved students by secretary: {e}")
            return []


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

    def get_student_users(self) -> List[Dict]:
        """Get all student users"""
        try:
            query = "SELECT * FROM students ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error getting students: {e}")
            return []


    #TAB-1: related to "Pending Applications" tab
    def get_pending_applications(self) -> List[Dict]:
        """Get all pending applications for admin review"""
        try:
            query = """
                SELECT a.app_id, a.self_found, a.application_date,
                   s.student_id, s.name AS student_name, s.email AS student_email,
                   c.name AS company_name,
                   q.department
                FROM applications a
                JOIN students s ON a.student_id = s.student_id
                JOIN companies c ON a.company_id = c.company_id
                LEFT JOIN quotas q ON a.quota_id = q.quota_id
                WHERE a.status = 'pending'
                ORDER BY a.application_date DESC
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
    
    
    
    
    
    
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()