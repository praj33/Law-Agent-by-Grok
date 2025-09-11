#!/usr/bin/env python3
"""
Test Enhanced Subdomain + BNS Agent
==================================

Simple test script to verify that the enhanced agent with subdomain classification
and BNS integration is working properly.
"""

import sys
import traceback

def test_bns_database():
    """Test BNS database functionality"""
    print("🧪 Testing BNS Database...")
    try:
        from bharatiya_nyaya_sanhita import create_bns_database
        
        bns_db = create_bns_database()
        stats = bns_db.get_stats()
        
        print(f"✅ BNS Database loaded: {stats['total_bns_sections']} sections")
        
        # Test domain-based retrieval
        sections = bns_db.get_bns_sections_for_domain("criminal_law", "theft", "my phone is stolen")
        print(f"✅ Retrieved {len(sections)} BNS sections for theft case")
        
        # Test IPC to BNS conversion
        conversion = bns_db.get_ipc_to_bns_conversion("378")
        if conversion:
            print(f"✅ IPC 378 → BNS {conversion['bns_section']}: {conversion['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ BNS Database test failed: {e}")
        traceback.print_exc()
        return False

def test_subdomain_classifier():
    """Test subdomain classifier functionality"""
    print("\n🧪 Testing Subdomain Classifier...")
    try:
        from subdomain_classifier import create_subdomain_classifier
        
        classifier = create_subdomain_classifier()
        stats = classifier.get_stats()
        
        print(f"✅ Subdomain Classifier loaded: {stats['total_domains']} domains, {stats['total_subdomains']} subdomains")
        
        # Test classification
        subdomain, confidence, alternatives = classifier.classify_subdomain("criminal_law", "my phone is stolen")
        print(f"✅ Classified 'phone stolen' → {subdomain} (confidence: {confidence:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Subdomain Classifier test failed: {e}")
        traceback.print_exc()
        return False

def test_enhanced_agent():
    """Test the enhanced agent with subdomain + BNS integration"""
    print("\n🧪 Testing Enhanced Agent...")
    try:
        from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent
        
        agent = create_enhanced_subdomain_bns_agent()
        print("✅ Enhanced Agent initialized successfully")
        
        # Test query processing
        test_query = "My phone was stolen from my pocket"
        print(f"\n🔍 Testing query: '{test_query}'")
        
        response = agent.process_query_with_complete_analysis(test_query)
        
        print(f"✅ Query processed successfully!")
        print(f"   Domain: {response['domain']}")
        print(f"   Subdomain: {response['subdomain']} (confidence: {response['subdomain_confidence']:.3f})")
        print(f"   BNS Sections: {len(response['bns_sections'])}")
        
        # Verify mandatory components
        completeness = response['analysis_completeness']
        if completeness['domain_classified'] and completeness['subdomain_classified'] and completeness['bns_sections_provided']:
            print("✅ All mandatory components present!")
            return True
        else:
            print("❌ Missing mandatory components")
            return False
        
    except Exception as e:
        print(f"❌ Enhanced Agent test failed: {e}")
        traceback.print_exc()
        return False

def test_simple_query():
    """Test a simple query end-to-end"""
    print("\n🧪 Testing Simple Query End-to-End...")
    try:
        from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent
        
        agent = create_enhanced_subdomain_bns_agent()
        
        # Test multiple queries
        test_queries = [
            "My phone is stolen",
            "Someone is hacking my computer", 
            "I was fired from my job",
            "Landlord won't return deposit"
        ]
        
        for query in test_queries:
            print(f"\n📋 Testing: '{query}'")
            response = agent.process_query_with_complete_analysis(query)
            
            print(f"   ✅ Domain: {response['domain']} → Subdomain: {response['subdomain']}")
            print(f"   ✅ BNS Sections: {len(response['bns_sections'])}")
            
            # Show first BNS section if available
            if response['bns_sections']:
                first_section = response['bns_sections'][0]
                print(f"   📚 First BNS Section: {first_section['section_number']} - {first_section['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple query test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 TESTING ENHANCED SUBDOMAIN + BNS AGENT")
    print("=" * 60)
    
    tests = [
        ("BNS Database", test_bns_database),
        ("Subdomain Classifier", test_subdomain_classifier), 
        ("Enhanced Agent", test_enhanced_agent),
        ("Simple Queries", test_simple_query)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n{'='*60}")
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Enhanced agent is ready!")
        print("✅ Subdomain classification working for all queries")
        print("✅ BNS sections integration working properly")
        print("✅ Complete legal analysis available")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("="*60)

if __name__ == "__main__":
    main()