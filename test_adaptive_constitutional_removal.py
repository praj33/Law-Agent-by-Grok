#!/usr/bin/env python3
"""
Test adaptive agent structured output to verify constitutional backing removal
"""

try:
    from cli_interface import LegalAgentCLI
    
    print("=== TESTING ADAPTIVE AGENT CONSTITUTIONAL REMOVAL ===")
    print()
    
    # Test with adaptive agent
    try:
        cli = LegalAgentCLI(use_adaptive=True)
        print("✅ Using Adaptive Agent")
    except:
        cli = LegalAgentCLI(use_adaptive=False)
        print("⚠️ Fallback to Enhanced Agent")
    
    # Test query
    test_query = "my employer is not paying my salary"
    print(f"Testing query: {test_query}")
    print("-" * 60)
    
    # Process the query
    cli.process_query(test_query)
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("Constitutional backing should be REMOVED from output.")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()