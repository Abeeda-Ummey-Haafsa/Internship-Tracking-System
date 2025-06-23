# Student Internship Tracking System
# Complete Desktop GUI Application with MVC Architecture

#!/usr/bin/env python3
"""
Main application entry point for Student Internship Management System
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from trial_project.controllers.internship_controller import InternshipController

def main():
    """Main application entry point"""
    try:
        # Create and start the application
        app = InternshipController()
        app.start_application()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup resources
        if 'app' in locals():
            app.cleanup()

if __name__ == "__main__":
    main()