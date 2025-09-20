#!/usr/bin/env python3
"""
Start Script for Legal AI Agent
===============================

This script starts the Legal AI Agent web interface.
"""

import sys
import os

def start_legal_ai_agent():
    """Start the Legal AI Agent web interface"""
    
    print("🚀 Starting Legal AI Agent...")
    print("=" * 50)
    
    try:
        # Import and run the web interface
        from legal_ai_web_interface import app
        app.run(debug=True, host='0.0.0.0', port=5001)
        
    except ImportError as e:
        print(f"❌ Failed to import Legal AI Agent components: {e}")
        print("💡 Make sure all required files are in the correct location:")
        print("   - legal_ai_agent.py")
        print("   - legal_ai_web_interface.py")
        print("   - templates/simple_index.html")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Failed to start Legal AI Agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_legal_ai_agent()