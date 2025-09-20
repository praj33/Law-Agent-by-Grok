#!/usr/bin/env python3
"""
Constitutional Article Analysis Demo
===================================

This script demonstrates the enhanced constitutional article matching functionality
with confidence percentages and comprehensive article analysis.

Features:
- Shows specific constitutional articles with confidence scores
- Analyzes all 140+ articles from article.json 
- Provides detailed relevance scoring and keyword matching
- Demonstrates structured output format with constitutional backing

Usage:
    python test_constitutional_analysis.py
"""

import sys
import os
from typing import Dict, Any

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adaptive_agent import create_adaptive_agent
from legal_agent import LegalQueryInput
from constitutional_article_matcher import (
    get_constitutional_articles_with_confidence,
    format_article_recommendations,
    constitutional_matcher
)


def test_constitutional_matching():
    """Test constitutional article matching with various queries"""
    
    print("🏛️ CONSTITUTIONAL ARTICLE MATCHING TEST")
    print("=" * 60)
    
    test_queries = [
        "my phone is being hacked",
        "landlord not returning security deposit",
        "workplace harassment by colleague", 
        "fundamental rights violation",
        "freedom of speech",
        "right to education",
        "discrimination based on caste",
        "president powers",
        "supreme court jurisdiction",
        "election commission duties"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: '{query}'")
        print("-" * 50)
        
        # Get constitutional analysis
        analysis = get_constitutional_articles_with_confidence(query)
        
        # Display summary
        print(f"📊 Search Results:")
        print(f"   • Articles Searched: {analysis['total_articles_searched']}")
        print(f"   • Matching Articles: {analysis['matching_articles']}")
        
        if analysis['matching_articles'] > 0:
            print(f"   • Top Confidence: {analysis['confidence_summary']['top_match_confidence']}%")
            print(f"   • Primary Domains: {', '.join(analysis['query_analysis']['primary_domains'])}")
            
            print(f"\n🎯 Top 3 Constitutional Articles:")
            for j, rec in enumerate(analysis['recommendations'][:3], 1):
                conf_icon = "🟢" if rec['confidence_percentage'] >= 70 else "🟡" if rec['confidence_percentage'] >= 40 else "🔴"
                print(f"   {conf_icon} {j}. Article {rec['article_number']} - {rec['confidence_percentage']}% confidence")
                print(f"      📖 {rec['title']}")
                print(f"      🔍 Keywords: {', '.join(rec['matching_keywords'][:3])}")
                if rec['match_reasons']:
                    print(f"      💡 {rec['match_reasons'][0]}")
        else:
            print("   ❌ No matching constitutional articles found")
        
        print()


def test_structured_output_with_articles():
    """Test structured output format with constitutional article integration"""
    
    print("\n🏛️ STRUCTURED OUTPUT WITH CONSTITUTIONAL ARTICLES")
    print("=" * 60)
    
    # Create adaptive agent
    agent = create_adaptive_agent()
    
    test_query = "my landlord is not returning my security deposit"
    
    print(f"🔍 Testing Query: '{test_query}'")
    print("-" * 50)
    
    # Create query input
    query_input = LegalQueryInput(user_input=test_query)
    
    try:
        # Get structured response with constitutional articles
        structured_response = agent.process_query_with_structured_output(query_input)
        print(structured_response)
        
    except Exception as e:
        print(f"❌ Error: {e}")


def test_separate_constitutional_analysis():
    """Test separate constitutional analysis functionality"""
    
    print("\n🏛️ SEPARATE CONSTITUTIONAL ANALYSIS")
    print("=" * 60)
    
    # Create adaptive agent
    agent = create_adaptive_agent()
    
    test_queries = [
        "fundamental rights violation",
        "freedom of expression censorship",
        "election rigging complaint"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Constitutional Analysis for: '{query}'")
        print("-" * 50)
        
        try:
            # Get formatted constitutional analysis
            analysis = agent.get_formatted_constitutional_analysis(query)
            print(analysis)
            
        except Exception as e:
            print(f"❌ Error: {e}")


def test_confidence_calculation():
    """Test confidence calculation algorithm"""
    
    print("\n🎯 CONFIDENCE CALCULATION ANALYSIS")
    print("=" * 60)
    
    # Test specific article references
    test_cases = [
        ("Article 21 violation", "Should show very high confidence for Article 21"),
        ("freedom of speech restriction", "Should match Article 19 with high confidence"),
        ("discrimination in employment", "Should match Articles 14, 15, 16"),
        ("cyber crime hacking", "Should match Article 21 (privacy)")
    ]
    
    for query, expected in test_cases:
        print(f"\n🔍 Query: '{query}'")
        print(f"💭 Expected: {expected}")
        
        analysis = get_constitutional_articles_with_confidence(query)
        
        if analysis['matching_articles'] > 0:
            top_match = analysis['recommendations'][0]
            print(f"✅ Result: Article {top_match['article_number']} - {top_match['confidence_percentage']}% confidence")
            print(f"📝 Title: {top_match['title']}")
            print(f"🔍 Keywords: {', '.join(top_match['matching_keywords'])}")
        else:
            print("❌ No matches found")


def show_database_stats():
    """Show constitutional database statistics"""
    
    print("\n📊 CONSTITUTIONAL DATABASE STATISTICS")
    print("=" * 60)
    
    print(f"📚 Total Articles in Database: {len(constitutional_matcher.articles)}")
    
    # Count articles by range
    article_ranges = {
        "Territory & Union (1-4)": 0,
        "Citizenship (5-11)": 0,
        "Fundamental Rights (12-35)": 0,
        "Directive Principles (36-51)": 0,
        "Government Structure (52-123)": 0,
        "Judiciary (124-147)": 0,
        "State Government (153-200)": 0,
        "High Courts (214-231)": 0,
        "Elections (324-329)": 0,
        "Language (343-351)": 0,
        "Emergency (352-360)": 0,
        "Amendment (368)": 0,
        "Special Provisions (370+)": 0
    }
    
    for article in constitutional_matcher.articles:
        article_num = int(article['article_number'])
        
        if 1 <= article_num <= 4:
            article_ranges["Territory & Union (1-4)"] += 1
        elif 5 <= article_num <= 11:
            article_ranges["Citizenship (5-11)"] += 1
        elif 12 <= article_num <= 35:
            article_ranges["Fundamental Rights (12-35)"] += 1
        elif 36 <= article_num <= 51:
            article_ranges["Directive Principles (36-51)"] += 1
        elif 52 <= article_num <= 123:
            article_ranges["Government Structure (52-123)"] += 1
        elif 124 <= article_num <= 147:
            article_ranges["Judiciary (124-147)"] += 1
        elif 153 <= article_num <= 200:
            article_ranges["State Government (153-200)"] += 1
        elif 214 <= article_num <= 231:
            article_ranges["High Courts (214-231)"] += 1
        elif 324 <= article_num <= 329:
            article_ranges["Elections (324-329)"] += 1
        elif 343 <= article_num <= 351:
            article_ranges["Language (343-351)"] += 1
        elif 352 <= article_num <= 360:
            article_ranges["Emergency (352-360)"] += 1
        elif article_num == 368:
            article_ranges["Amendment (368)"] += 1
        elif article_num >= 370:
            article_ranges["Special Provisions (370+)"] += 1
    
    print("\n📋 Articles by Category:")
    for category, count in article_ranges.items():
        if count > 0:
            print(f"   • {category}: {count} articles")
    
    print(f"\n🎯 Database Coverage:")
    print(f"   • Complete Fundamental Rights coverage")
    print(f"   • Comprehensive Government Structure")
    print(f"   • Full Judiciary framework")
    print(f"   • Election & Language provisions")
    print(f"   • Emergency & Amendment procedures")


def main():
    """Run comprehensive constitutional analysis demonstration"""
    
    print("🇮🇳 CONSTITUTIONAL ARTICLE ANALYSIS SYSTEM")
    print("=" * 70)
    print("Demonstrating enhanced constitutional article matching with confidence scores")
    print("Searching through 140+ constitutional articles with AI-powered relevance scoring")
    print("=" * 70)
    
    try:
        # Show database statistics
        show_database_stats()
        
        # Test constitutional matching
        test_constitutional_matching()
        
        # Test confidence calculation
        test_confidence_calculation()
        
        # Test structured output integration
        test_structured_output_with_articles()
        
        # Test separate constitutional analysis
        test_separate_constitutional_analysis()
        
        print(f"\n✅ CONSTITUTIONAL ANALYSIS SYSTEM READY!")
        print(f"🏛️ Your legal agent now provides:")
        print(f"   • Specific constitutional articles with confidence percentages")
        print(f"   • Comprehensive search through all {len(constitutional_matcher.articles)} articles")
        print(f"   • Detailed relevance scoring and keyword matching")
        print(f"   • Integration with structured legal guidance")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()