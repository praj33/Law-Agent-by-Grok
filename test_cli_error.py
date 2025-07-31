"""
Test CLI Error
==============

Simple test to identify the CLI error
"""

import sys
import traceback

def test_cli_import():
    """Test CLI import step by step"""
    
    print("🔍 Testing CLI import step by step...")
    
    try:
        print("1. Testing basic imports...")
        import sys
        import json
        from typing import Optional
        print("   ✅ Basic imports successful")
        
        print("2. Testing legal_agent import...")
        try:
            from legal_agent import LegalAgent, LegalQueryInput, create_legal_agent
            print("   ✅ legal_agent import successful")
        except Exception as e:
            print(f"   ❌ legal_agent import failed: {e}")
        
        print("3. Testing adaptive_legal_agent import...")
        try:
            from adaptive_legal_agent import create_adaptive_legal_agent
            print("   ✅ adaptive_legal_agent import successful")
        except Exception as e:
            print(f"   ❌ adaptive_legal_agent import failed: {e}")
        
        print("4. Testing working_enhanced_agent import...")
        try:
            from working_enhanced_agent import create_working_enhanced_agent
            print("   ✅ working_enhanced_agent import successful")
        except Exception as e:
            print(f"   ❌ working_enhanced_agent import failed: {e}")
            traceback.print_exc()
        
        print("5. Testing CLI class import...")
        try:
            from cli_interface import LegalAgentCLI
            print("   ✅ CLI class import successful")
        except Exception as e:
            print(f"   ❌ CLI class import failed: {e}")
            traceback.print_exc()
        
        print("6. Testing CLI instantiation...")
        try:
            from cli_interface import LegalAgentCLI
            cli = LegalAgentCLI()
            print("   ✅ CLI instantiation successful")
        except Exception as e:
            print(f"   ❌ CLI instantiation failed: {e}")
            traceback.print_exc()
        
        print("7. Testing agent query processing...")
        try:
            from cli_interface import LegalAgentCLI
            cli = LegalAgentCLI()
            response = cli.agent.process_query("test query")
            print(f"   ✅ Query processing successful: {response.domain}")
        except Exception as e:
            print(f"   ❌ Query processing failed: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Overall test failed: {e}")
        traceback.print_exc()

def test_working_agent_directly():
    """Test working agent directly"""
    
    print("\n🔍 Testing working agent directly...")
    
    try:
        print("1. Creating working enhanced agent...")
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        print("   ✅ Agent created successfully")
        
        print("2. Checking agent methods...")
        methods = [method for method in dir(agent) if not method.startswith('_')]
        print(f"   📋 Available methods: {methods}")
        
        print("3. Checking for generate_session_id...")
        has_method = hasattr(agent, 'generate_session_id')
        print(f"   🔍 Has generate_session_id: {has_method}")
        
        if has_method:
            print("4. Testing generate_session_id...")
            session_id = agent.generate_session_id()
            print(f"   ✅ Session ID generated: {session_id}")
        else:
            print("4. ❌ generate_session_id method missing!")
        
        print("5. Testing process_query...")
        response = agent.process_query("landlord not returning deposit")
        print(f"   ✅ Query processed: {response.domain}")
        
    except Exception as e:
        print(f"❌ Working agent test failed: {e}")
        traceback.print_exc()

def main():
    """Main test function"""
    
    print("🏛️ CLI ERROR DIAGNOSIS")
    print("=" * 50)
    
    test_cli_import()
    test_working_agent_directly()
    
    print("\n🎯 DIAGNOSIS COMPLETE")
    print("=" * 30)

if __name__ == "__main__":
    main()
