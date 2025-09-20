#!/usr/bin/env python3
"""
Domain Classifier Diagnostic and Fix
====================================

This script diagnoses and fixes the domain classification issue where
all queries are returning "unknown" instead of proper legal domains.

Issues to check:
1. ML Classifier initialization
2. Model files loading
3. Confidence thresholds
4. Training data
5. Fallback classification
"""

import sys
import os
import traceback

def test_basic_classification():
    """Test basic domain classification"""
    
    print("🔍 DOMAIN CLASSIFIER DIAGNOSTIC")
    print("=" * 50)
    
    test_queries = [
        "My Passport is Expired",
        "My Boss is not paying for Overtime", 
        "My landlord won't return my security deposit",
        "I want to divorce my husband",
        "My phone is being hacked",
        "I bought a defective product"
    ]
    
    expected_domains = [
        "immigration_law",
        "employment_law", 
        "tenant_rights",
        "family_law",
        "cyber_crime",
        "consumer_complaint"
    ]
    
    print("📋 Test Queries:")
    for i, (query, expected) in enumerate(zip(test_queries, expected_domains), 1):
        print(f"   {i}. '{query}' → should be: {expected}")
    
    # Test ML Classifier
    print(f"\n🤖 TESTING ML CLASSIFIER:")
    print("-" * 30)
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        
        classifier = create_ml_domain_classifier()
        print("✅ ML Classifier imported successfully")
        
        # Check if trained
        if hasattr(classifier, 'is_trained') and classifier.is_trained:
            print("✅ ML Classifier is trained")
        else:
            print("❌ ML Classifier not trained - training now...")
            if hasattr(classifier, 'train_models'):
                success = classifier.train_models()
                if success:
                    print("✅ ML Classifier trained successfully")
                else:
                    print("❌ ML Classifier training failed")
        
        # Test classifications
        print(f"\n📊 ML Classification Results:")
        for query, expected in zip(test_queries, expected_domains):
            try:
                domain, confidence, alternatives = classifier.classify_with_confidence(query)
                status = "✅" if domain != "unknown" else "❌"
                print(f"   {status} '{query}' → {domain} ({confidence:.3f})")
                
                if domain == "unknown":
                    print(f"      Alternatives: {alternatives[:2]}")
                    
            except Exception as e:
                print(f"   ❌ Error classifying '{query}': {e}")
                
    except ImportError as e:
        print(f"❌ Cannot import ML Classifier: {e}")
    except Exception as e:
        print(f"❌ ML Classifier error: {e}")
        traceback.print_exc()
    
    # Test Basic Legal Agent Classifier
    print(f"\n🏛️ TESTING BASIC LEGAL AGENT CLASSIFIER:")
    print("-" * 40)
    
    try:
        from legal_agent import DomainClassifier
        
        basic_classifier = DomainClassifier()
        print("✅ Basic Domain Classifier imported successfully")
        
        print(f"\n📊 Basic Classification Results:")
        for query, expected in zip(test_queries, expected_domains):
            try:
                domain, confidence = basic_classifier.classify(query)
                status = "✅" if domain != "unknown" else "❌"
                print(f"   {status} '{query}' → {domain} ({confidence:.3f})")
                    
            except Exception as e:
                print(f"   ❌ Error classifying '{query}': {e}")
                
    except ImportError as e:
        print(f"❌ Cannot import Basic Classifier: {e}")
    except Exception as e:
        print(f"❌ Basic Classifier error: {e}")
        traceback.print_exc()
    
    # Test Working Enhanced Agent
    print(f"\n💪 TESTING WORKING ENHANCED AGENT:")
    print("-" * 35)
    
    try:
        from working_enhanced_agent import WorkingEnhancedAgent
        
        agent = WorkingEnhancedAgent()
        print("✅ Working Enhanced Agent imported successfully")
        print(f"   ML Available: {agent.ml_available}")
        
        print(f"\n📊 Enhanced Agent Classification Results:")
        for query, expected in zip(test_queries, expected_domains):
            try:
                response = agent.process_query(query)
                status = "✅" if response.domain != "unknown" else "❌"
                print(f"   {status} '{query}' → {response.domain} ({response.confidence:.3f})")
                    
            except Exception as e:
                print(f"   ❌ Error processing '{query}': {e}")
                traceback.print_exc()
                
    except ImportError as e:
        print(f"❌ Cannot import Working Enhanced Agent: {e}")
    except Exception as e:
        print(f"❌ Working Enhanced Agent error: {e}")
        traceback.print_exc()

