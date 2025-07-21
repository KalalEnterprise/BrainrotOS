#!/usr/bin/env python3
"""
🧠 BrainrotOS - The most cursed desktop environment ever created
A satirical, Gen Z-themed desktop shell that parodies modern OS environments.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from splash_screen import BrainrotSplashScreen
from desktop_shell import BrainrotDesktop

class BrainrotOS:
    def __init__(self):
        # Enable high DPI scaling BEFORE creating QApplication
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        self.app = QApplication(sys.argv)
        self.setup_application()
        
    def setup_application(self):
        # Set application properties
        self.app.setApplicationName("BrainrotOS")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Brainrot Industries")
        
        # Set global font
        font = QFont("Courier New", 10)
        self.app.setFont(font)
        
        # Set dark theme
        self.app.setStyle('Fusion')
        
    def run(self):
        """Launch BrainrotOS with splash screen"""
        print("🧠 Initializing BrainrotOS...")
        print("⚡ Loading brainrot protocols...")
        print("🎮 Starting the most cursed OS experience...")
        
        # Show splash screen
        splash = BrainrotSplashScreen()
        splash.show()
        
        # Create desktop (but don't show yet)
        desktop = BrainrotDesktop()
        
        # Connect splash finished signal to show desktop
        def show_desktop():
            splash.close()
            desktop.show()
            print("✅ BrainrotOS loaded successfully!")
            print("🎯 Welcome to the terminal online experience!")
            
        splash.finished.connect(show_desktop)
        
        # Start the application
        return self.app.exec_()

def main():
    """Main entry point"""
    try:
        # Create and run BrainrotOS
        brainrot_os = BrainrotOS()
        sys.exit(brainrot_os.run())
        
    except KeyboardInterrupt:
        print("\n🛑 BrainrotOS terminated by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"💀 Fatal error in BrainrotOS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
