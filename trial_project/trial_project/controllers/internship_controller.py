from typing import Optional, List, Dict, Any
from trial_project.models.database_model import DatabaseModel
from trial_project.views.dashboard_view import DashboardView
from trial_project.views.login_view import LoginView


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
    
    def login(self, email: str, password: str):
        """Handle user login"""
        user = self.model.authenticate_user(email, password)
        if user:
            self.current_user = user
            self.login_view.root.destroy()
            self.show_dashboard()
        else:
            self.login_view.show_error("Invalid email or password")
    
    def register(self, name: str, email: str, password: str, role: str, department: str):
        """Handle user registration"""
        if self.model.create_user(name, email, password, role, department):
            self.login_view.show_success("Registration successful! Please login.")
            self.login_view.clear_forms()
        else:
            self.login_view.show_error("Registration failed. Email might already exist.")
    
    def show_dashboard(self):
        """Show role-based dashboard"""
        self.dashboard_view = DashboardView(self, self.current_user)
        self.dashboard_view.run()
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.start_application()
    
    # Application management
    def get_student_applications(self, student_id: int) -> List[Dict]:
        """Get applications for a student"""
        return self.model.get_applications_by_student(student_id)
    
    def get_pending_applications(self) -> List[Dict]:
        """Get pending applications for admin"""
        return self.model.get_pending_applications()
    
    def create_application(self, student_id: int, company_id: int, quota_id: int = None, self_found: bool = False) -> bool:
        """Create new application"""
        return self.model.create_application(student_id, company_id, quota_id, self_found)
    
    def update_application_status(self, app_id: int, status: str) -> bool:
        """Update application status"""
        return self.model.update_application_status(app_id, status)
    
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
        return self.model.create_company(name, contact_person, email, phone, address)
    
    # Faculty management
    def get_faculty_users(self) -> List[Dict]:
        """Get faculty users"""
        return self.model.get_faculty_users()
    
    def get_student_users(self) -> List[Dict]:
        """Get student users"""
        return self.model.get_student_users()
    
    def assign_faculty(self, faculty_id: int, student_id: int) -> bool:
        """Assign faculty to student"""
        return self.model.assign_faculty(faculty_id, student_id)
    
    def cleanup(self):
        """Cleanup resources"""
        if self.model:
            self.model.close_connection()