def fix_classification_issues():
    """Attempt to fix common classification issues"""
    
    print(f"\n🔧 ATTEMPTING TO FIX CLASSIFICATION ISSUES:")
    print("=" * 50)
    
    # Fix 1: Retrain ML Classifier
    print("🔧 Fix 1: Retrain ML Classifier with lower confidence threshold")
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        
        classifier = create_ml_domain_classifier()
        
        # Lower confidence threshold
        if hasattr(classifier, 'confidence_threshold'):
            old_threshold = classifier.confidence_threshold
            classifier.confidence_threshold = 0.05  # Much lower threshold
            print(f"   ✅ Lowered confidence threshold: {old_threshold} → {classifier.confidence_threshold}")
        
        # Retrain if needed
        if not classifier.is_trained:
            print("   🔄 Training ML models...")
            success = classifier.train_models()
            if success:
                print("   ✅ ML Classifier retrained successfully")
            else:
                print("   ❌ ML Classifier retraining failed")
        
    except Exception as e:
        print(f"   ❌ Fix 1 failed: {e}")
    
    # Fix 2: Enhance keyword matching
    print(f"\n🔧 Fix 2: Test enhanced keyword matching")
    try:
        test_enhanced_keywords()
    except Exception as e:
        print(f"   ❌ Fix 2 failed: {e}")
    
    # Fix 3: Create simple rule-based backup
    print(f"\n🔧 Fix 3: Create rule-based classification backup")
    try:
        create_rule_based_classifier()
    except Exception as e:
        print(f"   ❌ Fix 3 failed: {e}")

def test_enhanced_keywords():
    """Test enhanced keyword matching"""
    
    enhanced_patterns = {
        'immigration_law': ['passport', 'visa', 'citizenship', 'immigration', 'green card', 'expired', 'renewal'],
        'employment_law': ['boss', 'employer', 'work', 'job', 'salary', 'overtime', 'pay', 'workplace', 'fired', 'termination'],
        'tenant_rights': ['landlord', 'rent', 'deposit', 'eviction', 'lease', 'apartment', 'housing'],
        'family_law': ['divorce', 'marriage', 'custody', 'spouse', 'husband', 'wife', 'child'],
        'cyber_crime': ['hack', 'hacked', 'phone', 'computer', 'online', 'cyber', 'internet', 'digital'],
        'consumer_complaint': ['defective', 'product', 'warranty', 'refund', 'company', 'service', 'purchase']
    }
    
    test_queries = [
        "My Passport is Expired",
        "My Boss is not paying for Overtime", 
        "My landlord won't return my security deposit",
        "I want to divorce my husband",
        "My phone is being hacked",
        "I bought a defective product"
    ]
    
    print("   📊 Enhanced Keyword Matching Results:")
    
    for query in test_queries:
        query_lower = query.lower()
        best_domain = 'unknown'
        best_score = 0
        
        for domain, keywords in enhanced_patterns.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > best_score:
                best_score = score
                best_domain = domain
        
        confidence = min(0.8, best_score * 0.2) if best_score > 0 else 0.0
        status = "✅" if best_domain != "unknown" else "❌"
        print(f"   {status} '{query}' → {best_domain} ({confidence:.3f}) [score: {best_score}]")

def create_rule_based_classifier():
    """Create a simple rule-based classifier as backup"""
    
    def classify_rule_based(query):
        """Simple rule-based classification"""
        
        query_lower = query.lower()
        
        # Simple rules for common cases
        if any(word in query_lower for word in ['passport', 'visa', 'immigration', 'citizenship']):
            return 'immigration_law', 0.8
        elif any(word in query_lower for word in ['boss', 'employer', 'work', 'overtime', 'salary', 'job']):
            return 'employment_law', 0.8
        elif any(word in query_lower for word in ['landlord', 'rent', 'deposit', 'eviction']):
            return 'tenant_rights', 0.8
        elif any(word in query_lower for word in ['divorce', 'marriage', 'husband', 'wife']):
            return 'family_law', 0.8
        elif any(word in query_lower for word in ['hack', 'hacked', 'cyber', 'phone', 'computer']):
            return 'cyber_crime', 0.8
        elif any(word in query_lower for word in ['defective', 'product', 'warranty', 'refund']):
            return 'consumer_complaint', 0.8
        else:
            return 'unknown', 0.0
    
    test_queries = [
        "My Passport is Expired",
        "My Boss is not paying for Overtime", 
        "My landlord won't return my security deposit"
    ]
    
    print("   📊 Rule-Based Classification Results:")
    for query in test_queries:
        domain, confidence = classify_rule_based(query)
        status = "✅" if domain != "unknown" else "❌"
        print(f"   {status} '{query}' → {domain} ({confidence:.3f})")
    
    return classify_rule_based

def main():
    """Main diagnostic function"""
    
    print("🏛️ LEGAL AGENT DOMAIN CLASSIFIER DIAGNOSTIC & FIX")
    print("=" * 60)
    print("Diagnosing why queries return 'unknown' instead of proper domains")
    print("=" * 60)
    
    # Test current state
    test_basic_classification()
    
    # Attempt fixes
    fix_classification_issues()
    
    print(f"\n✅ DIAGNOSTIC COMPLETE!")
    print(f"   If issues persist, the problem may be in:")
    print(f"   1. Model file corruption")
    print(f"   2. Training data issues") 
    print(f"   3. Confidence threshold too high")
    print(f"   4. Import/initialization failures")

if __name__ == "__main__":
    main()