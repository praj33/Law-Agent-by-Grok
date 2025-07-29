#!/usr/bin/env python3
"""
Quick Start Script for Enhanced Legal Agent
==========================================
"""

import sys
from pathlib import Path

def main():
    print("🏛️ ENHANCED LEGAL AGENT - QUICK START")
    print("=" * 50)
    
    # Check if setup was completed
    required_files = [
        'training_data.json',
        'legal_case_data.json',
        'domain_classifier_model.pkl'
    ]
    
    missing = [f for f in required_files if not Path(f).exists()]
    
    if missing:
        print("⚠️ System not fully initialized. Run setup first:")
        print("   python setup_enhanced_system.py")
        return
    
    print("✅ System initialized. Choose an interface:")
    print()
    print("1. 🌟 Enhanced Constitutional CLI (Recommended)")
    print("   python constitutional_cli.py")
    print()
    print("2. 🧠 Adaptive Learning CLI")
    print("   python adaptive_cli.py")
    print()
    print("3. 🧪 Run Comprehensive Tests")
    print("   python comprehensive_test_suite.py")
    print()
    
    choice = input("Enter choice (1-3) or press Enter for option 1: ").strip()
    
    if choice == "2":
        import subprocess
        subprocess.run([sys.executable, "adaptive_cli.py"])
    elif choice == "3":
        import subprocess
        subprocess.run([sys.executable, "comprehensive_test_suite.py"])
    else:
        import subprocess
        subprocess.run([sys.executable, "constitutional_cli.py"])

if __name__ == "__main__":
    main()
