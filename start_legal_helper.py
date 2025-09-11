#!/usr/bin/env python3
"""
Start Simple Legal Helper
========================
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Timer

def start_legal_helper():
    """Start the simple legal helper web interface"""
    print("🚀 STARTING LEGAL HELPER")
    print("=" * 50)
    print("✅ Simple and easy to use")
    print("✅ Complete legal guidance")
    print("✅ No complicated features")
    print("✅ Just ask your question!")
    print("=" * 50)
    
    # Open browser after delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Legal Helper opened in your browser")
        except:
            print("📱 Please open: http://localhost:5000")
    
    Timer(3.0, open_browser).start()
    
    # Start the web interface
    try:
        subprocess.run([sys.executable, "simple_web_interface.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Legal Helper stopped")
    except Exception as e:
        print(f"❌ Failed to start: {e}")

if __name__ == "__main__":
    start_legal_helper()