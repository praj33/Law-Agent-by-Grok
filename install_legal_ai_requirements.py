#!/usr/bin/env python3
"""
Install Legal AI Agent Requirements
==================================

This script installs the required packages for the Legal AI Agent.
"""

import subprocess
import sys

def install_requirements():
    """Install the required packages"""
    try:
        # Install requirements from requirements_legal_ai.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_legal_ai.txt"])
        print("✅ All requirements installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)
        
    except FileNotFoundError:
        print("❌ requirements_legal_ai.txt not found. Please make sure it exists in the current directory.")
        sys.exit(1)

if __name__ == "__main__":
    print("📦 Installing Legal AI Agent Requirements...")
    print("=" * 50)
    install_requirements()