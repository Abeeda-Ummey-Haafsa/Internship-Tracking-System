# Student Internship Tracking System
# Complete Desktop GUI Application with MVC Architecture

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from trial_project.controllers.internship_controller import InternshipController


def main():
    """Main application entry point"""
    try:
        controller = InternshipController()
        controller.start_application()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Application Error", f"An error occurred: {e}")
    finally:
        # Cleanup
        try:
            controller.cleanup()
        except:
            pass

if __name__ == "__main__":
    main()