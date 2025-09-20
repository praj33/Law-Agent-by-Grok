"""
Test Script for Enhanced Structured Legal Agent
==============================================

This script demonstrates the new structured response format with:
1. Constitutional Articles
2. IPC Sections
3. CrPC Sections  
4. Special Acts

Author: Legal Agent Team
Date: 2025-01-XX
"""

from enhanced_structured_legal_agent import create_structured_legal_agent, get_structured_legal_advice

def test_structured_responses():
    """Test the structured response format with various legal queries"""
    
    print("🏛️ TESTING ENHANCED STRUCTURED LEGAL AGENT")
    print("=" * 70)
    print("Testing the new structured response format with Constitutional Articles,")
    print("IPC Sections, CrPC Sections, and Special Acts")
    print("=" * 70)
    
    # Create agent
    agent = create_structured_legal_agent()
    
    # Test cases covering different legal domains
    test_cases = [
        {
            "title": "Workplace Sexual Harassment",
            "query": "My male colleague is sexually harassing me at workplace and making inappropriate comments",
            "expected_domain": "employment_law"
        },
        {
            "title": "Domestic Violence Case", 
            "query": "My husband is beating me and threatening me with violence at home",
            "expected_domain": "family_law"
        },
        {
            "title": "Tenant Rights Issue",
            "query": "My landlord is not returning my security deposit even after 6 months of vacating",
            "expected_domain": "tenant_rights"
        },
        {
            "title": "Cyber Crime - Online Fraud",
            "query": "Someone hacked my bank account and transferred money through online fraud",
            "expected_domain": "cyber_crime"
        },
        {
            "title": "Criminal Case - Theft",
            "query": "Someone broke into my house and stole my jewelry and cash",
            "expected_domain": "criminal_law"
        },
        {
            "title": "Consumer Complaint",
            "query": "I bought a defective mobile phone and the company is refusing to replace it",
            "expected_domain": "consumer_complaint"
        },
        {
            "title": "Elder Abuse Case",
            "query": "My elderly father is being neglected and abused by his caretaker",
            "expected_domain": "elder_abuse"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST CASE {i}: {test_case['title']}")
        print(f"Query: \"{test_case['query']}\"")
        print(f"Expected Domain: {test_case['expected_domain']}")
        print('='*70)
        
        # Get structured response
        try:
            response = agent.process_structured_query(test_case['query'])
            
            # Display results
            print(f"✅ CLASSIFIED DOMAIN: {response.domain} (Confidence: {response.confidence:.2f})")
            print(f"📊 RESPONSE SUMMARY:")
            print(f"   • Constitutional Articles: {len(response.constitutional_articles)}")
            print(f"   • IPC Sections: {len(response.ipc_sections)}")
            print(f"   • CrPC Sections: {len(response.crpc_sections)}")
            print(f"   • Special Acts: {len(response.special_acts)}")
            
            # Show formatted response
            print(f"\n📋 FORMATTED RESPONSE:")
            print("-" * 50)
            formatted_response = response.to_formatted_response()
            print(formatted_response)
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        # Wait for user input to continue
        if i < len(test_cases):
            input(f"\n⏸️  Press Enter to continue to next test case...")
    
    print(f"\n🎉 ALL TESTS COMPLETED!")
    print(f"✅ Enhanced Structured Legal Agent is working properly")


def test_quick_function():
    """Test the quick advice function"""
    
    print(f"\n{'='*70}")
    print("🚀 TESTING QUICK STRUCTURED ADVICE FUNCTION")
    print('='*70)
    
    query = "My employer fired me without giving proper notice and is not paying my salary"
    
    print(f"Query: \"{query}\"")
    print(f"\nResponse:")
    print("-" * 50)
    
    try:
        advice = get_structured_legal_advice(query)
        print(advice)
        print(f"\n✅ Quick function working correctly!")
    except Exception as e:
        print(f"❌ ERROR in quick function: {e}")


def demonstrate_database_coverage():
    """Demonstrate the coverage of legal database"""
    
    print(f"\n{'='*70}")
    print("📊 LEGAL DATABASE COVERAGE DEMONSTRATION")
    print('='*70)
    
    agent = create_structured_legal_agent()
    
    print(f"📋 DATABASE STATISTICS:")
    print(f"   • IPC Sections: {len(agent.legal_db.ipc_sections)}")
    print(f"   • CrPC Sections: {len(agent.legal_db.crpc_sections)}")
    print(f"   • Special Acts: {len(agent.legal_db.special_acts)}")
    print(f"   • Domain Mappings: {len(agent.legal_db.domain_mappings)}")
    
    print(f"\n🎯 SUPPORTED LEGAL DOMAINS:")
    for domain in agent.legal_db.domain_mappings.keys():
        print(f"   • {domain.replace('_', ' ').title()}")
    
    print(f"\n📚 SAMPLE IPC SECTIONS:")
    sample_ipc = list(agent.legal_db.ipc_sections.items())[:5]
    for section_num, section_info in sample_ipc:
        print(f"   • Section {section_num}: {section_info['title']}")
    
    print(f"\n📚 SAMPLE SPECIAL ACTS:")
    sample_acts = list(agent.legal_db.special_acts.items())[:5]
    for act_key, act_info in sample_acts:
        print(f"   • {act_info['act_name']}")


if __name__ == "__main__":
    try:
        # Run all tests
        test_structured_responses()
        test_quick_function()
        demonstrate_database_coverage()
        
        print(f"\n🎊 ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print(f"🏛️ Enhanced Structured Legal Agent is ready for production use!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()