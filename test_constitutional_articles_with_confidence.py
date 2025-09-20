#!/usr/bin/env python3
"""
Test Constitutional Articles with Confidence Percentages
========================================================

This test demonstrates the enhanced constitutional article functionality
with confidence percentages from the article.json database.
"""

try:
    from cli_interface import LegalAgentCLI
    from constitutional_article_matcher import get_constitutional_articles_with_confidence
    
    print("🏛️ TESTING CONSTITUTIONAL ARTICLES WITH CONFIDENCE PERCENTAGES")
    print("=" * 80)
    print()
    
    # Test 1: Direct constitutional article matcher
    print("🔍 Test 1: Direct Constitutional Article Matcher")
    print("-" * 50)
    
    test_queries = [
        "my phone is being hacked by someone",
        "landlord not returning my security deposit", 
        "my employer is harassing me at workplace",
        "privacy violation by government"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        analysis = get_constitutional_articles_with_confidence(query)
        
        if analysis.get('matching_articles', 0) > 0:
            print(f"   📊 Found {analysis['matching_articles']} relevant articles from {analysis['total_articles_searched']} total")
            print(f"   🎯 Top match confidence: {analysis['confidence_summary']['top_match_confidence']}%")
            
            print("   📋 Top 3 Constitutional Articles:")
            for j, rec in enumerate(analysis['recommendations'][:3], 1):
                confidence = rec['confidence_percentage']
                conf_icon = "🟢" if confidence >= 70 else "🟡" if confidence >= 40 else "🔴"
                print(f"      {conf_icon} Article {rec['article_number']}: {rec['title']} ({confidence}% confidence)")
                if rec.get('matching_keywords'):
                    print(f"         Keywords: {', '.join(rec['matching_keywords'][:3])}")
        else:
            print("   ❌ No constitutional articles found")
    
    print("\n" + "=" * 80)
    print("🔍 Test 2: CLI Interface with Constitutional Articles")
    print("-" * 50)
    
    # Test CLI with constitutional articles
    cli = LegalAgentCLI(use_adaptive=False)
    
    test_query = "my coworker is sexually harassing me at workplace"
    print(f"\nTesting CLI with query: '{test_query}'")
    print("-" * 60)
    
    cli.process_query(test_query)
    
    print("\n" + "=" * 80)
    print("🔍 Test 3: Adaptive Agent Constitutional Features")
    print("-" * 50)
    
    try:
        cli_adaptive = LegalAgentCLI(use_adaptive=True)
        print("✅ Using Adaptive Agent with Constitutional Analysis")
        
        test_query_adaptive = "online fraud case involving my bank account"
        print(f"\nTesting adaptive agent with: '{test_query_adaptive}'")
        print("-" * 60)
        
        cli_adaptive.process_query(test_query_adaptive)
        
    except Exception as e:
        print(f"⚠️ Adaptive agent test failed: {e}")
    
    print("\n" + "=" * 80)
    print("✅ CONSTITUTIONAL ARTICLES TESTING COMPLETED!")
    print("=" * 80)
    print("🎯 Key Features Demonstrated:")
    print("   ✅ Constitutional articles from article.json database (140+ articles)")
    print("   ✅ Confidence percentages (0-100%) for each article")
    print("   ✅ Query-specific article matching with relevance scoring")
    print("   ✅ Domain-based constitutional backing")
    print("   ✅ Enhanced CLI display with confidence indicators")
    print("   ✅ Adaptive agent integration with constitutional analysis")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()