#!/usr/bin/env python3
"""
Test script to check kidnapping domain classification
"""

from enhanced_legal_agent import create_enhanced_legal_agent

def test_kidnapping_queries():
    """Test how kidnapping queries are classified"""
    
    # Create agent
    agent = create_enhanced_legal_agent()
    
    # Test queries related to kidnapping
    test_queries = [
        "My child was kidnapped for ransom",
        "My daughter was kidnapped and held for ransom",
        "Someone kidnapped my son from school",
        "Child kidnapping with ransom demand",
        "My 5-year-old daughter was kidnapped for ransom"
    ]
    
    print("Testing Kidnapping Query Classification")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: \"{query}\"")
        
        # Test with ML classifier
        domain, confidence, alternatives = agent.ml_classifier.classify_with_confidence(query)
        print(f"ML Classification: {domain} (confidence: {confidence:.3f})")
        
        if alternatives:
            print("Top alternatives:")
            for alt_domain, alt_conf in alternatives[:3]:
                print(f"  - {alt_domain}: {alt_conf:.3f}")
        
        # Test with enhanced classifier if available
        try:
            from enhanced_domain_classifier import create_enhanced_domain_classifier
            enhanced_classifier = create_enhanced_domain_classifier()
            enh_domain, enh_confidence, enh_alternatives = enhanced_classifier.classify_domain(query)
            print(f"Enhanced Classification: {enh_domain} (confidence: {enh_confidence:.3f})")
        except ImportError:
            print("Enhanced classifier not available")

if __name__ == "__main__":
    test_kidnapping_queries()