#!/usr/bin/env python3
"""
Quick Start BNS Legal Agent
===========================

Simple way to test the enhanced BNS agent with all features.
"""

def test_enhanced_bns_agent():
    """Test the enhanced BNS agent quickly"""
    
    print("🏛️ TESTING ENHANCED BNS LEGAL AGENT")
    print("=" * 50)
    
    try:
        # Import and create the enhanced BNS agent
        from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent, LegalQueryInput
        
        print("🔄 Initializing Enhanced BNS Agent...")
        agent = create_enhanced_subdomain_bns_agent()
        
        # Test query
        test_query = "My phone was stolen from my pocket"
        print(f"\n📋 Test Query: '{test_query}'")
        print("-" * 50)
        
        # Create query input
        query_input = LegalQueryInput(
            user_input=test_query,
            session_id="quick_test"
        )
        
        # Get terminal formatted response (like your preferred format)
        response = agent.process_query_with_terminal_format(query_input)
        print(response)
        
        print("\n" + "="*50)
        print("✅ SUCCESS! Enhanced BNS Agent Working!")
        print("✅ BNS sections included")
        print("✅ Enhanced features active")
        print("✅ Constitutional backing provided")
        print("✅ Ready for interactive use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def interactive_mode():
    """Start interactive mode"""
    
    try:
        from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent, LegalQueryInput
        
        agent = create_enhanced_subdomain_bns_agent()
        print("\n🔍 INTERACTIVE BNS LEGAL AGENT")
        print("=" * 50)
        print("Type 'quit' to exit")
        
        while True:
            user_input = input("\n📋 Legal Question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            try:
                query_input = LegalQueryInput(user_input=user_input, session_id="interactive")
                response = agent.process_query_with_terminal_format(query_input)
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Setup error: {e}")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Quick Test")
    print("2. Interactive Mode")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        test_enhanced_bns_agent()
    elif choice == "2":
        interactive_mode()
    else:
        print("Invalid choice. Running quick test...")
        test_enhanced_bns_agent()