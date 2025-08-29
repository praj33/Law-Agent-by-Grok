#!/usr/bin/env python3
"""
Simple test to verify constitutional backing removal from terminal
"""

try:
    from cli_interface import LegalAgentCLI
    
    print("=== TESTING CONSTITUTIONAL BACKING REMOVAL ===")
    print()
    
    # Create CLI
    cli = LegalAgentCLI(use_adaptive=False)
    
    # Test query
    test_query = "my landlord is not returning my security deposit"
    print(f"Testing query: {test_query}")
    print("-" * 50)
    
    # Process the query
    cli.process_query(test_query)
    
    print("\n" + "=" * 50)
    print("✅ Test completed! Check the output above.")
    print("If constitutional backing was removed, you should NOT see:")
    print("  - '🏛️ Constitutional Backing:' section")
    print("  - Article references in the response")
    print("=" * 50)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()