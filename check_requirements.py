#!/usr/bin/env python3
"""
Check Requirements for Law Agent
================================

This script checks if all required dependencies are installed.
"""

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking Law Agent Requirements")
    print("=" * 70)
    
    required_packages = [
        ("Flask", "flask"),
        ("Scikit-learn", "sklearn"),
        ("Pandas", "pandas"),
        ("NumPy", "numpy"),
        ("Python-dateutil", "dateutil"),
        ("Requests", "requests")
    ]
    
    missing_packages = []
    
    for name, module in required_packages:
        print(f"🔍 Checking {name}...", end=" ")
        try:
            __import__(module)
            print("✅ OK")
        except ImportError:
            print("❌ MISSING")
            missing_packages.append((name, module))
    
    print("=" * 70)
    
    if missing_packages:
        print("❌ Missing packages detected:")
        for name, module in missing_packages:
            print(f"   - {name} ({module})")
        print("\n💡 Install missing packages with:")
        print("   pip install flask scikit-learn pandas numpy python-dateutil requests")
        return False
    else:
        print("✅ All required packages are installed!")
        return True

def check_optional_packages():
    """Check if optional packages are installed"""
    print("\n🔍 Checking Optional Packages")
    print("=" * 70)
    
    optional_packages = [
        ("spaCy", "spacy"),
        ("Streamlit", "streamlit")
    ]
    
    for name, module in optional_packages:
        print(f"🔍 Checking {name}...", end=" ")
        try:
            __import__(module)
            print("✅ OK")
        except ImportError:
            print("❌ Not installed (optional)")

if __name__ == "__main__":
    print("🏛️ LAW AGENT BY GROK - REQUIREMENTS CHECK")
    print("=" * 70)
    
    required_ok = check_requirements()
    check_optional_packages()
    
    if required_ok:
        print("\n🎉 All required requirements are satisfied!")
        print("💡 You can now run the Law Agent web interface.")
    else:
        print("\n❌ Some required packages are missing.")
        print("💡 Please install them before running the Law Agent.")