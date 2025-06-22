import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List, Dict, Any

class ApplicationDialog:
    """Dialog for internship application"""
    
    def __init__(self, parent, controller, user):
        self.parent = parent
        self.controller = controller
        self.user = user
        
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.title("Apply for Internship")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent.root)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Select Company:", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(main_frame, textvariable=self.company_var, width=40)
        self.company_combo.pack(fill=tk.X, pady=5)
        
        # Load companies
        companies = self.controller.get_all_companies()
        company_values = [f"{c['company_id']}: {c['name']}" for c in companies]
        self.company_combo['values'] = company_values
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Submit Application", 
                  command=self.submit_application).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def submit_application(self):
        """Submit the application"""
        company_selection = self.company_var.get()
        if not company_selection:
            messagebox.showwarning("Warning", "Please select a company")
            return
        
        company_id = int(company_selection.split(':')[0])
        
        if self.controller.create_application(self.user['user_id'], company_id, self_found=True):
            messagebox.showinfo("Success", "Application submitted successfully!")
            self.parent.refresh_applications()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to submit application")