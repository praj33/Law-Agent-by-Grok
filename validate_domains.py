#!/usr/bin/env python3
"""
Domain Classification Validation Test
====================================

Tests the specific domains that should work based on training data.
"""

def validate_domain_classification():
    """Test domain classification for queries that should definitely work"""
    
    print("🎯 DOMAIN CLASSIFICATION VALIDATION")
    print("=" * 50)
    print("Testing queries that should return correct domains based on training data\n")
    
    # Test cases from actual training data patterns
    critical_tests = [
        # Cyber Crime
        ("my phone is being hacked by someone", "cyber_crime"),
        ("phone being hacked and privacy violated", "cyber_crime"),
        ("identity theft and online fraud", "cyber_crime"),
        ("cyberbullying and online harassment", "cyber_crime"),
        
        # Employment Law  
        ("my boss is not giving my salary", "employment_law"),
        ("wrongfully terminated from my job without cause", "employment_law"),
        ("not receiving overtime pay for extra hours", "employment_law"),
        ("workplace harassment by supervisor and colleagues", "employment_law"),
        
        # Family Law
        ("my husband beats me daily", "family_law"),
        ("want to file for divorce from my spouse", "family_law"),
        ("domestic violence and need protection order", "family_law"),
        ("child custody battle with ex-husband", "family_law"),
        
        # Criminal Law
        ("I was raped by my neighbor", "criminal_law"),
        ("arrested and charged with crime need defense", "criminal_law"),
        ("false accusations and need to prove innocence", "criminal_law"),
        
        # Immigration Law
        ("visa application denied need legal help", "immigration_law"),
        ("passport expired need renewal", "immigration_law"),
        ("green card process and permanent residency", "immigration_law"),
        
        # Tenant Rights
        ("my landlord won't return my security deposit", "tenant_rights"),
        ("landlord is trying to evict me without proper notice", "tenant_rights"),
        ("apartment has mold and landlord refuses to fix it", "tenant_rights"),
        
        # Consumer Complaint
        ("bought defective product and company refuses refund", "consumer_complaint"),
        ("warranty claim denied for faulty electronics", "consumer_complaint"),
        ("online shopping fraud and fake products received", "consumer_complaint"),
    ]
    
    try:
        # Test ML Classifier
        print("🤖 TESTING ML CLASSIFIER:")
        print("-" * 30)
        
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        
        print(f"✅ ML Classifier initialized")
        print(f"   Training examples: {len(classifier.training_data) if hasattr(classifier, 'training_data') else 'Unknown'}")
        print(f"   Confidence threshold: {classifier.confidence_threshold}")
        print(f"   Is trained: {classifier.is_trained}")
        print()
        
        correct = 0
        total = len(critical_tests)
        
        for i, (query, expected) in enumerate(critical_tests, 1):
            try:
                domain, confidence, alternatives = classifier.classify_with_confidence(query)
                
                if domain == expected:
                    status = "✅"
                    correct += 1
                elif domain == "unknown":
                    status = "❌"
                else:
                    status = f"⚠️"
                
                print(f"{status} Test {i:2d}: \"{query[:50]}...\"")
                print(f"          Expected: {expected}")
                print(f"          Got: {domain} (confidence: {confidence:.3f})")
                
                if domain != expected and alternatives:
                    print(f"          Alternatives: {[f'{d}({c:.2f})' for d, c in alternatives[:2]]}")
                print()
                
            except Exception as e:
                print(f"❌ Test {i:2d}: Error - {e}")
                print()
        
        accuracy = (correct / total) * 100
        print(f"📊 ML CLASSIFIER RESULTS:")
        print(f"   Correct: {correct}/{total} ({accuracy:.1f}%)")
        
        if accuracy >= 80:
            print(f"   ✅ EXCELLENT - ML Classifier working well!")
        elif accuracy >= 60:
            print(f"   ⚠️ GOOD - Some issues but mostly working")
        else:
            print(f"   ❌ POOR - Major classification issues")
        
        return accuracy >= 70
        
    except ImportError as e:
        print(f"❌ Cannot import ML classifier: {e}")
        return False
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_problem_queries():
    """Test the specific queries mentioned by the user"""
    
    print("\n🔍 TESTING SPECIFIC PROBLEM QUERIES")
    print("=" * 45)
    print("Testing queries that user mentioned were getting wrong domains\n")
    
    # These are likely the queries causing problems
    problem_queries = [
        ("my phone is being hacked by someone", "cyber_crime"),
        ("my boss is not giving my salary", "employment_law"), 
        ("landlord not returning deposit", "tenant_rights"),
        ("I want to divorce my husband", "family_law"),
        ("someone stole my wallet", "criminal_law"),
    ]
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        
        print(f"✅ Enhanced Agent initialized")
        print()
        
        for i, (query, expected) in enumerate(problem_queries, 1):
            try:
                response = agent.process_query(query)
                domain = response.domain
                confidence = response.confidence
                
                if domain == expected:
                    status = "✅ FIXED"
                elif domain == "unknown":
                    status = "❌ UNKNOWN"
                else:
                    status = f"⚠️ WRONG"
                
                print(f"{status} Query {i}: \"{query}\"")
                print(f"         Expected: {expected}")
                print(f"         Got: {domain} (confidence: {confidence:.3f})")
                print()
                
            except Exception as e:
                print(f"❌ Query {i}: Error - {e}")
                print()
        
    except Exception as e:
        print(f"❌ Cannot test enhanced agent: {e}")

if __name__ == "__main__":
    print("🚀 Starting Domain Classification Validation...\n")
    
    # Test ML classifier accuracy
    ml_success = validate_domain_classification()
    
    # Test specific problem queries
    test_specific_problem_queries()
    
    print("\n🎯 FINAL ASSESSMENT:")
    print("-" * 25)
    
    if ml_success:
        print("✅ Domain classification appears to be working correctly!")
        print("   Your queries should now return the right domains.")
        print("   Try testing with: 'my phone is being hacked by someone'")
    else:
        print("❌ Domain classification still has issues.")
        print("   Manual debugging may be needed.")
        print("   Check training data and model files.")
    
    print("\n🔧 TROUBLESHOOTING TIPS:")
    print("1. Restart your terminal/CLI interface")
    print("2. Try simple queries like 'phone hacked' or 'boss not paying salary'")
    print("3. Check if you're using the latest enhanced agent")
    print("4. Verify training data contains the domains you expect")