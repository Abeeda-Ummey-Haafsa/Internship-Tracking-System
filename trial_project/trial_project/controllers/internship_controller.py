from typing import Optional, List, Dict, Any
from trial_project.models.database_model import DatabaseModel
from views.dashboard_view.dashboard_view import DashboardView
from trial_project.views.login_view import LoginView
from tkinter import messagebox


class InternshipController:
    """Main controller handling business logic"""
    
    def __init__(self):
        self.model = DatabaseModel()
        self.current_user = None
        self.login_view = None
        self.dashboard_view = None
    
    def start_application(self):
        """Start the application"""
        self.login_view = LoginView(self)
        self.login_view.run()
    
    def login(self, email: str, password: str, role: str):
        """Handle user login"""
        if not email or not password or not role:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        user = self.model.authenticate_user(email, password, role)
        if user:
            self.current_user = user
            self.login_view.root.destroy()
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email, password, or role")
    
    def register(self, role: str, **kwargs):
        """Handle user registration"""
        # Validate required fields based on role
        required_fields = ['full_name', 'email', 'password']
        
        if role.lower() != 'company' and role.lower() != 'admin':
            required_fields.append('department')
        
        if role.lower() == 'student':
            required_fields.append('cgpa')
        
        # Check if all required fields are present and not empty
        for field in required_fields:
            if field not in kwargs or not kwargs[field]:
                messagebox.showerror("Registration Error", f"Please fill in the {field.replace('_', ' ').title()} field.")
                return
        
        # Validate CGPA for students
        if role.lower() == 'student':
            try:
                cgpa = float(kwargs['cgpa'])
                if cgpa < 2.0 or cgpa > 4.0:
                    messagebox.showerror("Registration Error", "CGPA must be between 2.00 and 4.00")
                    return
            except ValueError:
                messagebox.showerror("Registration Error", "CGPA must be a valid number")
                return
        
        
        # Attempt to create user
        if self.model.create_user_by_role(role, **kwargs):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            # Clear the registration form if available
            if hasattr(self.login_view, 'clear_forms'):
                self.login_view.clear_forms()
        else:
            messagebox.showerror("Registration Error", "Registration failed. Email might already exist or invalid data provided.")
    
    def show_dashboard(self):
        """Show role-based dashboard"""
        self.dashboard_view = DashboardView(self, self.current_user)
        self.dashboard_view.run()
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        if self.dashboard_view:
            self.dashboard_view.root.destroy()
        self.start_application()
    
    # Admin Management
    def get_total_students_for_faculty(self, faculty_id: int) -> int:
        return self.model.get_total_students_for_faculty(faculty_id)

    # Application management
    def get_student_applications(self, student_id: int) -> List[Dict]:
        """Get applications for a student"""
        return self.model.get_applications_by_student(student_id)
    
    def create_application(self, student_id: int, company_id: int, quota_id: int = None, self_found: bool = False) -> bool:
        """Create new application"""
        return self.model.create_application(student_id, company_id, quota_id, self_found)
    
    # Quota management
    def get_available_quotas(self, department: str = None) -> List[Dict]:
        """Get available quotas"""
        return self.model.get_available_quotas(department)
    
    def get_quota_details(self, quota_id: int) -> Optional[Dict]:
        """Get quota details by ID"""
        try:
            query = "SELECT * FROM quotas WHERE quota_id = %s"
            self.model.cursor.execute(query, (quota_id,))
            return self.model.cursor.fetchone()
        except Exception as e:
            print(f"Error getting quota details: {e}")
            return None
    
    def create_quota(self, company_id: int, department: str, total_slots: int, deadline: str, description: str) -> bool:
        """Create new quota"""
        return self.model.create_quota(company_id, department, total_slots, deadline, description)
    
    # Company management
    def get_all_companies(self) -> List[Dict]:
        """Get all companies"""
        return self.model.get_all_companies()
    
    def create_company(self, name: str, contact_person: str, email: str, phone: str, address: str) -> bool:
        """Create new company"""
        # This method might need to be updated based on your new company table structure
        return self.model.create_company_user(name, email, "default_password")
    
    # Faculty management
    def get_students_under_faculty(self, faculty_id: int) -> List[Dict]:
        return self.model.get_students_assigned_to_faculty(faculty_id)
    
    def get_reports_for_faculty(self, faculty_id: int) -> List[Dict]:
        return self.model.get_reports_assigned_to_faculty(faculty_id)
    
    def submit_report_grade(self, report_id: int, grade: str, comments: str) -> bool:
        return self.model.grade_student_report(report_id, grade, comments)
    
    # Secretary Management
    #TAB-1: related to "Pending Applications" tab
    def get_pending_applications(self) -> List[Dict]:
        """Get pending applications for secretary"""
        return self.model.get_pending_applications()
    
    def update_application_status(self, app_id: int, status: str) -> bool:
        """Update application status"""
        return self.model.update_application_status(app_id, status)

    #TAB-2: related to "Assign Faculty" tab
    def get_approved_unassigned_students(self) -> List[Dict]:
        return self.model.get_approved_unassigned_students()
    
    def get_faculty_users(self) -> List[Dict]:
        """Get faculty users from the model"""
        return self.model.get_faculty_users()
    
    def assign_faculty(self, faculty_id: int, student_id: int) -> bool:
        """Assign faculty to student"""
        return self.model.assign_faculty(faculty_id, student_id)
    
    # Department management
    def get_all_departments(self) -> List[Dict]:
        """Get all departments"""
        return self.model.get_all_departments()
    
    def get_department_names(self) -> List[str]:
        """Get department names for dropdowns"""
        departments = self.get_all_departments()
        return [dept['name'] for dept in departments]
    
    # User management utilities
    def get_current_user_info(self) -> Optional[Dict]:
        """Get current user information"""
        return self.current_user
    
    def get_user_role(self) -> str:
        """Get current user role"""
        return self.current_user['role'] if self.current_user else None
    
    def get_user_id(self) -> int:
        """Get current user ID"""
        return self.current_user['user_id'] if self.current_user else None
    
    def get_user_name(self) -> str:
        """Get current user name"""
        return self.current_user['name'] if self.current_user else None
    
    def get_user_email(self) -> str:
        """Get current user email"""
        return self.current_user['email'] if self.current_user else None
    
    def get_user_department(self) -> str:
        """Get current user department (for students, faculty, secretary)"""
        if self.current_user and 'department_id' in self.current_user:
            departments = self.get_all_departments()
            for dept in departments:
                if dept['department_id'] == self.current_user['department_id']:
                    return dept['name']
        return None
    
    def cleanup(self):
        """Cleanup resources"""
        if self.model:
            self.model.close_connection()