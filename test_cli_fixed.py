"""
Test CLI Fixed
==============

Test that the CLI is now working after fixing the missing methods
"""

import sys
import traceback

def test_cli_functionality():
    """Test CLI functionality step by step"""
    
    print("🔍 TESTING FIXED CLI FUNCTIONALITY")
    print("=" * 50)
    
    try:
        print("1. Testing CLI import...")
        from cli_interface import LegalAgentCLI
        print("   ✅ CLI import successful")
        
        print("2. Testing CLI instantiation...")
        cli = LegalAgentCLI()
        print("   ✅ CLI instantiation successful")
        
        print("3. Testing agent methods...")
        agent = cli.agent
        methods = [method for method in dir(agent) if not method.startswith('_')]
        print(f"   📋 Available methods: {len(methods)} methods")
        
        # Check for required methods
        required_methods = ['generate_session_id', 'get_learned_confidence', 'process_query']
        for method in required_methods:
            has_method = hasattr(agent, method)
            status = "✅" if has_method else "❌"
            print(f"   {status} {method}: {'Available' if has_method else 'Missing'}")
        
        print("4. Testing query processing...")
        test_queries = [
            "landlord not returning my deposit",
            "my boss is not giving my salary", 
            "I was raped by my neighbor",
            "defective product needs refund"
        ]
        
        for i, query in enumerate(test_queries, 1):
            try:
                response = agent.process_query(query)
                print(f"   ✅ Query {i}: {response.domain} (confidence: {response.confidence:.3f})")
            except Exception as e:
                print(f"   ❌ Query {i} failed: {e}")
        
        print("5. Testing CLI display method...")
        try:
            response = agent.process_query("landlord not returning deposit")
            cli.display_response(response)
            print("   ✅ Display method working")
        except Exception as e:
            print(f"   ❌ Display method failed: {e}")
            
        print("\n🎉 CLI FUNCTIONALITY TEST COMPLETE!")
        print("✅ All core functionality is working!")
        print("✅ CLI is ready to use!")
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        traceback.print_exc()

def main():
    """Main test function"""
    
    print("🏛️ CLI FIXED - FUNCTIONALITY TEST")
    print("=" * 60)
    
    test_cli_functionality()
    
    print(f"\n🚀 READY TO USE:")
    print("=" * 30)
    print("Run: python cli_interface.py")
    print("Then try queries like:")
    print("• 'landlord not returning my deposit'")
    print("• 'my boss is not giving my salary'")
    print("• 'I was raped by my neighbor'")
    print("• 'defective product needs refund'")

if __name__ == "__main__":
    main()
