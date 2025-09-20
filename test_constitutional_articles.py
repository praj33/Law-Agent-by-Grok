#!/usr/bin/env python3
"""
Test Constitutional Articles with Meanings and Confidence
========================================================

This script tests the enhanced constitutional integration that now includes:
- Article numbers
- Article titles/meanings
- Confidence percentages for each article
"""

from legal_agent import create_legal_agent, LegalQueryInput
import json

def test_constitutional_articles():
    """Test constitutional articles with meanings and confidence"""
    
    print("=== CONSTITUTIONAL ARTICLES TEST ===")
    print()
    
    # Create agent
    try:
        agent = create_legal_agent()
        print("✅ Legal agent created successfully")
    except Exception as e:
        print(f"❌ Failed to create legal agent: {e}")
        return
    
    # Test queries
    test_queries = [
        "my coworker is sexually harassing me at workplace",
        "my phone is being hacked by someone",
        "landlord not returning my security deposit",
        "I want to divorce my husband"
    ]
    
    for i, query_text in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: '{query_text}'")
        print("-" * 60)
        
        try:
            # Process query
            query = LegalQueryInput(user_input=query_text)
            response = agent.process_query(query)
            
            print(f"Domain: {response.domain}")
            print(f"Confidence: {response.confidence:.3f}")
            print()
            
            # Check constitutional articles
            if response.constitutional_articles:
                print("📋 Constitutional Articles with Meanings and Confidence:")
                for j, article in enumerate(response.constitutional_articles, 1):
                    article_num = article.get('article_number', 'N/A')
                    title = article.get('title', 'N/A')
                    summary = article.get('summary', 'N/A')
                    confidence = article.get('confidence_percentage')
                    
                    print(f"  {j}. Article {article_num}")
                    print(f"     Title: {title}")
                    
                    if summary and summary != 'N/A':
                        if len(summary) > 100:
                            summary = summary[:100] + "..."
                        print(f"     Meaning: {summary}")
                    
                    if confidence is not None:
                        print(f"     Confidence: {confidence}%")
                    
                    print()
            else:
                print("❌ No constitutional articles found")
            
            # Check constitutional backing text
            if response.constitutional_backing:
                print("🏛️ Constitutional Backing Preview:")
                lines = response.constitutional_backing.split('\n')
                for line in lines[:8]:
                    if line.strip():
                        print(f"  {line}")
                if len(lines) > 8:
                    print("  ...")
            else:
                print("❌ No constitutional backing found")
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            import traceback
            traceback.print_exc()
        
        print()

def test_direct_constitutional_matcher():
    """Test the constitutional matcher directly"""
    
    print("\n=== DIRECT CONSTITUTIONAL MATCHER TEST ===")
    print()
    
    try:
        from constitutional_article_matcher import get_constitutional_articles_with_confidence
        
        query = "workplace harassment by colleague"
        print(f"Testing query: '{query}'")
        
        analysis = get_constitutional_articles_with_confidence(query)
        
        print(f"Total articles searched: {analysis.get('total_articles_searched', 0)}")
        print(f"Matching articles found: {analysis.get('matching_articles', 0)}")
        
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print("\n📋 Top Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. Article {rec.get('article_number')} - {rec.get('confidence_percentage', 0)}%")
                print(f"     Title: {rec.get('title', 'N/A')}")
                content_preview = rec.get('content_preview', '')
                if content_preview:
                    if len(content_preview) > 80:
                        content_preview = content_preview[:80] + "..."
                    print(f"     Content: {content_preview}")
                print()
        else:
            print("❌ No recommendations found")
            
    except Exception as e:
        print(f"❌ Error testing constitutional matcher: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_constitutional_articles()
    test_direct_constitutional_matcher()
    
    print("\n✅ Constitutional articles test completed!")