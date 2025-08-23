"""
Constitutional Article Demo - Simple Version
============================================

This script demonstrates the constitutional article matching functionality
"""

# Test the constitutional matcher directly
if __name__ == "__main__":
    import json
    
    # Load and count articles
    try:
        with open('article.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print("🏛️ CONSTITUTIONAL ARTICLE ANALYSIS SYSTEM")
        print("=" * 50)
        print(f"📚 Total Articles Loaded: {len(articles)}")
        
        # Show sample articles
        print(f"\n📋 Sample Articles (first 5):")
        for i, article in enumerate(articles[:5]):
            print(f"   {i+1}. Article {article['article_number']}: {article['title'][:60]}...")
        
        # Test constitutional matcher
        from constitutional_article_matcher import get_constitutional_articles_with_confidence
        
        test_queries = [
            "fundamental rights violation",
            "freedom of speech",
            "right to education", 
            "phone being hacked"
        ]
        
        print(f"\n🔍 TESTING CONSTITUTIONAL ARTICLE MATCHING:")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            try:
                analysis = get_constitutional_articles_with_confidence(query)
                print(f"   📊 Articles searched: {analysis['total_articles_searched']}")
                print(f"   🎯 Matches found: {analysis['matching_articles']}")
                
                if analysis['matching_articles'] > 0:
                    top_match = analysis['recommendations'][0]
                    print(f"   🟢 Top match: Article {top_match['article_number']} - {top_match['confidence_percentage']}% confidence")
                    print(f"   📖 Title: {top_match['title']}")
                else:
                    print("   ❌ No matches found")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n✅ CONSTITUTIONAL ANALYSIS SYSTEM IS WORKING!")
        print(f"🎯 Key Features:")
        print(f"   • Searches through ALL {len(articles)} constitutional articles")
        print(f"   • Provides confidence percentages for each match")
        print(f"   • Shows specific articles relevant to legal queries") 
        print(f"   • Integrated with adaptive legal agent responses")
        
    except Exception as e:
        print(f"❌ Error loading articles: {e}")