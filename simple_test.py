#!/usr/bin/env python3

import sys
import os

# Test single query
def test_single_query():
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        
        query = "my phone is being hacked by someone"
        domain, confidence, alternatives = classifier.classify_with_confidence(query)
        
        print(f"Query: {query}")
        print(f"Domain: {domain}")
        print(f"Confidence: {confidence:.3f}")
        print(f"Expected: cyber_crime")
        print(f"Status: {'✅ CORRECT' if domain == 'cyber_crime' else '❌ WRONG'}")
        
        return domain == 'cyber_crime'
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_single_query()