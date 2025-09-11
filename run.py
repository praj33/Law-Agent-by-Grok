#!/usr/bin/env python3
"""
Legal Agent Launcher
===================

Simple launcher script to run the Legal Agent project.
Replaces all the complex batch files with a clean Python interface.

Usage:
    python run.py                    # Interactive CLI (default)
    python run.py --web              # Web interface
    python run.py --api              # FastAPI server
    python run.py --test             # Run tests
    python run.py --help             # Show help
"""

import sys
import os
import subprocess
import argparse

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("🏛️  LEGAL AGENT BY GROK")
    print("=" * 60)
    print("✅ Enhanced Legal Assistant with Constitutional Analysis")
    print("✅ 10+ Legal Domains | ML Classification | Real-time Processing")
    print("🌐 Modern Web Interface | Interactive CLI | FastAPI Backend")
    print("=" * 60)

def run_cli():
    """Run the interactive CLI interface"""
    print("🔧 Starting Interactive CLI...")
    print("💡 Try: 'Employee discloses company secrets' or 'Landlord won't return deposit'")
    print()
    
    try:
        subprocess.run([sys.executable, "cli_interface.py", "--adaptive"], check=True)
    except FileNotFoundError:
        print("❌ cli_interface.py not found. Trying alternative...")
        try:
            subprocess.run([sys.executable, "enhanced_cli.py"], check=True)
        except FileNotFoundError:
            print("❌ No CLI interface found. Please check your installation.")

def run_web():
    """Run the web interface"""
    print("🌐 Starting Web Interface...")
    print("📍 Access at: http://localhost:5000")
    print("🚀 Browser will open automatically...")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    # Available web interfaces in order of preference
    web_interfaces = [
        ("start_ultimate_web.py", "Ultimate Web Interface (Full Features)"),
        ("ultimate_web_interface.py", "Ultimate Web Interface (Direct)"),
        ("simple_web_interface.py", "Simple Web Interface"),
        ("start_web_interface.py", "Standard Web Interface")
    ]
    
    for web_file, description in web_interfaces:
        if os.path.exists(web_file):
            try:
                print(f"🎯 Using: {description}")
                subprocess.run([sys.executable, web_file], check=True)
                break
            except FileNotFoundError:
                print(f"❌ {web_file} not found, trying next...")
                continue
            except KeyboardInterrupt:
                print("\n👋 Web server stopped.")
                break
    else:
        print("❌ No web interface files found. Available files:")
        for web_file, desc in web_interfaces:
            exists = "✅" if os.path.exists(web_file) else "❌"
            print(f"  {exists} {web_file} - {desc}")

def run_api():
    """Run the FastAPI server"""
    print("🚀 Starting FastAPI Server...")
    print("📍 API docs at: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    try:
        # Try uvicorn first
        subprocess.run(["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"], check=True)
    except FileNotFoundError:
        print("❌ uvicorn not found. Trying direct FastAPI...")
        try:
            subprocess.run([sys.executable, "main.py"], check=True)
        except FileNotFoundError:
            print("❌ main.py not found. Please check your installation.")
    except KeyboardInterrupt:
        print("\n👋 API server stopped.")

def run_tests():
    """Run the test suite"""
    print("🧪 Running Tests...")
    print()
    
    test_files = [
        "test_all_improvements.py",
        "test_curated_system.py", 
        "final_comprehensive_test.py",
        "simple_test.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"▶️  Running {test_file}...")
            try:
                subprocess.run([sys.executable, test_file], check=True)
                print(f"✅ {test_file} completed")
            except subprocess.CalledProcessError:
                print(f"❌ {test_file} failed")
            print("-" * 40)
        else:
            print(f"���️  {test_file} not found, skipping...")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please check requirements.txt")
    except FileNotFoundError:
        print("❌ requirements.txt not found.")

def show_help():
    """Show help information"""
    print(__doc__)
    print("\nAvailable Commands:")
    print("  python run.py           # Interactive CLI (recommended)")
    print("  python run.py --web     # Web interface at localhost:5000") 
    print("  python run.py --api     # FastAPI server at localhost:8000")
    print("  python run.py --test    # Run test suite")
    print("  python run.py --install # Install dependencies")
    print("  python run.py --help    # Show this help")
    print()
    print("Quick Start:")
    print("1. python run.py --install  # First time setup")
    print("2. python run.py            # Start using the agent")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Legal Agent Launcher")
    parser.add_argument("--web", action="store_true", help="Run web interface")
    parser.add_argument("--api", action="store_true", help="Run FastAPI server")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--help-full", action="store_true", help="Show detailed help")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.help_full:
        show_help()
    elif args.install:
        install_dependencies()
    elif args.web:
        run_web()
    elif args.api:
        run_api()
    elif args.test:
        run_tests()
    else:
        # Default: run CLI
        run_cli()

if __name__ == "__main__":
    main()