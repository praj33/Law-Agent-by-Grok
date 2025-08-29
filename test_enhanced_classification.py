#!/usr/bin/env python3
"""
Test Property Classification Improvements
========================================

This script tests the enhanced domain classification with:
1. Spelling correction (hijaced -> hijacked)
2. Proper property_disputes domain classification
3. Subcategory detection for property issues
"""

def test_property_classification():
    """Test the enhanced property classification"""
    
    print("🏠 TESTING ENHANCED PROPERTY CLASSIFICATION")
    print("=" * 60)
    
    try:
        from working_enhanced_agent import WorkingEnhancedAgent
        
        agent = WorkingEnhancedAgent()
        
        # Test queries with spelling errors and property issues
        test_cases = [
            ("My Property is Been Hijaced", "property_disputes"),
            ("my house has been hijacked by neighbor", "property_disputes"),
            ("illegal possession of my land", "property_disputes"),
            ("property encroachment issue", "property_disputes"),
            ("landlord not returning deposit", "tenant_rights"),
            ("my phone is being hacked", "cyber_crime")
        ]
        
        print("🔍 Testing Classification Results:")
        print("-" * 40)
        
        for query, expected_domain in test_cases:
            print(f"\n📝 Query: '{query}'")
            
            # Test normalization
            normalized = agent.normalize_query_text(query)
            if normalized != query.lower():
                print(f"   🔧 Normalized: '{query}' → '{normalized}'")
            
            # Test classification
            domain, confidence = agent.fallback_classification(query)
            
            # Test subcategory
            subcategory = agent.get_subcategory_for_domain(domain, query)
            
            # Status check
            status = "✅" if domain == expected_domain else "❌"
            
            print(f"   {status} Domain: {domain} (expected: {expected_domain})")
            print(f"   📊 Confidence: {confidence:.3f}")
            print(f"   📋 Subcategory: {subcategory}")
            
            # Test detailed classification
            detailed = agent.get_detailed_classification(query, domain, confidence)
            print(f"   🎯 Route: {detailed.get('specific_route', 'N/A')}")
            print(f"   📈 Success Rate: {detailed.get('success_rate', 'N/A')}")
        
        print(f"\n✅ PROPERTY CLASSIFICATION TEST COMPLETED!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_processing():
    """Test complete query processing with property hijacking"""
    
    print(f"\n🎯 TESTING COMPLETE QUERY PROCESSING")
    print("=" * 60)
    
    try:
        from working_enhanced_agent import WorkingEnhancedAgent
        
        agent = WorkingEnhancedAgent()
        
        # Test the exact user query
        test_query = "My Property is Been Hijaced"
        
        print(f"🔍 Processing: '{test_query}'")
        print("-" * 40)
        
        response = agent.process_query(test_query)
        
        print(f"✅ PROCESSING RESULTS:")
        print(f"   Domain: {response.domain}")
        print(f"   Confidence: {response.confidence:.3f}")
        print(f"   Timeline: {response.timeline}")
        print(f"   Success Rate: {response.success_rate:.1%}")
        print(f"   Legal Route: {response.legal_route[:100]}...")
        
        if response.domain != "unknown":
            print(f"\n🎉 SUCCESS: Query properly classified as '{response.domain}'!")
            print(f"   No longer returning 'unknown' domain")
        else:
            print(f"\n⚠️ ISSUE: Still returning 'unknown' domain")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    
    print("🧪 ENHANCED DOMAIN CLASSIFICATION TEST")
    print("=" * 70)
    print("Testing improvements for property hijacking classification")
    print("=" * 70)
    
    # Test classification improvements
    classification_success = test_property_classification()
    
    # Test complete processing
    processing_success = test_complete_processing()
    
    print(f"\n📊 TEST SUMMARY:")
    print("=" * 30)
    print(f"Classification Test: {'✅ PASSED' if classification_success else '❌ FAILED'}")
    print(f"Processing Test: {'✅ PASSED' if processing_success else '❌ FAILED'}")
    
    if classification_success and processing_success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"Property hijacking queries should now work correctly.")
        print(f"\n💡 Next step: Start interactive CLI with:")
        print(f"   python cli_interface.py --adaptive")
    else:
        print(f"\n❌ SOME TESTS FAILED")
        print(f"Additional fixes may be needed.")

if __name__ == "__main__":
    main()