"""
Demo: Fixed Unknown Query Handling
==================================

Simple demonstration of the enhanced unknown query handling.
"""

from working_enhanced_agent import create_working_enhanced_agent

def demo_fix():
    """Demonstrate the fix for unknown queries"""
    
    print("🔧 DEMO: FIXED UNKNOWN QUERY HANDLING")
    print("=" * 50)
    
    agent = create_working_enhanced_agent()
    
    # Test the original problematic query
    test_queries = [
        "my neighbor girl is being harassed",
        "boss sexually harassing me",
        "someone hacked my phone",
        "my car was stolen",
        "need help with property issue"
    ]
    
    print(f"\n🧪 Testing {len(test_queries)} queries:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: \"{query}\"")
        
        response = agent.process_query(query)
        
        print(f"   Result: {response.domain} (confidence: {response.confidence:.3f})")
        print(f"   Route: {response.legal_route[:60]}...")
        print(f"   Timeline: {response.timeline}")
        
        if response.domain != 'unknown':
            print(f"   ✅ FIXED: No longer 'unknown'!")
        else:
            print(f"   ❌ Still unknown")
    
    print(f"\n🎉 Demo complete!")

if __name__ == "__main__":
    demo_fix()
