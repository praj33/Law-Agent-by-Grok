#!/usr/bin/env python3
"""
Final Test - Constitutional Articles Integration
===============================================
"""

from legal_agent import create_legal_agent, LegalQueryInput

def test_final_integration():
    """Test final integration with improved constitutional articles"""
    
    print("=== FINAL INTEGRATION TEST ===")
    print()
    
    agent = create_legal_agent()
    query = LegalQueryInput(user_input="my phone is being hacked by someone")
    response = agent.process_query(query)
    
    print(f"🔍 Query: 'my phone is being hacked by someone'")
    print(f"📋 Domain: {response.domain}")
    print(f"📊 Confidence: {response.confidence:.3f}")
    print()
    
    if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
        print("🏛️ Constitutional Articles:")
        for i, article in enumerate(response.constitutional_articles, 1):
            print(f"  {i}. Article {article.get('article_number', 'N/A')}")
            print(f"     Title: {article.get('title', 'N/A')}")
            print(f"     Confidence: {article.get('confidence_percentage', 0)}%")
            print()
        
        print("✅ SUCCESS: Constitutional articles with confidence returned!")
    else:
        print("❌ ISSUE: No constitutional articles returned")
    
    # Test constitutional backing text
    if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
        print("📜 Constitutional Backing Preview:")
        preview = response.constitutional_backing[:300] + "..." if len(response.constitutional_backing) > 300 else response.constitutional_backing
        print(preview)
        print()
        
        # Check if it contains confidence percentages
        if "Confidence:" in response.constitutional_backing:
            print("✅ SUCCESS: Constitutional backing includes confidence percentages!")
        else:
            print("⚠️ NOTICE: Constitutional backing may not include confidence percentages")
    
    print("=" * 60)
    print("✅ Final integration test completed!")

if __name__ == "__main__":
    test_final_integration()