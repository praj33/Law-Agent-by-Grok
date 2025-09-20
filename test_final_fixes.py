#!/usr/bin/env python3
"""
DOMAIN CLASSIFICATION FIXES - FINAL VALIDATION
==============================================

This script validates that all domain classification fixes are working correctly.
"""

def main():
    """Test all fixes and provide final validation"""
    
    print("🎯 DOMAIN CLASSIFICATION FIXES - FINAL VALIDATION")
    print("=" * 60)
    print()
    
    print("📋 FIXES APPLIED:")
    print("-" * 20)
    print("✅ 1. ML Classifier thresholds lowered to 0.001 (emergency level)")
    print("✅ 2. Enhanced agent override logic disabled")
    print("✅ 3. ML classifier results now prioritized")
    print("✅ 4. Enhanced analysis only used as last resort")
    print("✅ 5. Forced model retraining on initialization")
    print()
    
    # Critical test queries
    test_queries = [
        ("my phone is being hacked by someone", "cyber_crime"),
        ("my boss is not giving my salary", "employment_law"), 
        ("landlord not returning deposit", "tenant_rights"),
        ("bought defective phone want refund", "consumer_complaint"),
        ("my husband beats me daily", "family_law"),
        ("I was raped by my neighbor", "criminal_law"),
        ("passport expired need renewal", "immigration_law"),
        ("contract was breached", "contract_dispute"),
        ("elderly father being abused", "elder_abuse"),
        ("injured in car accident", "personal_injury")
    ]
    
    # Test ML Classifier
    print("🤖 TESTING ML CLASSIFIER (FIXED):")
    print("-" * 35)
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        
        classifier = create_ml_domain_classifier()
        print(f"✅ Classifier loaded")
        print(f"   Confidence threshold: {classifier.confidence_threshold}")
        print(f"   Cosine threshold: {classifier.cosine_threshold}")
        print(f"   Is trained: {classifier.is_trained}")
        print()
        
        ml_correct = 0
        for i, (query, expected) in enumerate(test_queries, 1):
            try:
                domain, confidence, alternatives = classifier.classify_with_confidence(query)
                
                if domain == expected:
                    status = "✅ CORRECT"
                    ml_correct += 1
                elif domain == "unknown":
                    status = "❌ UNKNOWN"
                else:
                    status = f"⚠️ WRONG (got {domain})"
                
                print(f"{status} Test {i:2d}: \"{query[:40]}...\"")
                print(f"             Expected: {expected} | Got: {domain} ({confidence:.3f})")
                print()
                
            except Exception as e:
                print(f"❌ Test {i:2d}: ERROR - {e}")
        
        ml_accuracy = (ml_correct / len(test_queries)) * 100
        print(f"📊 ML CLASSIFIER ACCURACY: {ml_correct}/{len(test_queries)} ({ml_accuracy:.1f}%)")
        
    except Exception as e:
        print(f"❌ ML Classifier test failed: {e}")
        ml_accuracy = 0
    
    print()
    
    # Test Enhanced Agent
    print("🚀 TESTING ENHANCED AGENT (FIXED):")
    print("-" * 35)
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        agent = create_working_enhanced_agent()
        print(f"✅ Enhanced agent loaded")
        print()
        
        agent_correct = 0
        for i, (query, expected) in enumerate(test_queries, 1):
            try:
                response = agent.process_query(query)
                domain = response.domain
                confidence = response.confidence
                
                if domain == expected:
                    status = "✅ CORRECT"
                    agent_correct += 1
                elif domain == "unknown":
                    status = "❌ UNKNOWN"
                else:
                    status = f"⚠️ WRONG (got {domain})"
                
                print(f"{status} Test {i:2d}: \"{query[:40]}...\"")
                print(f"             Expected: {expected} | Got: {domain} ({confidence:.3f})")
                print()
                
            except Exception as e:
                print(f"❌ Test {i:2d}: ERROR - {e}")
        
        agent_accuracy = (agent_correct / len(test_queries)) * 100
        print(f"📊 ENHANCED AGENT ACCURACY: {agent_correct}/{len(test_queries)} ({agent_accuracy:.1f}%)")
        
    except Exception as e:
        print(f"❌ Enhanced Agent test failed: {e}")
        agent_accuracy = 0
    
    # Final Assessment
    print()
    print("🎯 FINAL ASSESSMENT:")
    print("=" * 25)
    
    if agent_accuracy >= 80:
        print("🎉 EXCELLENT! Domain classification is now working correctly!")
        print(f"   Enhanced Agent Accuracy: {agent_accuracy:.1f}%")
        print()
        print("✅ YOUR ISSUES SHOULD BE FIXED!")
        print("   • Queries should now return correct domains")
        print("   • 'my phone is being hacked' → cyber_crime")
        print("   • 'my boss not paying salary' → employment_law")
        print("   • 'landlord not returning deposit' → tenant_rights")
        print()
        print("🚀 HOW TO TEST:")
        print("   1. Open a new terminal")
        print("   2. Run: python cli_interface.py")
        print("   3. Try: 'my phone is being hacked by someone'")
        print("   4. Should get: cyber_crime domain")
        
    elif agent_accuracy >= 60:
        print("⚠️ IMPROVED but still has some issues")
        print(f"   Enhanced Agent Accuracy: {agent_accuracy:.1f}%")
        print("   Most queries should work, but some may still be incorrect")
        
    else:
        print("❌ STILL HAS MAJOR ISSUES")
        print(f"   Enhanced Agent Accuracy: {agent_accuracy:.1f}%")
        print("   Further investigation needed")
    
    print()
    print("📝 TROUBLESHOOTING:")
    print("   • If you're still getting wrong domains, restart your terminal")
    print("   • Make sure you're using a fresh terminal session")
    print("   • Try simple queries first like 'phone hacked' or 'boss not paying'")
    print("   • Check if you're using --adaptive flag which has different behavior")

if __name__ == "__main__":
    main()