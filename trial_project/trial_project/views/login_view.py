# =============================================================================
# VIEW LAYER - GUI Components (Updated for new table structure)
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Login - Student Internship System")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

        # Email
        ttk.Label(frame, text="Email:").pack(anchor=tk.W, pady=(10, 0))
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.pack()

        # Password
        ttk.Label(frame, text="Password:").pack(anchor=tk.W, pady=(10, 0))
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack()

        # Role
        ttk.Label(frame, text="Role:").pack(anchor=tk.W, pady=(10, 0))
        self.role_var = tk.StringVar(value="Student")
        role_combo = ttk.Combobox(frame, textvariable=self.role_var,
                                  values=["Student", "Faculty", "Secretary", "Company", "Admin"],
                                  state="readonly", width=28)
        role_combo.pack()

        ttk.Button(frame, text="Login", command=self.login).pack(pady=20)

        # Register link
        reg_label = tk.Label(frame, text="Don't Have an Account? Register Here!", foreground="blue", cursor="hand2")
        reg_label.pack()
        reg_label.bind("<Button-1>", lambda e: self.open_registration())

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get().strip()

        if not email or not password or not role:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.controller.login(email, password, role)

    def open_registration(self):
        RegistrationRoleSelector(self.controller)

    def clear_forms(self):
        """Clear login form fields"""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_var.set("Student")

    def run(self):
        self.root.mainloop()

class RegistrationRoleSelector:
    def __init__(self, controller):
        self.controller = controller
        self.popup = tk.Toplevel()
        self.popup.title("Select Role")
        self.popup.geometry("300x200")
        self.popup.resizable(False, False)
        self.popup.grab_set()  # Make popup modal

        ttk.Label(self.popup, text="Select Role to Register", font=("Arial", 12, "bold")).pack(pady=20)

        self.role_var = tk.StringVar(value="Student")
        self.role_combo = ttk.Combobox(self.popup, textvariable=self.role_var,
                                       values=["Student", "Faculty", "Secretary", "Company"], state="readonly")
        self.role_combo.pack(pady=10)

        ttk.Button(self.popup, text="Next", command=self.open_form).pack(pady=10)
        ttk.Button(self.popup, text="Cancel", command=self.popup.destroy).pack(pady=5)

    def open_form(self):
        role = self.role_var.get()
        self.popup.destroy()
        RegistrationForm(self.controller, role)

class RegistrationForm:
    def __init__(self, controller, role):
        self.controller = controller
        self.role = role
        self.popup = tk.Toplevel()
        self.popup.title(f"{role} Registration")
        self.popup.geometry("400x500")
        self.popup.resizable(False, False)
        self.popup.grab_set()  # Make popup modal

        self.entries = {}
        self.department_var = None
        self.faculty_var = None

        ttk.Label(self.popup, text=f"{role} Registration", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create scrollable frame for longer forms
        canvas = tk.Canvas(self.popup)
        scrollbar = ttk.Scrollbar(self.popup, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        form_frame = ttk.Frame(scrollable_frame, padding=10)
        form_frame.pack()

        self.setup_form_fields(form_frame)

        canvas.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))

        scrollbar.pack(side="right", fill="y", pady=10)

        # Register button at bottom
        button_frame = ttk.Frame(self.popup)
        button_frame.pack(side="bottom", fill="x", pady=(0, 10))

        ttk.Button(button_frame, text="Register", command=self.register).pack(side="left", padx=20)
        ttk.Button(button_frame, text="Cancel", command=self.popup.destroy).pack(side="left")


    def setup_form_fields(self, frame):
        """Setup form fields based on role"""
        # Common fields
        self.add_field(frame, "Full Name")
        self.add_field(frame, "Email")
        self.add_field(frame, "Password", show="*")

        # Role-specific fields
        if self.role != "Company":
            self.add_department_dropdown(frame)

        if self.role == "Student":
            self.add_field(frame, "CGPA")
        # elif self.role == "Secretary":
        #     self.add_faculty_dropdown(frame)

    def add_field(self, frame, label, show=None):
        """Add a text entry field"""
        ttk.Label(frame, text=f"{label}:").pack(anchor=tk.W, pady=(10, 2))
        entry = ttk.Entry(frame, show=show, width=35) if show else ttk.Entry(frame, width=35)
        entry.pack(pady=(0, 5))
        self.entries[label.lower().replace(" ", "_")] = entry

    def add_department_dropdown(self, frame):
        """Add department dropdown"""
        ttk.Label(frame, text="Department:").pack(anchor=tk.W, pady=(10, 2))
        
        # Get departments from controller
        departments = self.controller.get_department_names()
        
        self.department_var = tk.StringVar()
        if departments:
            self.department_var.set(departments[0])
        
        dept_combo = ttk.Combobox(frame, textvariable=self.department_var,
                                  values=departments, state="readonly", width=33)
        dept_combo.pack(pady=(0, 5))

    def add_faculty_dropdown(self, frame):
        """Add faculty dropdown for secretary registration"""
        ttk.Label(frame, text="Supervising Faculty:").pack(anchor=tk.W, pady=(10, 2))
        
        # Get faculty members from controller
        faculties = self.controller.get_faculty_users()
        faculty_options = [f"{faculty['faculty_id']} - {faculty['name']}" for faculty in faculties]
        
        self.faculty_var = tk.StringVar()
        if faculty_options:
            self.faculty_var.set(faculty_options[0])
        
        faculty_combo = ttk.Combobox(frame, textvariable=self.faculty_var,
                                     values=faculty_options, state="readonly", width=33)
        faculty_combo.pack(pady=(0, 5))

    def register(self):
        """Handle registration submission"""
        # Collect data from text entries
        data = {k: v.get().strip() for k, v in self.entries.items()}
        
        # Add department if applicable
        if self.department_var and self.role != "Company":
            data['department'] = self.department_var.get()
        
        # Add faculty_id for secretary
        # if self.faculty_var and self.role == "Secretary":
        #     faculty_selection = self.faculty_var.get()
        #     if faculty_selection:
        #         # Extract faculty_id from "ID - Name" format
        #         faculty_id = faculty_selection.split(" - ")[0]
        #         data['faculty_id'] = faculty_id
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'password']
        
        if self.role != "Company":
            required_fields.append('department')
        
        if self.role == "Student":
            required_fields.append('cgpa')
        # elif self.role == "Secretary":
        #     required_fields.append('department')
        
        # Check if all required fields are filled
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            messagebox.showerror("Error", f"Please fill in the following fields: {', '.join(missing_fields)}")
            return
        
        # Submit registration
        self.controller.register(role=self.role, **data)
        self.popup.destroy()