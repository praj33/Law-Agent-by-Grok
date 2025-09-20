#!/usr/bin/env python3
"""
Quick Domain Classification Test
===============================

Tests the fixes for domain classification returning "unknown"
"""

def test_domain_classification():
    """Test domain classification with the fixed system"""
    
    print("🧪 TESTING DOMAIN CLASSIFICATION FIXES")
    print("=" * 50)
    
    # Test queries that were returning "unknown"
    test_cases = [
        ("My Passport is Expired", "immigration_law"),
        ("My Boss is not paying for Overtime", "employment_law"),
        ("My landlord won't return my security deposit", "tenant_rights"),
        ("I want to divorce my husband", "family_law"),
        ("My phone is being hacked", "cyber_crime"),
        ("I bought a defective product", "consumer_complaint")
    ]
    
    # Test with enhanced fallback classification
    try:
        from working_enhanced_agent import WorkingEnhancedAgent
        
        agent = WorkingEnhancedAgent()
        
        print("🔧 Testing Enhanced Agent (with fallback):")
        print("-" * 40)
        
        for query, expected in test_cases:
            try:
                # Test the fallback classification directly
                domain, confidence = agent.fallback_classification(query)
                
                status = "✅" if domain == expected else "❌" if domain != "unknown" else "⚠️"
                print(f"{status} '{query}' → {domain} ({confidence:.3f})")
                if domain != expected:
                    print(f"   Expected: {expected}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
        # Test enhanced unknown analysis
        print(f"\n🧠 Testing Enhanced Unknown Analysis:")
        print("-" * 40)
        
        for query, expected in test_cases:
            try:
                domain, confidence = agent.enhanced_unknown_analysis(query, [])
                
                status = "✅" if domain == expected else "❌" if domain != "unknown" else "⚠️"
                print(f"{status} '{query}' → {domain} ({confidence:.3f})")
                if domain != expected:
                    print(f"   Expected: {expected}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Cannot test enhanced agent: {e}")
    
    # Test with ML classifier
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        
        print(f"\n🤖 Testing ML Classifier (with lowered threshold):")
        print("-" * 50)
        
        classifier = create_ml_domain_classifier()
        
        for query, expected in test_cases:
            try:
                domain, confidence, alternatives = classifier.classify_with_confidence(query)
                
                status = "✅" if domain == expected else "❌" if domain != "unknown" else "⚠️"
                print(f"{status} '{query}' → {domain} ({confidence:.3f})")
                if domain != expected and domain != "unknown":
                    print(f"   Expected: {expected}")
                elif domain == "unknown":
                    print(f"   Alternatives: {alternatives[:2]}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Cannot test ML classifier: {e}")

if __name__ == "__main__":
    test_domain_classification()