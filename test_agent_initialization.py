#!/usr/bin/env python3
"""
Test Ultimate Legal Agent Initialization
========================================

This script tests if the ultimate legal agent can be properly initialized.
"""

import traceback
import sys
import os

def test_ultimate_agent():
    """Test if ultimate legal agent can be initialized"""
    print("🔍 Testing Ultimate Legal Agent Initialization")
    print("=" * 70)
    
    try:
        print("🔧 Importing ultimate_legal_agent module...")
        from ultimate_legal_agent import create_ultimate_legal_agent
        print("✅ Module imported successfully")
        
        print("🔧 Creating ultimate legal agent instance...")
        agent = create_ultimate_legal_agent()
        print("✅ Agent instance created successfully")
        
        print("🔧 Testing with a simple query...")
        response = agent.process_ultimate_query("test query")
        print("✅ Query processed successfully")
        print(f"📊 Response: {response['total_sections']} sections identified")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required files are in the directory:")
        print("   - ultimate_legal_agent.py")
        print("   - complete_legal_database.py")
        print("   - enhanced_subdomain_classifier.py")
        print("   - expanded_legal_domains.py")
        return False
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        print("📝 Full traceback:")
        traceback.print_exc()
        return False

def test_component_imports():
    """Test importing individual components"""
    print("🔍 Testing Individual Component Imports")
    print("=" * 70)
    
    components = [
        ("ultimate_legal_agent", "create_ultimate_legal_agent"),
        ("complete_legal_database", "create_complete_legal_database"),
        ("enhanced_subdomain_classifier", "create_enhanced_subdomain_classifier"),
        ("expanded_legal_domains", "create_expanded_legal_domains")
    ]
    
    all_good = True
    for module_name, function_name in components:
        print(f"🔧 Testing {module_name}...", end=" ")
        try:
            module = __import__(module_name)
            if hasattr(module, function_name):
                print("✅ OK")
            else:
                print(f"❌ Missing function {function_name}")
                all_good = False
        except ImportError as e:
            print(f"❌ Import failed - {str(e)}")
            all_good = False
        except Exception as e:
            print(f"❌ Error - {str(e)}")
            all_good = False
    
    return all_good

def main():
    """Main function"""
    print("🏛️ LAW AGENT BY GROK - AGENT INITIALIZATION TEST")
    print("=" * 70)
    
    # Test component imports
    components_ok = test_component_imports()
    print()
    
    if not components_ok:
        print("❌ Component import test failed. Cannot proceed with agent test.")
        return
    
    # Test agent initialization
    agent_ok = test_ultimate_agent()
    print()
    
    if agent_ok:
        print("🎉 All tests passed! The ultimate legal agent is working correctly.")
    else:
        print("❌ Agent initialization test failed.")
        print("💡 Try running 'python diagnose_and_start.py' for more detailed diagnostics.")

if __name__ == "__main__":
    main()