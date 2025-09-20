#!/usr/bin/env python3
"""
Test Query: My phone is stolen
"""

from working_enhanced_agent import create_working_enhanced_agent

def test_stolen_phone_query():
    """Test the stolen phone query classification"""
    
    # Create agent
    agent = create_working_enhanced_agent()
    
    # Test the query
    query = "My phone is stolen"
    print(f"Testing query: \"{query}\"")
    print("-" * 50)
    
    response = agent.process_query(query)
    
    print(f"✅ RESULT:")
    print(f"   Domain: {response.domain}")
    print(f"   Confidence: {response.confidence:.3f}")
    print(f"   Timeline: {response.timeline}")
    print(f"   Success Rate: {response.success_rate:.1%}")
    print(f"   Legal Route: {response.legal_route}")
    
    # Explain the classification
    if response.domain == "criminal_law":
        print(f"\n📝 EXPLANATION:")
        print(f"   ✅ Correctly classified as CRIMINAL LAW")
        print(f"   📱 Phone theft is a criminal offense")
        print(f"   🚔 Requires police complaint (FIR)")
        print(f"   ⚖️ Falls under IPC Section 379 (Theft)")
    elif response.domain == "cyber_crime":
        print(f"\n📝 EXPLANATION:")
        print(f"   ⚠️ Classified as CYBER CRIME")
        print(f"   💭 May be due to 'phone' keyword association")
        print(f"   📱 Physical phone theft should be criminal law")
    else:
        print(f"\n📝 EXPLANATION:")
        print(f"   ❓ Classified as: {response.domain}")
        print(f"   💭 Phone theft should typically be criminal_law")

if __name__ == "__main__":
    test_stolen_phone_query()