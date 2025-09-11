#!/usr/bin/env python3
"""
Final test to verify kidnapping classification is working
"""

from enhanced_legal_agent import create_enhanced_legal_agent

def test_kidnapping_with_agent():
    """Test kidnapping queries with the full legal agent"""
    
    # Create agent
    agent = create_enhanced_legal_agent()
    
    # Test kidnapping query
    query = "My 5-year-old daughter was kidnapped for ransom"
    
    print("Testing Kidnapping Query with Enhanced Legal Agent")
    print("=" * 55)
    print(f"Query: \"{query}\"")
    print()
    
    # Process query
    response = agent.process_enhanced_query(query)
    
    print(f"Domain: {response.domain}")
    print(f"Confidence: {response.confidence:.3f}")
    print(f"Legal Route: {response.legal_route}")
    print(f"Jurisdiction: {response.jurisdiction}")
    print()
    
    if response.domain == "criminal_law":
        print("✅ SUCCESS: Kidnapping correctly classified as criminal_law")
    else:
        print(f"❌ ERROR: Expected criminal_law, got {response.domain}")

if __name__ == "__main__":
    test_kidnapping_with_agent()