#!/usr/bin/env python3
"""
Test Improved Constitutional Articles
====================================

This script tests the improved constitutional article recommendations
with confidence filtering and better cyber crime mappings.
"""

from constitutional_article_matcher import get_constitutional_articles_with_confidence
from legal_agent import create_legal_agent, LegalQueryInput

def test_improved_constitutional_articles():
    """Test improved constitutional articles with confidence filtering"""
    
    print("=== IMPROVED CONSTITUTIONAL ARTICLES TEST ===")
    print()
    
    # Test queries
    test_queries = [
        "my phone is being hacked by someone",
        "my coworker is sexually harassing me at workplace", 
        "landlord not returning my security deposit",
        "I want to divorce my husband"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: '{query}'")
        print("-" * 60)
        
        # Test direct constitutional matcher
        print("📋 Direct Constitutional Matcher Results:")
        recommendations = get_constitutional_articles_with_confidence(query)
        
        if recommendations and recommendations.get('recommendations'):
            # Show all recommendations with confidence levels
            for j, rec in enumerate(recommendations['recommendations'][:5], 1):
                confidence = rec['confidence_percentage']
                
                # Color coding based on confidence
                if confidence >= 70:
                    conf_icon = "🟢"
                elif confidence >= 50:
                    conf_icon = "🟡"
                elif confidence >= 30:
                    conf_icon = "🟠"
                else:
                    conf_icon = "🔴"
                
                print(f"  {conf_icon} {j}. Article {rec['article_number']} - {confidence}% Confidence")
                print(f"     Title: {rec['title']}")
                
                if rec.get('matching_keywords'):
                    print(f"     Keywords: {', '.join(rec['matching_keywords'][:3])}")
                
                if rec.get('match_reasons'):
                    print(f"     Reason: {rec['match_reasons'][0]}")
                print()
            
            # Show filtering results
            high_conf = [r for r in recommendations['recommendations'] if r['confidence_percentage'] >= 50]
            medium_conf = [r for r in recommendations['recommendations'] if 30 <= r['confidence_percentage'] < 50]
            low_conf = [r for r in recommendations['recommendations'] if r['confidence_percentage'] < 30]
            
            print(f"📊 Confidence Distribution:")
            print(f"   • High (≥50%): {len(high_conf)} articles")
            print(f"   • Medium (30-49%): {len(medium_conf)} articles") 
            print(f"   • Low (<30%): {len(low_conf)} articles")
            
            if high_conf:
                print(f"   ✅ Will show: {len(high_conf)} high-confidence articles")
            elif medium_conf:
                print(f"   ⚠️ Will show: {min(3, len(medium_conf))} medium-confidence articles (fallback)")
            else:
                print(f"   ❌ No articles meet minimum confidence threshold")
        else:
            print("❌ No constitutional articles found")
        
        print()
        
        # Test legal agent integration
        print("🤖 Legal Agent Integration:")
        try:
            agent = create_legal_agent()
            query_input = LegalQueryInput(user_input=query)
            response = agent.process_query(query_input)
            
            if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                print(f"   ✅ Agent returned {len(response.constitutional_articles)} constitutional articles")
                for article in response.constitutional_articles[:3]:
                    print(f"   • Article {article.get('article_number', 'N/A')}: {article.get('confidence_percentage', 0)}% confidence")
            else:
                print("   ❌ Agent did not return constitutional articles")
                
        except Exception as e:
            print(f"   ❌ Error testing agent: {e}")
        
        print("=" * 60)
        print()

def test_cyber_crime_specific():
    """Test cyber crime specific improvements"""
    
    print("=== CYBER CRIME SPECIFIC TEST ===")
    print()
    
    cyber_queries = [
        "my phone is being hacked",
        "someone hacked my phone",
        "phone hacking by unknown person",
        "my digital privacy is violated",
        "online fraud happened to me"
    ]
    
    for query in cyber_queries:
        print(f"🔍 Query: '{query}'")
        print("-" * 40)
        
        recommendations = get_constitutional_articles_with_confidence(query)
        
        if recommendations and recommendations.get('recommendations'):
            # Check if we get the expected articles for cyber crimes
            expected_articles = ['21', '19', '300A']  # Privacy, communication, digital property
            found_articles = [rec['article_number'] for rec in recommendations['recommendations'][:5]]
            
            print(f"📋 Found Articles: {found_articles}")
            print(f"🎯 Expected Articles: {expected_articles}")
            
            # Check overlap
            overlap = set(found_articles) & set(expected_articles)
            print(f"✅ Overlap: {list(overlap)} ({len(overlap)}/{len(expected_articles)})")
            
            # Show top recommendation
            top_rec = recommendations['recommendations'][0]
            print(f"🏆 Top Match: Article {top_rec['article_number']} ({top_rec['confidence_percentage']}%)")
            print(f"   Title: {top_rec['title']}")
            
        print()

if __name__ == "__main__":
    test_improved_constitutional_articles()
    test_cyber_crime_specific()
    print("✅ Improved constitutional articles test completed!")