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
        elif self.user['role'] == 'secretary':
            self.setup_secretary_tabs()
        elif self.user['role'] == 'company':
            self.setup_company_tabs()
        elif self.user['role'] == 'admin':
            self.setup_admin_tabs()
    
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
        self.setup_my_students_tab(students_frame)
        
        # Evaluations tab
        eval_frame = ttk.Frame(self.notebook)
        self.notebook.add(eval_frame, text="Evaluations")
        self.setup_evaluations_tab(eval_frame)
    
    def setup_secretary_tabs(self):
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
    
    def setup_admin_tabs(self):
        """Setup tabs for admin role"""
        # View All Faculty Tab
        all_faculty_frame = ttk.Frame(self.notebook)
        self.notebook.add(all_faculty_frame, text="View Faculty List")
        self.setup_view_faculty_tab(all_faculty_frame)

        # Remove Faculty tab
        remove_faculty_frame = ttk.Frame(self.notebook)
        self.notebook.add(remove_faculty_frame, text="Remove Faculty")
        #self.setup_remove_faculty_tab(remove_faculty_frame)

        # View All Secretary Tab
        all_secretary_frame = ttk.Frame(self.notebook)
        self.notebook.add(all_secretary_frame, text="View Secretary List")
        #self.setup_view_secretary_tab(all_secretary_frame)

        # Remove Secretary tab
        remove_secretary_frame = ttk.Frame(self.notebook)
        self.notebook.add(remove_secretary_frame, text="Remove Secretary")
        #self.setup_remove_secretary_tab(remove_secretary_frame)

        # View All Company Tab
        all_company_frame = ttk.Frame(self.notebook)
        self.notebook.add(all_company_frame, text="View Company List")
        #self.setup_view_company_tab(all_company_frame)

        # Remove Company tab
        remove_company_frame = ttk.Frame(self.notebook)
        self.notebook.add(remove_company_frame, text="Remove Company")
        #self.setup_remove_company_tab(remove_company_frame)
    

    # RELATED TO FACULTY TAB
    def setup_my_students_tab(self, parent):
        ttk.Label(parent, text="Students Assigned to Me", font=("Arial", 14)).pack(pady=10)
        columns = ("ID", "Name", "Email", "CGPA", "Department")
        self.my_students_tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            self.my_students_tree.heading(col, text=col)
            self.my_students_tree.column(col, width=120)
        self.my_students_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_my_students()
    
    def refresh_my_students(self):
        students = self.controller.get_students_under_faculty(self.user['user_id'])
        for row in self.my_students_tree.get_children():
            self.my_students_tree.delete(row)
        for s in students:
            self.my_students_tree.insert("", "end", values=(s['student_id'], s['name'], s['email'], s['cgpa'], s['department']))

    def setup_evaluations_tab(self, parent):
        ttk.Label(parent, text="Evaluate Submitted Reports", font=("Arial", 14)).pack(
            pady=10
        )

        # Frame for Treeview

        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("Report ID", "Student Name", "Submitted At", "Grade", "Comments")
        self.report_tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=10
        )

        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120)
        self.report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.report_tree.yview
        )
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load report data

        self.refresh_faculty_reports()

        # Frame for grading form

        form_frame = ttk.LabelFrame(parent, text="Submit Evaluation", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(form_frame, text="Grade:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.grade_var = tk.StringVar()
        self.grade_entry = ttk.Entry(form_frame, textvariable=self.grade_var, width=20)
        self.grade_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Comments:").grid(
            row=1, column=0, sticky=tk.NW, padx=5, pady=5
        )
        self.comments_text = tk.Text(form_frame, width=50, height=4)
        self.comments_text.grid(row=1, column=1, padx=5, pady=5)

        submit_btn = ttk.Button(
            form_frame, text="Submit Evaluation", command=self.submit_evaluation
        )
        submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def refresh_faculty_reports(self):
        """Load reports submitted to this faculty"""
        faculty_id = self.user["user_id"]
        reports = self.controller.get_reports_for_faculty(faculty_id)

        # Clear existing

        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        for report in reports:
            self.report_tree.insert(
                "",
                "end",
                values=(
                    report["report_id"],
                    report["student_name"],
                    report["submitted_at"].strftime("%Y-%m-%d"),
                    report["grade"] or "Not Graded",
                    (report["comments"][:30] + "...") if report["comments"] else "",
                ),
            )

    def submit_evaluation(self):
        """Submit evaluation (grade + comments) for selected report"""
        selection = self.report_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to evaluate")
            return
        report_id = self.report_tree.item(selection[0])["values"][0]
        grade = self.grade_var.get().strip()
        comments = self.comments_text.get("1.0", tk.END).strip()

        if not grade:
            messagebox.showwarning("Warning", "Please enter a grade")
            return
        if self.controller.submit_report_grade(report_id, grade, comments):
            messagebox.showinfo("Success", "Evaluation submitted successfully")
            self.refresh_faculty_reports()
            self.grade_var.set("")
            self.comments_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Failed to submit evaluation")



    # RELATED TO ADMIN TAB
    def setup_view_faculty_tab(self, parent):
        """Setup view all faculty tab"""
        # Top frame for controls
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
    
        ttk.Label(top_frame, text="Faculty Management", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Refresh", command=self.refresh_faculty_list).pack(side=tk.RIGHT)
        # ttk.Button(top_frame, text="Export to CSV", command=self.export_faculty_csv).pack(side=tk.RIGHT, padx=(0, 10))
    
        # Filter frame
        # filter_frame = ttk.Frame(parent)
        # filter_frame.pack(fill=tk.X, padx=10, pady=5)
    
        # ttk.Label(filter_frame, text="Filter by Department:").pack(side=tk.LEFT)
        # self.faculty_dept_filter = ttk.Combobox(filter_frame, width=20)
        # self.faculty_dept_filter.pack(side=tk.LEFT, padx=(10, 0))
        # ttk.Button(filter_frame, text="Apply Filter", command=self.filter_faculty).pack(side=tk.LEFT, padx=(10, 0))
        # ttk.Button(filter_frame, text="Clear Filter", command=self.clear_faculty_filter).pack(side=tk.LEFT, padx=(5, 0))
    
        # Treeview Frame
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Name", "Email", "Department", "Created Date", "Total Students")
        self.faculty_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.faculty_tree.heading(col, text=col)
            if col == "Email":
                self.faculty_tree.column(col, width=200)
            elif col == "Name":
                self.faculty_tree.column(col, width=150)
            else:
                self.faculty_tree.column(col, width=120)

        # Scrollbars (correctly assigned to tree_frame)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.faculty_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.faculty_tree.xview)
        self.faculty_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout inside tree_frame
        self.faculty_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    
        # Load departments for filter
        # self.load_faculty_departments()
        # self.refresh_faculty_list()

    def refresh_faculty_list(self):
        # Clear previous Treeview rows
        for row in self.faculty_tree.get_children():
            self.faculty_tree.delete(row)

        try:
            faculty_list = self.controller.get_faculty_users()

            for faculty in faculty_list:
                faculty_id = faculty.get("faculty_id") or faculty.get("id")  # Adjust based on actual DB schema
                name = faculty.get("name")
                email = faculty.get("email")
                department = faculty.get("department")
                created_at = faculty.get("created_at")

                # Optional: get total students under this faculty if required
                total_students = self.controller.get_total_students_for_faculty(faculty_id)

                self.faculty_tree.insert("", "end", values=(
                    faculty_id, name, email, department, created_at, total_students
                ))

        except Exception as e:
            print("Failed to refresh faculty list:", e)


    
    # RELATED TO STUDENT TAB
    # TAB-01: related to "My Applications" tab
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

    def apply_for_internship(self):
        """Show application dialog"""
        ApplicationDialog(self, self.controller, self.user)
    
    def apply_self_found(self):
        """Show self-found application dialog"""
        SelfFoundDialog(self, self.controller, self.user)
    
    # TAB-02: related to "Available Quotas" tab
    def setup_quotas_tab(self, parent):
        """Setup quotas tab for students"""
        # Top frame for filters
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Filter by Department:").pack(side=tk.LEFT)
        self.dept_filter = ttk.Combobox(top_frame, values=["All", "Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Business Administration"])
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
    
    # TAB-03: related to "Reports" tab
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
    
    
    
    
    # RELATED TO SECRETARY TAB
    #TAB-1: related to "Pending Applications" tab
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

    def refresh_pending_applications(self):
        """Refresh pending applications for secretary"""
        if self.user['role'] == 'secretary':
            applications = self.controller.get_pending_applications()
            
            # Clear existing items
            for item in self.pending_tree.get_children():
                self.pending_tree.delete(item)
            
            # Add applications
            for app in applications:
                app_type = "Self-Found" if app['self_found'] else "Quota-Based"
                dept = app['department'] or "N/A"
                try:
                    self.pending_tree.insert("", "end", values=(
                        app['app_id'], app['student_name'], app['student_email'],
                        app['company_name'], dept, app['application_date'].strftime('%Y-%m-%d'), app_type
                    ))
                except Exception as e:
                    print("Error inserting pending application row:", e)

    #TAB-2: related to "Assign Faculty" tab
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

        self.load_faculty_and_students()

    def load_faculty_and_students(self):
        """Load faculty and student lists for assignment"""
        faculty_list = self.controller.get_faculty_users()
        student_list = student_list = self.controller.get_approved_unassigned_students()
        
        # Populate faculty combo
        faculty_values = [f"{f['user_id']}: {f['name']}" for f in faculty_list]
        self.faculty_combo['values'] = faculty_values
        
        # Populate student combo
        student_values = [f"{s['user_id']}: {s['name']}" for s in student_list]
        self.student_combo['values'] = student_values
    
    
    

    # RELATED TO COMPANY TAB
    def setup_company_quota_tab(self, parent):
        """Setup quota management tab for company"""
        # Create quota form
        form_frame = ttk.LabelFrame(parent, text="Create New Quota", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Department:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.quota_dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(form_frame, textvariable=self.quota_dept_var,
                                 values=["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Business Administration"],
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