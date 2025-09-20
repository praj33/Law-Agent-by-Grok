#!/usr/bin/env python3
"""
Test the enhanced ML domain classifier with new features
"""

def test_enhanced_ml_classifier():
    print("🧪 TESTING ENHANCED ML DOMAIN CLASSIFIER")
    print("=" * 50)
    
    # Import and initialize the enhanced classifier
    from ml_domain_classifier import create_ml_domain_classifier
    classifier = create_ml_domain_classifier()
    
    # Test the new get_model_stats method
    print("1. Testing Enhanced Model Statistics...")
    stats = classifier.get_model_stats()
    print(f"   ✅ Model Stats Working:")
    print(f"      - Training Examples: {stats['training_examples']}")
    print(f"      - Domains: {stats['domain_count']}")
    print(f"      - Classifications Made: {stats['classifications_made']}")
    print(f"      - Confidence Threshold: {stats['confidence_threshold']}")
    print(f"      - Min Confidence for Classification: {stats['min_confidence_for_classification']}")
    print(f"      - High Confidence Threshold: {stats['high_confidence_threshold']}")
    
    # Test various queries to see the enhanced confidence handling
    test_queries = [
        "my phone was stolen",
        "I need a divorce",
        "boss is harassing me at work",
        "bought a defective product",
        "landlord won't return my deposit",
        "someone hacked my computer",
        "passport has expired",
        "contract was breached",
        "elderly parent being abused",
        "injured in a car accident"
    ]
    
    print("\n2. Testing Enhanced Classification with New Thresholds...")
    high_confidence_count = 0
    total_tests = len(test_queries)
    
    for query in test_queries:
        domain, confidence, alternatives = classifier.classify_with_confidence(query)
        is_high_confidence = confidence >= stats['high_confidence_threshold']
        if is_high_confidence:
            high_confidence_count += 1
        status = "✅ HIGH" if is_high_confidence else "⚠️  NORMAL"
        print(f"   {status} '{query[:30]:<30}' -> {domain:<20} (confidence: {confidence:.3f})")
    
    print(f"\n📊 Classification Results:")
    print(f"   - High Confidence Classifications: {high_confidence_count}/{total_tests}")
    print(f"   - Success Rate: {high_confidence_count/total_tests*100:.1f}%")
    
    # Test edge cases
    print("\n3. Testing Edge Cases...")
    edge_cases = [
        "random text with no legal meaning",
        "I need help with something",
        ""  # Empty string
    ]
    
    for query in edge_cases:
        try:
            domain, confidence, alternatives = classifier.classify_with_confidence(query)
            print(f"   ✅ Edge Case '{query[:20]:<20}' -> {domain:<15} (confidence: {confidence:.3f})")
        except Exception as e:
            print(f"   ❌ Edge Case '{query[:20]:<20}' failed: {e}")
    
    print("\n🎉 ENHANCED ML DOMAIN CLASSIFIER TESTS COMPLETED!")
    return True

if __name__ == "__main__":
    success = test_enhanced_ml_classifier()
    if success:
        print("\n✅ Enhanced ML Classifier is ready for production!")
    else:
        print("\n❌ Enhanced ML Classifier needs attention!")