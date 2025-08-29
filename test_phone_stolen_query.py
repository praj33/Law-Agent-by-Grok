"""
Test Phone Stolen Query
======================

This script tests the specific query "phone stolen" to ensure
it's correctly classified as criminal_law instead of cyber_crime.
"""

def test_phone_stolen_query():
    """Test the phone stolen query comprehensively"""
    
    print("📱 TESTING 'PHONE STOLEN' QUERY")
    print("=" * 50)
    
    # Test query variations
    test_queries = [
        "phone stolen",
        "my phone stolen", 
        "phone is stolen",
        "phone was stolen",
        "someone stole phone",
        "phone stolen from me"
    ]
    
    print("🧪 Testing ML Classifier directly:")
    print("-" * 40)
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        
        correct_count = 0
        total_count = len(test_queries)
        
        for query in test_queries:
            domain, confidence, alternatives = classifier.classify_with_confidence(query)
            
            is_correct = domain == "criminal_law"
            status = "✅" if is_correct else "❌"
            
            if is_correct:
                correct_count += 1
            
            print(f"{status} \"{query}\" → {domain} (confidence: {confidence:.3f})")
        
        accuracy = (correct_count / total_count) * 100
        print(f"\n📊 ML Classifier Accuracy: {correct_count}/{total_count} ({accuracy:.1f}%)")
        
        ml_success = accuracy >= 80
        
    except Exception as e:
        print(f"❌ ML Classifier Error: {e}")
        ml_success = False
    
    print("\n🤖 Testing Working Enhanced Agent:")
    print("-" * 40)
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        
        # Test the main query
        main_query = "phone stolen"
        response = agent.process_query(main_query)
        
        print(f"\nQuery: \"{main_query}\"")
        print(f"Domain: {response.domain}")
        print(f"Confidence: {response.confidence:.3f}")
        print(f"Legal Route: {response.legal_route[:60]}...")
        print(f"Timeline: {response.timeline}")
        
        agent_success = response.domain == "criminal_law"
        
        if agent_success:
            print("✅ Enhanced Agent: CORRECT")
        else:
            print("❌ Enhanced Agent: INCORRECT")
            
    except Exception as e:
        print(f"❌ Enhanced Agent Error: {e}")
        agent_success = False
    
    print("\n🖥️  Testing CLI Interface:")
    print("-" * 40)
    
    try:
        from cli_interface import LegalAgentCLI
        cli = LegalAgentCLI(use_adaptive=False)
        
        # Simulate CLI processing
        test_query = "phone stolen"
        cli.process_query(test_query)
        
        if hasattr(cli, 'last_response') and cli.last_response:
            cli_domain = cli.last_response.domain
            cli_confidence = cli.last_response.confidence
            
            print(f"CLI Result: {cli_domain} (confidence: {cli_confidence:.3f})")
            
            cli_success = cli_domain == "criminal_law"
            
            if cli_success:
                print("✅ CLI Interface: CORRECT")
            else:
                print("❌ CLI Interface: INCORRECT")
        else:
            print("⚠️  Could not access CLI response")
            cli_success = False
            
    except Exception as e:
        print(f"❌ CLI Interface Error: {e}")
        cli_success = False
    
    # Final Results
    print("\n" + "=" * 50)
    print("🏁 FINAL TEST RESULTS:")
    print("-" * 30)
    
    if ml_success and agent_success and cli_success:
        print("🎉 COMPLETE SUCCESS!")
        print("   ✅ ML Classifier: Working")
        print("   ✅ Enhanced Agent: Working") 
        print("   ✅ CLI Interface: Working")
        print("\n💡 'phone stolen' is now correctly classified as Criminal Law!")
        return True
        
    elif ml_success and agent_success:
        print("✅ MOSTLY SUCCESSFUL!")
        print("   ✅ ML Classifier: Working")
        print("   ✅ Enhanced Agent: Working")
        print("   ⚠️  CLI Interface: May have issues")
        return True
        
    else:
        print("❌ ISSUES DETECTED:")
        print(f"   ML Classifier: {'✅' if ml_success else '❌'}")
        print(f"   Enhanced Agent: {'✅' if agent_success else '❌'}")
        print(f"   CLI Interface: {'✅' if cli_success else '❌'}")
        return False


def test_distinction():
    """Test that we can distinguish phone theft from phone hacking"""
    
    print("\n🔍 TESTING PHONE THEFT vs PHONE HACKING DISTINCTION:")
    print("-" * 60)
    
    test_cases = [
        # Physical theft (should be criminal_law)
        ("phone stolen", "criminal_law"),
        ("my phone stolen", "criminal_law"),
        ("phone is stolen", "criminal_law"),
        ("someone stole my phone", "criminal_law"),
        
        # Digital crimes (should be cyber_crime)
        ("phone hacked", "cyber_crime"),
        ("my phone is hacked", "cyber_crime"),
        ("phone being hacked", "cyber_crime"),
        ("someone hacked my phone", "cyber_crime"),
    ]
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        
        correct = 0
        total = len(test_cases)
        
        for query, expected in test_cases:
            domain, confidence, _ = classifier.classify_with_confidence(query)
            is_correct = domain == expected
            status = "✅" if is_correct else "❌"
            
            if is_correct:
                correct += 1
            
            print(f"{status} \"{query}\" → {domain} (expected: {expected})")
        
        accuracy = (correct / total) * 100
        print(f"\nDistinction Accuracy: {correct}/{total} ({accuracy:.1f}%)")
        
        return accuracy >= 75
        
    except Exception as e:
        print(f"❌ Error testing distinction: {e}")
        return False


if __name__ == "__main__":
    print("🚀 COMPREHENSIVE PHONE STOLEN QUERY TEST")
    print("=" * 70)
    
    # Test main functionality
    main_success = test_phone_stolen_query()
    
    # Test distinction capability
    distinction_success = test_distinction()
    
    print("\n" + "=" * 70)
    print("📋 OVERALL SUMMARY:")
    
    if main_success and distinction_success:
        print("🎉 EXCELLENT! Phone stolen classification is working perfectly!")
        print("   Your system correctly handles both physical theft and cyber crimes.")
        
    elif main_success:
        print("✅ GOOD! Phone stolen classification is working.")
        print("   Minor distinction issues may exist but core functionality works.")
        
    else:
        print("❌ ISSUES REMAIN with phone stolen classification.")
        print("   Additional debugging may be needed.")
    
    print("\n💡 Try in your terminal:")
    print("   python cli_interface.py")
    print("   Then type: phone stolen")
    print("   Should show: Criminal Law")