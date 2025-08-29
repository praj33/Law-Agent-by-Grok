"""
Complete System Test - Phone Theft Classification Fix
====================================================

This script tests the complete system to ensure that "My phone is stolen"
is now correctly classified as "criminal_law" through the entire pipeline.
"""

def test_complete_system():
    """Test the complete system with the phone theft query"""
    
    print("🔧 TESTING COMPLETE SYSTEM - PHONE THEFT CLASSIFICATION")
    print("=" * 70)
    
    # Test the exact query that was problematic
    test_query = "My phone is stolen"
    
    print(f"Testing query: \"{test_query}\"")
    print("-" * 50)
    
    # Test 1: ML Classifier directly
    print("1. Testing ML Classifier directly:")
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        domain, confidence, alternatives = classifier.classify_with_confidence(test_query)
        
        print(f"   Domain: {domain}")
        print(f"   Confidence: {confidence:.3f}")
        
        if domain == "criminal_law":
            print("   ✅ ML Classifier: CORRECT")
            ml_success = True
        else:
            print("   ❌ ML Classifier: INCORRECT")
            ml_success = False
            
    except Exception as e:
        print(f"   ❌ ML Classifier Error: {e}")
        ml_success = False
    
    print()
    
    # Test 2: Working Enhanced Agent
    print("2. Testing Working Enhanced Agent:")
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        response = agent.process_query(test_query)
        
        print(f"   Domain: {response.domain}")
        print(f"   Confidence: {response.confidence:.3f}")
        print(f"   Legal Route: {response.legal_route[:60]}...")
        
        if response.domain == "criminal_law":
            print("   ✅ Enhanced Agent: CORRECT")
            agent_success = True
        else:
            print("   ❌ Enhanced Agent: INCORRECT")
            agent_success = False
            
    except Exception as e:
        print(f"   ❌ Enhanced Agent Error: {e}")
        agent_success = False
    
    print()
    
    # Test 3: CLI Interface (if available)
    print("3. Testing CLI Interface:")
    try:
        from cli_interface import LegalAgentCLI
        cli = LegalAgentCLI()
        
        # Simulate processing the query
        print(f"   CLI initialized successfully")
        print("   ✅ CLI Interface: AVAILABLE")
        cli_success = True
        
    except Exception as e:
        print(f"   ⚠️  CLI Interface: {e}")
        cli_success = False
    
    print()
    
    # Final Results
    print("=" * 70)
    print("🏁 FINAL RESULTS:")
    print("-" * 30)
    
    if ml_success and agent_success:
        print("🎉 SUCCESS! Phone theft classification is now FIXED!")
        print("   ✅ ML Classifier correctly identifies as criminal_law")
        print("   ✅ Enhanced Agent correctly processes the query")
        print("   ✅ Your terminal should now work correctly!")
        
        print("\n💡 WHAT TO DO NEXT:")
        print("   1. Open your terminal/CLI")
        print("   2. Type: 'My phone is stolen'")
        print("   3. You should now see it classified as Criminal Law")
        
        return True
        
    elif ml_success:
        print("✅ ML Classifier is working correctly")
        print("⚠️  Enhanced Agent may have issues")
        print("   The core fix is working, but there may be integration issues")
        return False
        
    else:
        print("❌ System still has issues")
        print("   The fix may not be working properly")
        return False


def test_distinction():
    """Test that we can still distinguish between physical theft and cyber crimes"""
    
    print("\n🔍 TESTING PHYSICAL vs CYBER DISTINCTION:")
    print("-" * 50)
    
    test_cases = [
        ("My phone is stolen", "criminal_law"),
        ("My phone is being hacked", "cyber_crime"),
        ("Someone stole my phone", "criminal_law"),
        ("Phone hacked by cybercriminal", "cyber_crime"),
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
        
        if accuracy >= 75:
            print("✅ Good distinction between physical theft and cyber crimes")
            return True
        else:
            print("⚠️  Some confusion between physical theft and cyber crimes")
            return False
            
    except Exception as e:
        print(f"❌ Error testing distinction: {e}")
        return False


if __name__ == "__main__":
    print("🚀 COMPLETE SYSTEM TEST - PHONE THEFT CLASSIFICATION FIX")
    print("=" * 80)
    
    # Test complete system
    system_success = test_complete_system()
    
    # Test distinction
    distinction_success = test_distinction()
    
    print("\n" + "=" * 80)
    print("📋 SUMMARY:")
    
    if system_success and distinction_success:
        print("🎉 COMPLETE SUCCESS!")
        print("   Your phone theft classification issue is now FIXED!")
        print("   The system correctly distinguishes between physical theft and cyber crimes.")
        
    elif system_success:
        print("✅ MOSTLY SUCCESSFUL!")
        print("   Phone theft classification is fixed.")
        print("   Minor distinction issues may remain.")
        
    else:
        print("❌ ISSUES REMAIN")
        print("   Additional debugging may be needed.")
    
    print("\n💡 Try your terminal now with: 'My phone is stolen'")