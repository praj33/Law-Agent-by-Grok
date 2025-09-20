#!/usr/bin/env python3
"""
Script to retrain the domain classifier with updated training data
"""

from ml_domain_classifier import create_ml_domain_classifier

def retrain_classifier():
    """Force retrain the domain classifier with updated training data"""
    
    print("🚀 Retraining ML Domain Classifier with updated training data...")
    
    # Create classifier which will automatically retrain with updated data
    classifier = create_ml_domain_classifier()
    
    # Test some queries to verify the retraining worked
    test_queries = [
        "My 5-year-old daughter was kidnapped for ransom",
        "Someone is hacking my computer",
        "I need custody of my children",
        "I was raped by my neighbor"
    ]
    
    print("\n🧪 Testing retrained classifier:")
    print("-" * 50)
    
    for query in test_queries:
        domain, confidence, alternatives = classifier.classify_with_confidence(query)
        print(f"Query: \"{query}\"")
        print(f"  Domain: {domain} (confidence: {confidence:.3f})")
        print(f"  Top alternatives: {alternatives[:3]}")
        print()
    
    print("✅ Retraining complete!")
    return classifier

if __name__ == "__main__":
    retrain_classifier()