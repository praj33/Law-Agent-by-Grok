"""
Debug Feedback Issue
===================

Debug the exact feedback issue that's occurring
"""

import sys
import importlib

def debug_feedback_issue():
    """Debug the feedback issue step by step"""
    
    print("🔍 DEBUGGING FEEDBACK ISSUE")
    print("=" * 50)
    
    try:
        # Force reload modules to avoid caching issues
        print("1. Reloading modules...")
        if 'working_enhanced_agent' in sys.modules:
            importlib.reload(sys.modules['working_enhanced_agent'])
        if 'cli_interface' in sys.modules:
            importlib.reload(sys.modules['cli_interface'])
        print("   ✅ Modules reloaded")
        
        # Test direct agent creation
        print("2. Testing direct agent creation...")
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        print("   ✅ Agent created successfully")
        
        # Check if method exists
        print("3. Checking for process_feedback method...")
        has_method = hasattr(agent, 'process_feedback')
        print(f"   {'✅' if has_method else '❌'} Has process_feedback: {has_method}")
        
        if has_method:
            print("4. Testing process_feedback method...")
            agent.process_feedback("test query", "tenant_rights", 0.8, "helpful")
            print("   ✅ process_feedback method works")
        else:
            print("4. ❌ process_feedback method missing!")
            methods = [m for m in dir(agent) if not m.startswith('_')]
            print(f"   Available methods: {methods}")
        
        # Test CLI creation
        print("5. Testing CLI creation...")
        from cli_interface import LegalAgentCLI
        cli = LegalAgentCLI()
        print("   ✅ CLI created successfully")
        
        # Check CLI agent
        print("6. Checking CLI agent...")
        cli_has_method = hasattr(cli.agent, 'process_feedback')
        print(f"   {'✅' if cli_has_method else '❌'} CLI agent has process_feedback: {cli_has_method}")
        
        if cli_has_method:
            print("7. Testing CLI feedback processing...")
            # Simulate a query first
            cli.last_query = "test query"
            cli.last_response = cli.agent.process_query("test query")
            
            # Test feedback
            cli.process_feedback("helpful")
            print("   ✅ CLI feedback processing works")
        else:
            print("7. ❌ CLI agent missing process_feedback method!")
            cli_methods = [m for m in dir(cli.agent) if not m.startswith('_')]
            print(f"   CLI agent methods: {cli_methods}")
            
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main debug function"""
    
    print("🏛️ FEEDBACK ISSUE DEBUG")
    print("=" * 40)
    
    debug_feedback_issue()

if __name__ == "__main__":
    main()
