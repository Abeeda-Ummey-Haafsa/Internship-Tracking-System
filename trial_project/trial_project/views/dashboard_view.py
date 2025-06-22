import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List, Dict, Any

from trial_project.views.dialogs.application_dialog import ApplicationDialog
from trial_project.views.dialogs.self_found_dialog import SelfFoundDialog

class DashboardView:
    """Main Dashboard Interface"""
    
    def __init__(self, controller, user):
        self.controller = controller
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {user['name']} ({user['role'].title()})")
        self.root.geometry("1000x700")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dashboard UI"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text=f"Welcome, {self.user['name']}", 
                               font=("Arial", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Role-specific tabs
        if self.user['role'] == 'student':
            self.setup_student_tabs()
        elif self.user['role'] == 'faculty':
            self.setup_faculty_tabs()
        elif self.user['role'] == 'admin':
            self.setup_admin_tabs()
        elif self.user['role'] == 'company':
            self.setup_company_tabs()
    
    def setup_student_tabs(self):
        """Setup tabs for student role"""
        # Applications tab
        app_frame = ttk.Frame(self.notebook)
        self.notebook.add(app_frame, text="My Applications")
        self.setup_applications_tab(app_frame)
        
        # Available Quotas tab
        quota_frame = ttk.Frame(self.notebook)
        self.notebook.add(quota_frame, text="Available Quotas")
        self.setup_quotas_tab(quota_frame)
        
        # Reports tab
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="Reports")
        self.setup_reports_tab(report_frame)
    
    def setup_faculty_tabs(self):
        """Setup tabs for faculty role"""
        # Students tab
        students_frame = ttk.Frame(self.notebook)
        self.notebook.add(students_frame, text="My Students")
        
        # Evaluations tab
        eval_frame = ttk.Frame(self.notebook)
        self.notebook.add(eval_frame, text="Evaluations")
    
    def setup_admin_tabs(self):
        """Setup tabs for admin role"""
        # Pending Applications tab
        pending_frame = ttk.Frame(self.notebook)
        self.notebook.add(pending_frame, text="Pending Applications")
        self.setup_pending_applications_tab(pending_frame)
        
        # Faculty Assignment tab
        faculty_frame = ttk.Frame(self.notebook)
        self.notebook.add(faculty_frame, text="Faculty Assignment")
        self.setup_faculty_assignment_tab(faculty_frame)
        
        # Reports tab
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="System Reports")
    
    def setup_company_tabs(self):
        """Setup tabs for company role"""
        # Company Profile tab
        profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(profile_frame, text="Company Profile")
        
        # Quota Management tab
        quota_frame = ttk.Frame(self.notebook)
        self.notebook.add(quota_frame, text="Manage Quotas")
        self.setup_company_quota_tab(quota_frame)
    
    def setup_applications_tab(self, parent):
        """Setup applications tab for students"""
        # Top frame for buttons
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(top_frame, text="Apply for Internship", 
                  command=self.apply_for_internship).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Apply Self-Found", 
                  command=self.apply_self_found).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(top_frame, text="Refresh", 
                  command=self.refresh_applications).pack(side=tk.RIGHT)
        
        # Treeview for applications
        columns = ("ID", "Company", "Department", "Status", "Date", "Type")
        self.app_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.app_tree.heading(col, text=col)
            self.app_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.app_tree.yview)
        self.app_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.app_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.refresh_applications()
    
    def setup_quotas_tab(self, parent):
        """Setup quotas tab for students"""
        # Top frame for filters
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Filter by Department:").pack(side=tk.LEFT)
        self.dept_filter = ttk.Combobox(top_frame, values=["All", "Computer Science", "Engineering", "Business"])
        self.dept_filter.set("All")
        self.dept_filter.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(top_frame, text="Apply Filter", 
                  command=self.filter_quotas).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(top_frame, text="Apply to Selected", 
                  command=self.apply_to_selected_quota).pack(side=tk.RIGHT)
        
        # Treeview for quotas
        columns = ("ID", "Company", "Department", "Slots", "Deadline", "Description")
        self.quota_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.quota_tree.heading(col, text=col)
            self.quota_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar2 = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.quota_tree.yview)
        self.quota_tree.configure(yscrollcommand=scrollbar2.set)
        
        # Pack treeview and scrollbar
        self.quota_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.refresh_quotas()
    
    def setup_reports_tab(self, parent):
        """Setup reports tab for students"""
        # Upload report section
        upload_frame = ttk.LabelFrame(parent, text="Upload Internship Report", padding="10")
        upload_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.report_path_var = tk.StringVar()
        ttk.Label(upload_frame, text="Report File:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(upload_frame, textvariable=self.report_path_var, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(upload_frame, text="Browse", command=self.browse_report).grid(row=0, column=2)
        
        ttk.Button(upload_frame, text="Upload Report", 
                  command=self.upload_report).grid(row=1, column=0, columnspan=3, pady=10)
    
    def setup_pending_applications_tab(self, parent):
        """Setup pending applications tab for admin"""
        # Top frame for buttons
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(top_frame, text="Approve Selected", 
                  command=self.approve_application).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Reject Selected", 
                  command=self.reject_application).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(top_frame, text="Refresh", 
                  command=self.refresh_pending_applications).pack(side=tk.RIGHT)
        
        # Treeview for pending applications
        columns = ("ID", "Student", "Email", "Company", "Department", "Date", "Type")
        self.pending_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.pending_tree.heading(col, text=col)
            self.pending_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar3 = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.pending_tree.yview)
        self.pending_tree.configure(yscrollcommand=scrollbar3.set)
        
        # Pack treeview and scrollbar
        self.pending_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar3.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.refresh_pending_applications()
    
    def setup_faculty_assignment_tab(self, parent):
        """Setup faculty assignment tab for admin"""
        # Assignment form
        form_frame = ttk.LabelFrame(parent, text="Assign Faculty to Student", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Select Faculty:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.faculty_var = tk.StringVar()
        self.faculty_combo = ttk.Combobox(form_frame, textvariable=self.faculty_var, width=30)
        self.faculty_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Select Student:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(form_frame, textvariable=self.student_var, width=30)
        self.student_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Assign Faculty", 
                  command=self.assign_faculty_to_student).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.load_faculty_and_students()
    
    def setup_company_quota_tab(self, parent):
        """Setup quota management tab for company"""
        # Create quota form
        form_frame = ttk.LabelFrame(parent, text="Create New Quota", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Department:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.quota_dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(form_frame, textvariable=self.quota_dept_var,
                                 values=["Computer Science", "Engineering", "Business", "Mathematics", "Physics"],
                                 width=25)
        dept_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Total Slots:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.slots_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.slots_var, width=27).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.deadline_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.deadline_var, width=27).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.desc_text = tk.Text(form_frame, width=25, height=3)
        self.desc_text.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Create Quota", 
                  command=self.create_company_quota).grid(row=4, column=0, columnspan=2, pady=10)
    
    # Event handlers
    def refresh_applications(self):
        """Refresh applications list"""
        if self.user['role'] == 'student':
            applications = self.controller.get_student_applications(self.user['user_id'])
            
            # Clear existing items
            for item in self.app_tree.get_children():
                self.app_tree.delete(item)
            
            # Add applications
            for app in applications:
                app_type = "Self-Found" if app['self_found'] else "Quota-Based"
                dept = app['department'] or "N/A"
                self.app_tree.insert("", "end", values=(
                    app['app_id'], app['company_name'], dept, 
                    app['status'].title(), app['application_date'].strftime('%Y-%m-%d'), app_type
                ))
    
    def refresh_quotas(self):
        """Refresh quotas list"""
        department = None if self.dept_filter.get() == "All" else self.dept_filter.get()
        quotas = self.controller.get_available_quotas(department)
        
        # Clear existing items
        for item in self.quota_tree.get_children():
            self.quota_tree.delete(item)
        
        # Add quotas
        for quota in quotas:
            self.quota_tree.insert("", "end", values=(
                quota['quota_id'], quota['company_name'], quota['department'],
                quota['available_slots'], quota['deadline'], quota['description'][:50]
            ))
    
    def filter_quotas(self):
        """Filter quotas by department"""
        self.refresh_quotas()
    
    def apply_for_internship(self):
        """Show application dialog"""
        ApplicationDialog(self, self.controller, self.user)
    
    def apply_self_found(self):
        """Show self-found application dialog"""
        SelfFoundDialog(self, self.controller, self.user)
    
    def apply_to_selected_quota(self):
        """Apply to selected quota"""
        selection = self.quota_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a quota to apply for")
            return
        
        item = self.quota_tree.item(selection[0])
        quota_id = item['values'][0]
        
        # Get company_id from quota
        quota_data = self.controller.get_quota_details(quota_id)
        if quota_data:
            if self.controller.create_application(self.user['user_id'], quota_data['company_id'], quota_id):
                messagebox.showinfo("Success", "Application submitted successfully!")
                self.refresh_applications()
                self.refresh_quotas()
            else:
                messagebox.showerror("Error", "Failed to submit application")
    
    def browse_report(self):
        """Browse for report file"""
        filename = filedialog.askopenfilename(
            title="Select Report File",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx"), ("All files", "*.*")]
        )
        if filename:
            self.report_path_var.set(filename)
    
    def upload_report(self):
        """Upload internship report"""
        # Implementation for report upload
        messagebox.showinfo("Info", "Report upload functionality would be implemented here")
    
    def refresh_pending_applications(self):
        """Refresh pending applications for admin"""
        if self.user['role'] == 'admin':
            applications = self.controller.get_pending_applications()
            
            # Clear existing items
            for item in self.pending_tree.get_children():
                self.pending_tree.delete(item)
            
            # Add applications
            for app in applications:
                app_type = "Self-Found" if app['self_found'] else "Quota-Based"
                dept = app['department'] or "N/A"
                self.pending_tree.insert("", "end", values=(
                    app['app_id'], app['student_name'], app['student_email'],
                    app['company_name'], dept, app['application_date'].strftime('%Y-%m-%d'), app_type
                ))
    
    def approve_application(self):
        """Approve selected application"""
        selection = self.pending_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to approve")
            return
        
        item = self.pending_tree.item(selection[0])
        app_id = item['values'][0]
        
        if self.controller.update_application_status(app_id, 'approved'):
            messagebox.showinfo("Success", "Application approved successfully!")
            self.refresh_pending_applications()
        else:
            messagebox.showerror("Error", "Failed to approve application")
    
    def reject_application(self):
        """Reject selected application"""
        selection = self.pending_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to reject")
            return
        
        item = self.pending_tree.item(selection[0])
        app_id = item['values'][0]
        
        if self.controller.update_application_status(app_id, 'rejected'):
            messagebox.showinfo("Success", "Application rejected successfully!")
            self.refresh_pending_applications()
        else:
            messagebox.showerror("Error", "Failed to reject application")
    
    def load_faculty_and_students(self):
        """Load faculty and student lists for assignment"""
        faculty_list = self.controller.get_faculty_users()
        student_list = self.controller.get_student_users()
        
        # Populate faculty combo
        faculty_values = [f"{f['user_id']}: {f['name']}" for f in faculty_list]
        self.faculty_combo['values'] = faculty_values
        
        # Populate student combo
        student_values = [f"{s['user_id']}: {s['name']}" for s in student_list]
        self.student_combo['values'] = student_values
    
    def assign_faculty_to_student(self):
        """Assign faculty to student"""
        faculty_selection = self.faculty_var.get()
        student_selection = self.student_var.get()
        
        if not faculty_selection or not student_selection:
            messagebox.showwarning("Warning", "Please select both faculty and student")
            return
        
        faculty_id = int(faculty_selection.split(':')[0])
        student_id = int(student_selection.split(':')[0])
        
        if self.controller.assign_faculty(faculty_id, student_id):
            messagebox.showinfo("Success", "Faculty assigned successfully!")
        else:
            messagebox.showerror("Error", "Failed to assign faculty")
    
    def create_company_quota(self):
        """Create new quota for company"""
        department = self.quota_dept_var.get()
        slots = self.slots_var.get()
        deadline = self.deadline_var.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        
        if not all([department, slots, deadline]):
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
        
        try:
            slots = int(slots)
        except ValueError:
            messagebox.showerror("Error", "Total slots must be a number")
            return
        
        # For company role, we need to get company_id (simplified here)
        company_id = 1  # This should be properly linked to the company user
        
        if self.controller.create_quota(company_id, department, slots, deadline, description):
            messagebox.showinfo("Success", "Quota created successfully!")
            # Clear form
            self.quota_dept_var.set("")
            self.slots_var.set("")
            self.deadline_var.set("")
            self.desc_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Failed to create quota")
    
    def logout(self):
        """Logout and return to login screen"""
        self.root.destroy()
        self.controller.logout()
    
    def run(self):
        """Start the dashboard"""
        self.root.mainloop()