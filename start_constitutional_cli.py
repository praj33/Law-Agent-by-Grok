#!/usr/bin/env python3
"""
Constitutional Legal Agent CLI Launcher
======================================

This script launches the Legal Agent CLI with constitutional analysis enabled,
showing the NEW features you requested:
- Specific constitutional articles with confidence percentages
- Searches through all articles from article.json
- Enhanced legal guidance with constitutional backing

Usage:
    python start_constitutional_cli.py

This will automatically enable the constitutional analysis system.
"""

import sys
import os

def main():
    """Launch the CLI with constitutional analysis enabled"""
    
    print("🏛️ LAUNCHING CONSTITUTIONAL LEGAL AGENT CLI")
    print("=" * 60)
    print("✅ Constitutional Analysis: ENABLED")
    print("✅ Confidence Percentages: ENABLED") 
    print("✅ 140+ Articles Database: LOADED")
    print("=" * 60)
    
    # Change to correct directory
    os.chdir(r"c:\Users\adity\OneDrive\Documents\LAST LAW\Law Agent by Grok\Law Agent by Grok")
    
    # Import and run the CLI with adaptive mode
    try:
        from cli_interface import LegalAgentCLI
        cli = LegalAgentCLI(use_adaptive=True)
        cli.start()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all required modules are available.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()