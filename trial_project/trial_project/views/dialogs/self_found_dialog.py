import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List, Dict, Any

class SelfFoundDialog:
    """Dialog for self-found internship application"""
    
    def __init__(self, parent, controller, user):
        self.parent = parent
        self.controller = controller
        self.user = user
        
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.title("Apply for Self-Found Internship")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent.root)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Company details form
        ttk.Label(main_frame, text="Company Information", 
                 font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(form_frame, text="Company Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.company_name = ttk.Entry(form_frame, width=40)
        self.company_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contact Person:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.contact_person = ttk.Entry(form_frame, width=40)
        self.contact_person.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email = ttk.Entry(form_frame, width=40)
        self.email.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone = ttk.Entry(form_frame, width=40)
        self.phone.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Address:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.address = tk.Text(form_frame, width=30, height=3)
        self.address.grid(row=4, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Submit Application", 
                  command=self.submit_application).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def submit_application(self):
        """Submit self-found application"""
        name = self.company_name.get().strip()
        contact = self.contact_person.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        address = self.address.get("1.0", tk.END).strip()
        
        if not all([name, contact, email]):
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
        
        # Create company first
        if self.controller.create_company(name, contact, email, phone, address):
            # Get the newly created company
            companies = self.controller.get_all_companies()
            company_id = None
            for company in companies:
                if company['name'] == name and company['email'] == email:
                    company_id = company['company_id']
                    break
            
            if company_id and self.controller.create_application(self.user['user_id'], company_id, self_found=True):
                messagebox.showinfo("Success", "Self-found internship application submitted successfully!")
                self.parent.refresh_applications()
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to submit application")
        else:
            messagebox.showerror("Error", "Failed to create company record")