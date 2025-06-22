# =============================================================================
# VIEW LAYER - GUI Components
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class LoginView:
    """Login and Registration Interface"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Student Internship Tracking System - Login")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Internship Tracking System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Login Form
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding="15")
        login_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(login_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(login_frame, width=30)
        self.email_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(login_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        login_btn = ttk.Button(login_frame, text="Login", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Registration Form
        reg_frame = ttk.LabelFrame(main_frame, text="Register New User", padding="15")
        reg_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(reg_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_name_entry = ttk.Entry(reg_frame, width=30)
        self.reg_name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(reg_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_email_entry = ttk.Entry(reg_frame, width=30)
        self.reg_email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(reg_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_password_entry = ttk.Entry(reg_frame, width=30, show="*")
        self.reg_password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(reg_frame, text="Role:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(reg_frame, textvariable=self.role_var, 
                                 values=["student", "faculty", "admin", "company"], 
                                 state="readonly", width=27)
        role_combo.grid(row=3, column=1, pady=5)
        
        ttk.Label(reg_frame, text="Department:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(reg_frame, textvariable=self.dept_var,
                                 values=["Computer Science", "Engineering", "Business", "Mathematics", "Physics"],
                                 width=27)
        dept_combo.grid(row=4, column=1, pady=5)
        
        register_btn = ttk.Button(reg_frame, text="Register", command=self.register)
        register_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        self.controller.login(email, password)
    
    def register(self):
        """Handle registration"""
        name = self.reg_name_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        role = self.role_var.get()
        department = self.dept_var.get().strip()
        
        if not all([name, email, password, role]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        self.controller.register(name, email, password, role, department)
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
    
    def show_success(self, message):
        """Show success message"""
        messagebox.showinfo("Success", message)
    
    def clear_forms(self):
        """Clear all form fields"""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.reg_name_entry.delete(0, tk.END)
        self.reg_email_entry.delete(0, tk.END)
        self.reg_password_entry.delete(0, tk.END)
        self.role_var.set("student")
        self.dept_var.set("")
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()