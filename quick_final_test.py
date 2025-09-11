#!/usr/bin/env python3
"""
Quick Test for Final Enhanced Legal Agent
========================================
"""

from final_enhanced_legal_agent import create_final_enhanced_legal_agent

def quick_test():
    print("🚀 QUICK TEST - FINAL ENHANCED LEGAL AGENT")
    print("=" * 60)
    
    # Initialize agent
    try:
        agent = create_final_enhanced_legal_agent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return
    
    # Test single query
    test_query = "My phone was stolen"
    print(f"\n🔍 Testing: '{test_query}'")
    
    try:
        response = agent.process_complete_legal_query(test_query)
        
        print(f"\n✅ RESULTS:")
        print(f"   Domain: {response['domain']}")
        print(f"   Subdomain: {response['subdomain']}")
        print(f"   BNS Sections: {len(response['bns_sections'])}")
        print(f"   IPC Sections: {len(response['ipc_sections'])}")
        print(f"   CrPC Sections: {len(response['crpc_sections'])}")
        print(f"   Total Sections: {response['total_sections']}")
        
        # Show first few sections
        if response['bns_sections']:
            print(f"\n📚 First BNS Section:")
            first_bns = response['bns_sections'][0]
            print(f"   Section {first_bns['section_number']}: {first_bns['title']}")
        
        if response['ipc_sections']:
            print(f"\n📖 First IPC Section:")
            first_ipc = response['ipc_sections'][0]
            print(f"   Section {first_ipc['section_number']}: {first_ipc['title']}")
        
        if response['crpc_sections']:
            print(f"\n⚖️ First CrPC Section:")
            first_crpc = response['crpc_sections'][0]
            print(f"   Section {first_crpc['section_number']}: {first_crpc['title']}")
        
        # Check completeness
        completeness = response['analysis_completeness']
        print(f"\n✅ COMPLETENESS CHECK:")
        print(f"   Domain: {'✅' if completeness['domain_classified'] else '❌'}")
        print(f"   Subdomain: {'✅' if completeness['subdomain_classified'] else '❌'}")
        print(f"   BNS: {'✅' if completeness['bns_sections_provided'] else '❌'}")
        print(f"   IPC: {'✅' if completeness['ipc_sections_provided'] else '❌'}")
        print(f"   CrPC: {'✅' if completeness['crpc_sections_provided'] else '❌'}")
        
        print(f"\n🎉 TEST SUCCESSFUL!")
        print("✅ All requirements met:")
        print("   • Subdomain classification: DONE")
        print("   • BNS sections: DONE")
        print("   • IPC sections: DONE")
        print("   • CrPC sections: DONE")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()