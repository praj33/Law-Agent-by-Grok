#!/usr/bin/env python3
"""
Start Enhanced Legal Agent Web Interface
======================================

Quick startup script for the enhanced web interface with complete legal analysis.
Access URL: http://localhost:5000
"""

import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_files = [
        'final_enhanced_legal_agent.py',
        'comprehensive_legal_sections.py',
        'subdomain_classifier.py',
        'enhanced_web_interface.py',
        'templates/final_enhanced_index.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    print("✅ All required files found")
    return True

def check_python_packages():
    """Check if required Python packages are installed"""
    print("🔍 Checking Python packages...")
    
    required_packages = ['flask', 'sklearn', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages available")
    return True

def open_browser():
    """Open browser after a delay"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Browser opened at http://localhost:5000")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("��� Please manually open: http://localhost:5000")

def start_web_interface():
    """Start the enhanced web interface"""
    print("🚀 STARTING ENHANCED LEGAL AGENT WEB INTERFACE")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start - missing required files")
        input("Press Enter to exit...")
        return
    
    if not check_python_packages():
        print("\n❌ Cannot start - missing required packages")
        input("Press Enter to exit...")
        return
    
    print("\n🔧 Starting web server...")
    print("📱 Access URL: http://localhost:5000")
    print("🔗 Features available:")
    print("   ✅ Subdomain classification for ALL queries")
    print("   ✅ BNS sections for ALL queries")
    print("   ✅ IPC sections for ALL queries")
    print("   ✅ CrPC sections for ALL queries")
    print("   ✅ Constitutional backing")
    print("   ✅ Complete legal analysis")
    print("\n⏳ Initializing system components...")
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    try:
        # Start the web interface
        import enhanced_web_interface
        print("\n🎉 Web interface started successfully!")
        print("🌐 Access at: http://localhost:5000")
        print("⏹️ Press Ctrl+C to stop the server")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start web interface: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure all required files are present")
        print("   2. Check that port 5000 is not in use")
        print("   3. Verify Python packages are installed")
        input("\nPress Enter to exit...")

def main():
    """Main function"""
    try:
        start_web_interface()
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()