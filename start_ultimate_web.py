#!/usr/bin/env python3
"""
Start Ultimate Legal Agent Web Interface
=======================================
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Timer

def check_python_version():
    """Check if Python version is sufficient"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"💡 Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import sklearn
        import pandas
        import numpy
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Install with: pip install flask scikit-learn pandas numpy")
        return False

def start_web_interface():
    """Start the ultimate web interface"""
    print("🚀 STARTING ULTIMATE LEGAL AGENT WEB INTERFACE")
    print("=" * 70)
    print("✅ Handles ANY type of legal query (murder, kidnapping, etc.)")
    print("✅ ALL BNS, IPC, CrPC sections")
    print("✅ Feedback system that adjusts confidence")
    print("✅ Query storage and history")
    print("✅ Enhanced subdomain classification")
    print("=" * 70)
    
    # Check prerequisites
    if not check_python_version():
        return False
        
    if not check_dependencies():
        return False
    
    # Open browser after delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Browser opened at http://localhost:5000")
        except:
            print("📱 Please manually open: http://localhost:5000")
    
    Timer(3.0, open_browser).start()
    
    # Start the web interface
    try:
        subprocess.run([sys.executable, "ultimate_web_interface.py"], check=True)
        return True
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        print("💡 Try running 'python diagnose_and_start.py' for detailed diagnostics")
        return False

def main():
    """Main function"""
    print("🏛️ LAW AGENT BY GROK - WEB INTERFACE STARTER")
    print("=" * 70)
    
    success = start_web_interface()
    
    if not success:
        print("\n❌ Web interface failed to start")
        print("💡 Run 'python diagnose_and_start.py' for detailed diagnostics")
        sys.exit(1)
    else:
        print("\n✅ Web interface started successfully")

if __name__ == "__main__":
    main()