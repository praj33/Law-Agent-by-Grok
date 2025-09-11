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
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start: {e}")

if __name__ == "__main__":
    start_web_interface()