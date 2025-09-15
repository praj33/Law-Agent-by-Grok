#!/usr/bin/env python3
"""
Diagnose and Start Ultimate Legal Agent Web Interface
=====================================================

This script will diagnose potential issues with the legal agent components
before starting the web interface.
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Timer
import importlib.util

def check_component(component_name, file_path):
    """Check if a component can be imported"""
    print(f"🔍 Checking {component_name}...", end=" ")
    try:
        spec = importlib.util.spec_from_file_location(component_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ OK")
            return True
        else:
            print("❌ FAILED - Could not load module")
            return False
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        return False

def diagnose_components():
    """Diagnose all required components"""
    print("🔧 DIAGNOSING ULTIMATE LEGAL AGENT COMPONENTS")
    print("=" * 70)
    
    components = [
        ("Ultimate Legal Agent", "ultimate_legal_agent.py"),
        ("Complete Legal Database", "complete_legal_database.py"),
        ("Enhanced Subdomain Classifier", "enhanced_subdomain_classifier.py"),
        ("Expanded Legal Domains", "expanded_legal_domains.py")
    ]
    
    all_good = True
    for name, file_path in components:
        if not os.path.exists(file_path):
            print(f"❌ MISSING - {name} ({file_path}) not found")
            all_good = False
            continue
            
        if not check_component(name, file_path):
            all_good = False
    
    print("=" * 70)
    return all_good

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔧 CHECKING DEPENDENCIES")
    print("=" * 70)
    
    dependencies = [
        ("Flask", "flask"),
        ("Scikit-learn", "sklearn"),
        ("Pandas", "pandas"),
        ("NumPy", "numpy")
    ]
    
    all_good = True
    for name, module in dependencies:
        print(f"🔍 Checking {name}...", end=" ")
        try:
            __import__(module)
            print("✅ OK")
        except ImportError as e:
            print(f"❌ MISSING - {str(e)}")
            all_good = False
    
    print("=" * 70)
    return all_good

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

def main():
    """Main function"""
    print("🏛️ LAW AGENT BY GROK - DIAGNOSTIC STARTUP")
    print("=" * 70)
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        print("❌ Some dependencies are missing. Please install them:")
        print("   pip install flask scikit-learn pandas numpy")
        return
    
    # Check components
    components_ok = diagnose_components()
    if not components_ok:
        print("❌ Some components failed to load. Please check the errors above.")
        print("💡 Try reinstalling or regenerating the missing components.")
        return
    
    print("✅ All components and dependencies are OK!")
    print("")
    
    # Ask user if they want to start the server
    try:
        response = input("Do you want to start the web interface? (y/N): ")
        if response.lower() in ['y', 'yes']:
            start_web_interface()
        else:
            print("👋 Goodbye!")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()