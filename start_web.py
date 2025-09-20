#!/usr/bin/env python3
"""
Simple Web Interface Launcher
============================

Starts the web interface and automatically opens it in your browser.
"""

import sys
import time
import threading
import webbrowser
import subprocess
import os

def start_web_interface():
    """Start web interface and open browser"""
    print("🌐 Starting Legal Agent Web Interface...")
    print("=" * 50)
    
    # Function to open browser after delay
    def open_browser():
        time.sleep(3)  # Wait for server to start
        print("🚀 Opening browser...")
        webbrowser.open('http://localhost:5000')
    
    # Start browser opener in background
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start the web server
    try:
        print("📍 Server will be available at: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Try available web interfaces in order of preference
        web_files = [
            "ultimate_web_interface.py",
            "simple_web_interface.py", 
            "start_web_interface.py"
        ]
        
        for web_file in web_files:
            if os.path.exists(web_file):
                print(f"🎯 Starting {web_file}...")
                subprocess.run([sys.executable, web_file], check=True)
                break
        else:
            print("❌ No web interface files found!")
            print("💡 Available files:")
            for f in web_files:
                exists = "✅" if os.path.exists(f) else "❌"
                print(f"  {exists} {f}")
        
    except KeyboardInterrupt:
        print("\n👋 Web server stopped.")
    except FileNotFoundError:
        print("❌ web_interface.py not found!")
        print("💡 Make sure you're in the correct directory")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")

if __name__ == "__main__":
    start_web_interface()