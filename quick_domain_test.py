"""
Quick Domain Classification Test
===============================

Test basic queries to see if domain classification is working correctly.
"""

def test_basic_domains():
    """Test basic domain classification"""
    
    print("🔍 QUICK DOMAIN CLASSIFICATION TEST")
    print("=" * 50)
    
    # Test basic queries that should work
    test_queries = [
        ("My phone is stolen", "criminal_law"),
        ("My landlord won't return deposit", "tenant_rights"),
        ("I was fired from work", "employment_law"),
        ("My visa is expired", "immigration_law"),
        ("I want divorce", "family_law"),
        ("Defective product", "consumer_complaint"),
        ("Phone is hacked", "cyber_crime")
    ]
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        
        correct = 0
        total = len(test_queries)
        
        for query, expected_domain in test_queries:
            try:
                response = agent.process_query(query)
                actual_domain = response.domain
                
                is_correct = actual_domain == expected_domain
                status = "✅" if is_correct else "❌"
                
                if is_correct:
                    correct += 1
                
                print(f"{status} \"{query}\" → {actual_domain} (expected: {expected_domain})")
                
            except Exception as e:
                print(f"❌ Error with \"{query}\": {e}")
        
        accuracy = (correct / total) * 100
        print(f"\n📊 Overall Accuracy: {correct}/{total} ({accuracy:.1f}%)")
        
        if accuracy >= 80:
            print("✅ Domain classification is working well!")
            return True
        else:
            print("❌ Domain classification has issues!")
            return False
            
    except Exception as e:
        print(f"❌ Agent Error: {e}")
        return False


def test_ml_classifier_directly():
    """Test ML classifier directly"""
    
    print("\n🤖 TESTING ML CLASSIFIER DIRECTLY")
    print("=" * 50)
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        
        test_queries = [
            ("My phone is stolen", "criminal_law"),
            ("My landlord won't return deposit", "tenant_rights"),
            ("I was fired from work", "employment_law")
        ]
        
        correct = 0
        total = len(test_queries)
        
        for query, expected in test_queries:
            domain, confidence, alternatives = classifier.classify_with_confidence(query)
            
            is_correct = domain == expected
            status = "✅" if is_correct else "❌"
            
            if is_correct:
                correct += 1
            
            print(f"{status} \"{query}\" → {domain} (expected: {expected})")
        
        accuracy = (correct / total) * 100
        print(f"\n📊 ML Classifier Accuracy: {correct}/{total} ({accuracy:.1f}%)")
        
        return accuracy >= 80
        
    except Exception as e:
        print(f"❌ ML Classifier Error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 QUICK DOMAIN CLASSIFICATION DIAGNOSTIC")
    print("=" * 60)
    
    # Test ML classifier first
    ml_working = test_ml_classifier_directly()
    
    # Test full agent
    agent_working = test_basic_domains()
    
    print("\n" + "=" * 60)
    print("🏁 DIAGNOSTIC RESULTS:")
    
    if ml_working and agent_working:
        print("✅ Everything is working correctly!")
    elif ml_working:
        print("✅ ML Classifier is working")
        print("❌ Agent has integration issues")
    else:
        print("❌ ML Classifier has issues")
        print("❌ This is causing agent problems")
    
    print("\n💡 If there are issues, I'll fix them immediately!")