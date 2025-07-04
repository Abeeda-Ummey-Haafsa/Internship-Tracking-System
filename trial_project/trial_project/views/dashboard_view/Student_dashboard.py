import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

class StudentDashboard:
    def __init__(self, controller, user):
        self.controller = controller
        self.user = user
        self.root = tk.Tk()
        self.root.title("Student Dashboard - Internship Management System")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Sidebar
        self.create_sidebar(main_frame)
        
        # Content area
        self.create_content_area(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create header with user info and logout"""
        header_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="Student Dashboard", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        # User info
        user_info_frame = ttk.Frame(header_frame)
        user_info_frame.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        
        user_name = self.controller.get_user_name()
        user_email = self.controller.get_user_email()
        user_dept = self.controller.get_user_department()
        
        ttk.Label(user_info_frame, text=f"Welcome, {user_name}", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.E)
        ttk.Label(user_info_frame, text=f"Email: {user_email}").pack(anchor=tk.E)
        ttk.Label(user_info_frame, text=f"Department: {user_dept}").pack(anchor=tk.E)
        
        # Logout button
        ttk.Button(header_frame, text="Logout", command=self.logout).grid(row=0, column=2, padx=10, pady=10)
    
    def create_sidebar(self, parent):
        """Create sidebar with navigation"""
        sidebar_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        sidebar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(sidebar_frame, text="Navigation", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Navigation buttons
        nav_buttons = [
            ("Profile", self.show_profile),
            ("Applications", self.show_applications),
            ("Available Quotas", self.show_quotas),
            ("Apply for Internship", self.show_apply_form),
            ("Reports", self.show_reports),
            ("Settings", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar_frame, text=text, command=command, width=20)
            btn.pack(pady=5, padx=10, fill=tk.X)
    
    def create_content_area(self, parent):
        """Create main content area with notebook"""
        content_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        content_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Create tabs
        self.create_profile_tab()
        self.create_applications_tab()
        self.create_quotas_tab()
        self.create_apply_tab()
        self.create_reports_tab()
    
    def create_profile_tab(self):
        """Create profile information tab"""
        profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(profile_frame, text="Profile")
        
        # Create scrollable frame
        canvas = tk.Canvas(profile_frame)
        scrollbar = ttk.Scrollbar(profile_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Profile content
        profile_content = ttk.Frame(scrollable_frame, padding="20")
        profile_content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(profile_content, text="Student Profile", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Profile information
        info_frame = ttk.LabelFrame(profile_content, text="Personal Information", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid layout for profile info
        info_frame.columnconfigure(1, weight=1)
        
        profile_fields = [
            ("Full Name:", self.controller.get_user_name()),
            ("Email:", self.controller.get_user_email()),
            ("Department:", self.controller.get_user_department()),
            ("CGPA:", f"{self.user.get('cgpa', 'N/A')}"),
            ("Student ID:", str(self.user.get('student_id', 'N/A'))),
            ("Member Since:", self.user.get('created_at', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(profile_fields):
            ttk.Label(info_frame, text=label, font=("Arial", 9, "bold")).grid(row=i, column=0, sticky=tk.W, pady=5)
            ttk.Label(info_frame, text=str(value)).grid(row=i, column=1, sticky=tk.W, padx=(20, 0), pady=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(profile_content, text="Statistics", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Load statistics
        self.load_student_statistics(stats_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_applications_tab(self):
        """Create applications tab"""
        app_frame = ttk.Frame(self.notebook)
        self.notebook.add(app_frame, text="My Applications")
        
        # Header
        header_frame = ttk.Frame(app_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="My Applications", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Refresh", 
                  command=self.refresh_applications).pack(side=tk.RIGHT)
        
        # Applications treeview
        tree_frame = ttk.Frame(app_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create treeview
        columns = ("ID", "Company", "Department", "Status", "Applied Date", "Type")
        self.app_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.app_tree.heading("ID", text="App ID")
        self.app_tree.heading("Company", text="Company")
        self.app_tree.heading("Department", text="Department")
        self.app_tree.heading("Status", text="Status")
        self.app_tree.heading("Applied Date", text="Applied Date")
        self.app_tree.heading("Type", text="Type")
        
        # Column widths
        self.app_tree.column("ID", width=60)
        self.app_tree.column("Company", width=150)
        self.app_tree.column("Department", width=120)
        self.app_tree.column("Status", width=100)
        self.app_tree.column("Applied Date", width=120)
        self.app_tree.column("Type", width=100)
        
        # Add scrollbar
        app_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.app_tree.yview)
        self.app_tree.configure(yscrollcommand=app_scrollbar.set)
        
        self.app_tree.pack(side="left", fill="both", expand=True)
        app_scrollbar.pack(side="right", fill="y")
        
        # Context menu for applications
        self.app_tree.bind("<Button-3>", self.show_application_context_menu)
    
    def create_quotas_tab(self):
        """Create available quotas tab"""
        quota_frame = ttk.Frame(self.notebook)
        self.notebook.add(quota_frame, text="Available Quotas")
        
        # Header
        header_frame = ttk.Frame(quota_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Available Quotas", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Refresh", 
                  command=self.refresh_quotas).pack(side=tk.RIGHT)
        
        # Filter frame
        filter_frame = ttk.Frame(quota_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter by Department:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.dept_filter_var = tk.StringVar(value="All")
        dept_values = ["All"] + self.controller.get_department_names()
        dept_combo = ttk.Combobox(filter_frame, textvariable=self.dept_filter_var,
                                 values=dept_values, state="readonly", width=20)
        dept_combo.pack(side=tk.LEFT, padx=(0, 10))
        dept_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_quotas())
        
        # Quotas treeview
        quota_tree_frame = ttk.Frame(quota_frame)
        quota_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create treeview
        quota_columns = ("ID", "Company", "Department", "Total Slots", "Available", "Deadline", "Description")
        self.quota_tree = ttk.Treeview(quota_tree_frame, columns=quota_columns, show="headings", height=15)
        
        # Configure columns
        for col in quota_columns:
            self.quota_tree.heading(col, text=col)
        
        # Column widths
        self.quota_tree.column("ID", width=50)
        self.quota_tree.column("Company", width=150)
        self.quota_tree.column("Department", width=120)
        self.quota_tree.column("Total Slots", width=80)
        self.quota_tree.column("Available", width=80)
        self.quota_tree.column("Deadline", width=100)
        self.quota_tree.column("Description", width=200)
        
        # Add scrollbar
        quota_scrollbar = ttk.Scrollbar(quota_tree_frame, orient="vertical", command=self.quota_tree.yview)
        self.quota_tree.configure(yscrollcommand=quota_scrollbar.set)
        
        self.quota_tree.pack(side="left", fill="both", expand=True)
        quota_scrollbar.pack(side="right", fill="y")
        
        # Double-click to apply
        self.quota_tree.bind("<Double-1>", self.apply_to_quota)
    
    def create_apply_tab(self):
        """Create application form tab"""
        apply_frame = ttk.Frame(self.notebook)
        self.notebook.add(apply_frame, text="Apply for Internship")
        
        # Create scrollable frame
        canvas = tk.Canvas(apply_frame)
        scrollbar = ttk.Scrollbar(apply_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Application form content
        form_content = ttk.Frame(scrollable_frame, padding="20")
        form_content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_content, text="Apply for Internship", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Application type selection
        type_frame = ttk.LabelFrame(form_content, text="Application Type", padding="15")
        type_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.app_type_var = tk.StringVar(value="quota")
        ttk.Radiobutton(type_frame, text="Apply through Quota", 
                       variable=self.app_type_var, value="quota",
                       command=self.toggle_application_type).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(type_frame, text="Self-Found Internship", 
                       variable=self.app_type_var, value="self_found",
                       command=self.toggle_application_type).pack(anchor=tk.W, pady=5)
        
        # Quota-based application
        self.quota_frame = ttk.LabelFrame(form_content, text="Quota-Based Application", padding="15")
        self.quota_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.quota_frame, text="Select Quota:").pack(anchor=tk.W, pady=(0, 5))
        self.quota_var = tk.StringVar()
        self.quota_combo = ttk.Combobox(self.quota_frame, textvariable=self.quota_var,
                                       state="readonly", width=50)
        self.quota_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Self-found application
        self.self_found_frame = ttk.LabelFrame(form_content, text="Self-Found Application", padding="15")
        self.self_found_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.self_found_frame, text="Company:").pack(anchor=tk.W, pady=(0, 5))
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(self.self_found_frame, textvariable=self.company_var,
                                         state="readonly", width=50)
        self.company_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Submit button
        ttk.Button(form_content, text="Submit Application", 
                  command=self.submit_application).pack(pady=20)
        
        # Initialize form
        self.toggle_application_type()
        self.load_application_data()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_reports_tab(self):
        """Create reports tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        ttk.Label(reports_frame, text="Internship Reports", 
                 font=("Arial", 14, "bold")).pack(pady=20)
        
        # Reports will be implemented based on your requirements
        info_label = ttk.Label(reports_frame, 
                              text="Reports functionality will be available after internship completion.",
                              font=("Arial", 10))
        info_label.pack(pady=20)
    
    def create_footer(self, parent):
        """Create footer with status information"""
        footer_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        footer_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(footer_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Current time
        self.time_label = ttk.Label(footer_frame, text="")
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.update_time()
    
    def update_time(self):
        """Update current time in footer"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update every second
    
    def load_dashboard_data(self):
        """Load initial dashboard data"""
        self.refresh_applications()
        self.refresh_quotas()
    
    def load_student_statistics(self, parent):
        """Load and display student statistics"""
        student_id = self.controller.get_user_id()
        applications = self.controller.get_student_applications(student_id)
        
        # Calculate statistics
        total_apps = len(applications)
        pending_apps = len([app for app in applications if app.get('status') == 'pending'])
        approved_apps = len([app for app in applications if app.get('status') == 'approved'])
        rejected_apps = len([app for app in applications if app.get('status') == 'rejected'])
        
        # Grid layout for statistics
        parent.columnconfigure(1, weight=1)
        
        stats = [
            ("Total Applications:", total_apps),
            ("Pending Applications:", pending_apps),
            ("Approved Applications:", approved_apps),
            ("Rejected Applications:", rejected_apps),
            ("Success Rate:", f"{(approved_apps/total_apps*100):.1f}%" if total_apps > 0 else "0%")
        ]
        
        for i, (label, value) in enumerate(stats):
            ttk.Label(parent, text=label, font=("Arial", 9, "bold")).grid(row=i, column=0, sticky=tk.W, pady=5)
            ttk.Label(parent, text=str(value)).grid(row=i, column=1, sticky=tk.W, padx=(20, 0), pady=5)
    
    def refresh_applications(self):
        """Refresh applications list"""
        # Clear existing items
        for item in self.app_tree.get_children():
            self.app_tree.delete(item)
        
        # Load applications
        student_id = self.controller.get_user_id()
        applications = self.controller.get_student_applications(student_id)
        
        for app in applications:
            app_type = "Self-Found" if app.get('self_found') else "Quota-Based"
            app_date = app.get('application_date', '')
            if app_date:
                app_date = str(app_date).split()[0]  # Get date part only
            
            self.app_tree.insert("", tk.END, values=(
                app.get('app_id', ''),
                app.get('company_name', ''),
                app.get('department', ''),
                app.get('status', '').title(),
                app_date,
                app_type
            ))
        
        self.status_label.config(text=f"Loaded {len(applications)} applications")
    
    def refresh_quotas(self):
        """Refresh available quotas"""
        # Clear existing items
        for item in self.quota_tree.get_children():
            self.quota_tree.delete(item)
        
        # Get department filter
        dept_filter = self.dept_filter_var.get()
        department = None if dept_filter == "All" else dept_filter
        
        # Load quotas
        quotas = self.controller.get_available_quotas(department)
        
        for quota in quotas:
            self.quota_tree.insert("", tk.END, values=(
                quota.get('quota_id', ''),
                quota.get('company_name', ''),
                quota.get('department', ''),
                quota.get('total_slots', ''),
                quota.get('available_slots', ''),
                quota.get('deadline', ''),
                quota.get('description', '')[:50] + "..." if len(quota.get('description', '')) > 50 else quota.get('description', '')
            ))
        
        self.status_label.config(text=f"Loaded {len(quotas)} available quotas")
    
    def toggle_application_type(self):
        """Toggle between quota-based and self-found application"""
        if self.app_type_var.get() == "quota":
            self.quota_frame.pack(fill=tk.X, pady=(0, 20))
            self.self_found_frame.pack_forget()
        else:
            self.self_found_frame.pack(fill=tk.X, pady=(0, 20))
            self.quota_frame.pack_forget()
    
    def load_application_data(self):
        """Load data for application form"""
        # Load quotas
        student_dept = self.controller.get_user_department()
        quotas = self.controller.get_available_quotas(student_dept)
        quota_options = [f"{quota['quota_id']} - {quota['company_name']} ({quota['available_slots']} slots)" 
                        for quota in quotas]
        self.quota_combo['values'] = quota_options
        
        # Load companies
        companies = self.controller.get_all_companies()
        company_options = [f"{company['company_id']} - {company['name']}" 
                          for company in companies]
        self.company_combo['values'] = company_options
    
    def submit_application(self):
        """Submit application"""
        try:
            student_id = self.controller.get_user_id()
            
            if self.app_type_var.get() == "quota":
                # Quota-based application
                quota_selection = self.quota_var.get()
                if not quota_selection:
                    messagebox.showerror("Error", "Please select a quota")
                    return
                
                quota_id = int(quota_selection.split(" - ")[0])
                company_id = None  # Will be determined by quota
                
                # Get quota details to find company
                quota_details = self.controller.get_quota_details(quota_id)
                if quota_details:
                    company_id = quota_details['company_id']
                
                success = self.controller.create_application(student_id, company_id, quota_id, False)
                
            else:
                # Self-found application
                company_selection = self.company_var.get()
                if not company_selection:
                    messagebox.showerror("Error", "Please select a company")
                    return
                
                company_id = int(company_selection.split(" - ")[0])
                success = self.controller.create_application(student_id, company_id, None, True)
            
            if success:
                messagebox.showinfo("Success", "Application submitted successfully!")
                self.refresh_applications()
                self.load_application_data()  # Refresh available quotas
                # Clear form
                self.quota_var.set("")
                self.company_var.set("")
            else:
                messagebox.showerror("Error", "Failed to submit application")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid selection")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def apply_to_quota(self, event):
        """Apply to selected quota via double-click"""
        selection = self.quota_tree.selection()
        if not selection:
            return
        
        item = self.quota_tree.item(selection[0])
        quota_id = item['values'][0]
        company_name = item['values'][1]
        available_slots = item['values'][4]
        
        if available_slots == 0:
            messagebox.showwarning("Warning", "No slots available for this quota")
            return
        
        result = messagebox.askyesno("Confirm Application", 
                                   f"Apply to {company_name}?\n\nThis will submit your application.")
        
        if result:
            try:
                student_id = self.controller.get_user_id()
                
                # Get quota details to find company
                quota_details = self.controller.get_quota_details(quota_id)
                if quota_details:
                    company_id = quota_details['company_id']
                    success = self.controller.create_application(student_id, company_id, quota_id, False)
                    
                    if success:
                        messagebox.showinfo("Success", "Application submitted successfully!")
                        self.refresh_applications()
                        self.refresh_quotas()
                    else:
                        messagebox.showerror("Error", "Failed to submit application")
                else:
                    messagebox.showerror("Error", "Could not find quota details")
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def show_application_context_menu(self, event):
        """Show context menu for application"""
        # This can be implemented to show application details, cancel application, etc.
        pass
    
    def show_profile(self):
        """Show profile tab"""
        self.notebook.select(0)
    
    def show_applications(self):
        """Show applications tab"""
        self.notebook.select(1)
    
    def show_quotas(self):
        """Show quotas tab"""
        self.notebook.select(2)
    
    def show_apply_form(self):
        """Show apply form tab"""
        self.notebook.select(3)
    
    def show_reports(self):
        """Show reports tab"""
        self.notebook.select(4)
    
    def show_settings(self):
        """Show settings (placeholder)"""
        messagebox.showinfo("Settings", "Settings functionality will be implemented soon.")
    
    def logout(self):
        """Handle logout"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.controller.logout()
    
    def run(self):
        """Run the dashboard"""
        self.root.mainloop()

# Example usage within your dashboard_view.py
def create_student_dashboard(controller, user):
    """Factory function to create student dashboard"""
    return StudentDashboard(controller, user)