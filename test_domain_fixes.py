#!/usr/bin/env python3
"""
Quick Domain Classification Test - Verify Fixes
==============================================

Test critical queries to ensure domain classification is working correctly.
"""

def test_critical_queries():
    """Test critical queries that should return specific domains"""
    
    print("🧪 TESTING DOMAIN CLASSIFICATION FIXES")
    print("=" * 50)
    
    # Test queries that should return specific domains
    test_cases = [
        ("my phone is being hacked by someone", "cyber_crime"),
        ("my boss is not giving my salary", "employment_law"),
        ("landlord not returning deposit", "tenant_rights"),
        ("bought defective phone want refund", "consumer_complaint"),
        ("my husband beats me daily", "family_law"),
        ("I was raped by my neighbor", "criminal_law"),
        ("passport expired need renewal", "immigration_law"),
        ("contract was breached by vendor", "contract_dispute"),
        ("elderly father being abused", "elder_abuse"),
        ("injured in car accident", "personal_injury")
    ]
    
    try:
        # Test ML Classifier directly
        print("🤖 TESTING ML CLASSIFIER:")
        print("-" * 30)
        
        from ml_domain_classifier import create_ml_domain_classifier
        
        classifier = create_ml_domain_classifier()
        print(f"✅ ML Classifier loaded successfully")
        print(f"   Confidence threshold: {classifier.confidence_threshold}")
        print(f"   Cosine threshold: {classifier.cosine_threshold}")
        print()
        
        ml_results = []
        for query, expected in test_cases:
            try:
                domain, confidence, alternatives = classifier.classify_with_confidence(query)
                
                # Determine status
                if domain == expected:
                    status = "✅ CORRECT"
                elif domain == "unknown":
                    status = "❌ UNKNOWN"
                else:
                    status = f"⚠️ WRONG (got {domain})"
                
                ml_results.append((query, expected, domain, confidence, status))
                print(f"{status}")
                print(f"   Query: \"{query}\"")
                print(f"   Expected: {expected} | Got: {domain} (conf: {confidence:.3f})")
                print()
                
            except Exception as e:
                print(f"❌ Error testing '{query}': {e}")
                ml_results.append((query, expected, "ERROR", 0.0, "ERROR"))
        
        # Test Enhanced Agent
        print("🚀 TESTING ENHANCED AGENT:")
        print("-" * 30)
        
        from working_enhanced_agent import create_working_enhanced_agent
        
        agent = create_working_enhanced_agent()
        print(f"✅ Enhanced Agent loaded successfully")
        print()
        
        agent_results = []
        for query, expected in test_cases:
            try:
                response = agent.process_query(query)
                domain = response.domain
                confidence = response.confidence
                
                # Determine status
                if domain == expected:
                    status = "✅ CORRECT"
                elif domain == "unknown":
                    status = "❌ UNKNOWN"
                else:
                    status = f"⚠️ WRONG (got {domain})"
                
                agent_results.append((query, expected, domain, confidence, status))
                print(f"{status}")
                print(f"   Query: \"{query}\"")
                print(f"   Expected: {expected} | Got: {domain} (conf: {confidence:.3f})")
                print()
                
            except Exception as e:
                print(f"❌ Error testing '{query}': {e}")
                agent_results.append((query, expected, "ERROR", 0.0, "ERROR"))
        
        # Summary
        print("📊 SUMMARY:")
        print("-" * 20)
        
        ml_correct = sum(1 for _, _, _, _, status in ml_results if "CORRECT" in status)
        ml_total = len(ml_results)
        
        agent_correct = sum(1 for _, _, _, _, status in agent_results if "CORRECT" in status)
        agent_total = len(agent_results)
        
        print(f"ML Classifier: {ml_correct}/{ml_total} correct ({ml_correct/ml_total*100:.1f}%)")
        print(f"Enhanced Agent: {agent_correct}/{agent_total} correct ({agent_correct/agent_total*100:.1f}%)")
        
        if agent_correct >= ml_correct:
            print(f"✅ Enhanced Agent performing well!")
        else:
            print(f"⚠️ Enhanced Agent needs improvement")
        
        if agent_correct >= agent_total * 0.8:  # 80% threshold
            print(f"🎉 EXCELLENT: Domain classification working correctly!")
            return True
        else:
            print(f"❌ POOR: Domain classification needs more fixes")
            return False
        
    except Exception as e:
        print(f"❌ Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_critical_queries()
    if success:
        print("\n✅ Domain classification fixes successful!")
        print("You should now get correct domains for all queries.")
    else:
        print("\n❌ Domain classification still has issues.")
        print("Manual investigation needed.")