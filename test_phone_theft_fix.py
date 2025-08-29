"""
Test Phone Theft Classification Fix
===================================

This script tests the specific issue where "My phone is stolen" 
was being classified as "cyber_crime" instead of "criminal_law".
"""

def test_phone_theft_classification():
    """Test phone theft queries to ensure they're classified as criminal_law"""
    
    print("🔧 TESTING PHONE THEFT CLASSIFICATION FIX")
    print("=" * 60)
    
    # Import the fixed ML classifier
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        print("✅ ML Classifier loaded successfully")
    except Exception as e:
        print(f"❌ Error loading ML classifier: {e}")
        return False
    
    # Test queries that should be classified as criminal_law
    phone_theft_queries = [
        "My phone is stolen",
        "My phone was stolen", 
        "Phone is stolen",
        "Someone stole my phone",
        "Phone stolen from me",
        "Phone theft incident",
        "Phone snatched by thief",
        "Phone stolen in market",
        "Phone stolen need police help",
        "Mobile is stolen",
        "Mobile was stolen",
        "Someone stole my mobile"
    ]
    
    print(f"\n🧪 Testing {len(phone_theft_queries)} phone theft queries:")
    print("-" * 50)
    
    correct_classifications = 0
    total_queries = len(phone_theft_queries)
    
    for query in phone_theft_queries:
        try:
            domain, confidence, alternatives = classifier.classify_with_confidence(query)
            
            # Check if classified correctly
            is_correct = domain == "criminal_law"
            status = "✅" if is_correct else "❌"
            
            if is_correct:
                correct_classifications += 1
            
            print(f"{status} \"{query}\"")
            print(f"    → Classified as: {domain} (confidence: {confidence:.3f})")
            
            if not is_correct:
                print(f"    → Expected: criminal_law")
                if alternatives:
                    print(f"    → Alternatives: {[f'{d}({c:.3f})' for d, c in alternatives[:3]]}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error classifying \"{query}\": {e}")
    
    # Calculate accuracy
    accuracy = (correct_classifications / total_queries) * 100
    
    print("=" * 60)
    print(f"📊 RESULTS:")
    print(f"   Correct Classifications: {correct_classifications}/{total_queries}")
    print(f"   Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 90:
        print(f"🎉 EXCELLENT! Phone theft classification is working correctly!")
        print(f"   Your terminal should now classify 'My phone is stolen' as criminal_law")
        return True
    elif accuracy >= 70:
        print(f"⚠️  GOOD: Most phone theft queries are classified correctly")
        print(f"   Some edge cases may still need improvement")
        return True
    else:
        print(f"❌ POOR: Phone theft classification needs more work")
        print(f"   The fix may not be working properly")
        return False


def test_cyber_vs_criminal_distinction():
    """Test that we can distinguish between cyber crimes and physical theft"""
    
    print("\n🔍 TESTING CYBER CRIME vs CRIMINAL LAW DISTINCTION")
    print("=" * 60)
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
    except Exception as e:
        print(f"❌ Error loading classifier: {e}")
        return False
    
    # Test cases with expected domains
    test_cases = [
        # Physical theft (should be criminal_law)
        ("My phone is stolen", "criminal_law"),
        ("Phone was stolen from me", "criminal_law"),
        ("Someone stole my phone", "criminal_law"),
        ("Phone theft in market", "criminal_law"),
        
        # Cyber crimes (should be cyber_crime)
        ("My phone is being hacked", "cyber_crime"),
        ("Phone being hacked and privacy violated", "cyber_crime"),
        ("Someone is hacking my phone", "cyber_crime"),
        ("Phone hacked by cybercriminal", "cyber_crime"),
    ]
    
    print(f"🧪 Testing {len(test_cases)} distinction cases:")
    print("-" * 50)
    
    correct = 0
    total = len(test_cases)
    
    for query, expected_domain in test_cases:
        try:
            domain, confidence, alternatives = classifier.classify_with_confidence(query)
            
            is_correct = domain == expected_domain
            status = "✅" if is_correct else "❌"
            
            if is_correct:
                correct += 1
            
            print(f"{status} \"{query}\"")
            print(f"    → Got: {domain} | Expected: {expected_domain}")
            print(f"    → Confidence: {confidence:.3f}")
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    accuracy = (correct / total) * 100
    
    print("=" * 60)
    print(f"📊 DISTINCTION TEST RESULTS:")
    print(f"   Correct: {correct}/{total}")
    print(f"   Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 80:
        print(f"🎉 EXCELLENT! Can distinguish between cyber crimes and physical theft!")
        return True
    else:
        print(f"⚠️  Needs improvement in distinguishing cyber vs physical crimes")
        return False


if __name__ == "__main__":
    print("🚀 PHONE THEFT CLASSIFICATION FIX TEST")
    print("=" * 70)
    
    # Test phone theft classification
    theft_success = test_phone_theft_classification()
    
    # Test cyber vs criminal distinction
    distinction_success = test_cyber_vs_criminal_distinction()
    
    print("\n" + "=" * 70)
    print("🏁 FINAL RESULTS:")
    
    if theft_success and distinction_success:
        print("🎉 SUCCESS! Phone theft classification is now fixed!")
        print("   'My phone is stolen' should now be classified as criminal_law")
        print("   The system can distinguish between physical theft and cyber crimes")
    elif theft_success:
        print("✅ Phone theft classification is working")
        print("⚠️  Some distinction issues may remain")
    else:
        print("❌ Phone theft classification still needs work")
        print("   Manual investigation may be needed")
    
    print("\n💡 TIP: Try running your terminal query again!")