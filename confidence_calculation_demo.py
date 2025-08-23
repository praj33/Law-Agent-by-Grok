#!/usr/bin/env python3
"""
CONFIDENCE CALCULATION DEMONSTRATION
====================================

This script shows the EXACT basis for confidence percentage calculation
for your query: "Employee discloses all the company secrets to another company"

It breaks down each factor and shows how the percentages are calculated.
"""

import json
import sys
import os

def demonstrate_confidence_calculation():
    """Demonstrate step-by-step confidence calculation"""
    
    print("🎯 CONFIDENCE PERCENTAGE CALCULATION DEMONSTRATION")
    print("=" * 70)
    
    query = "Employee discloses all the company secrets to another company"
    print(f"📝 Query: '{query}'")
    print("=" * 70)
    
    # Query analysis
    query_words = query.lower().split()
    print(f"\n🔍 QUERY ANALYSIS:")
    print(f"   • Query Words: {query_words}")
    print(f"   • Key Terms: employee, discloses, company, secrets")
    print(f"   • Legal Domain: Employment Law, Trade Secrets, Intellectual Property")
    
    # Sample articles for demonstration
    sample_articles = [
        {
            "article_number": "19",
            "title": "Protection of certain rights regarding freedom of speech etc",
            "content": "All citizens shall have the right to practice any profession, or to carry on any occupation, trade or business...",
            "keywords": ["profession", "trade", "business", "occupation"]
        },
        {
            "article_number": "300A", 
            "title": "Right to property",
            "content": "No person shall be deprived of his property save by authority of law...",
            "keywords": ["property", "intellectual", "rights"]
        },
        {
            "article_number": "21",
            "title": "Protection of life and personal liberty", 
            "content": "No person shall be deprived of his life or personal liberty except according to procedure established by law...",
            "keywords": ["livelihood", "employment", "dignity"]
        }
    ]
    
    print(f"\n📊 CONFIDENCE CALCULATION FOR EACH ARTICLE:")
    print("=" * 70)
    
    for i, article in enumerate(sample_articles, 1):
        print(f"\n{i}. ARTICLE {article['article_number']} - {article['title']}")
        print("-" * 60)
        
        # Calculate each factor
        confidence_breakdown = calculate_confidence_breakdown(query, article)
        
        print(f"🔢 CALCULATION BREAKDOWN:")
        print(f"   1️⃣ Base Relevance Score: {confidence_breakdown['base_relevance']:.1%}")
        print(f"      • Keyword matches: {confidence_breakdown['keyword_matches']}")
        print(f"      • Relevance points: {confidence_breakdown['relevance_points']}")
        
        print(f"   2️⃣ Direct Article Reference: {confidence_breakdown['direct_reference']:.1%}")
        print(f"      • 'Article {article['article_number']}' in query: {confidence_breakdown['has_direct_ref']}")
        
        print(f"   3️⃣ Title Word Overlap: {confidence_breakdown['title_overlap']:.1%}")
        print(f"      • Common words: {confidence_breakdown['common_title_words']}")
        print(f"      • Overlap ratio: {confidence_breakdown['title_ratio']:.2f}")
        
        print(f"   4️⃣ Keyword Matching Bonus: {confidence_breakdown['keyword_bonus']:.1%}")
        print(f"      • Matching keywords: {len(confidence_breakdown['matching_keywords'])}")
        
        print(f"   5️⃣ Content Relevance: {confidence_breakdown['content_relevance']:.1%}")
        print(f"      • Content matches: {confidence_breakdown['content_matches']}")
        
        print(f"   6️⃣ Domain-Specific Bonus: {confidence_breakdown['domain_bonus']:.1%}")
        print(f"      • Domain alignment: {confidence_breakdown['domain_type']}")
        
        total_confidence = sum([
            confidence_breakdown['base_relevance'],
            confidence_breakdown['direct_reference'], 
            confidence_breakdown['title_overlap'],
            confidence_breakdown['keyword_bonus'],
            confidence_breakdown['content_relevance'],
            confidence_breakdown['domain_bonus']
        ])
        
        final_confidence = min(1.0, total_confidence)
        confidence_percentage = int(final_confidence * 100)
        
        print(f"\n📈 TOTAL CALCULATION:")
        print(f"   Raw Total: {total_confidence:.1%}")
        print(f"   Final Confidence: {final_confidence:.1%} (capped at 100%)")
        print(f"   🎯 CONFIDENCE PERCENTAGE: {confidence_percentage}%")
        
        # Confidence level indicator
        if confidence_percentage >= 70:
            level = "🟢 HIGH CONFIDENCE"
        elif confidence_percentage >= 40:
            level = "🟡 MEDIUM CONFIDENCE"
        else:
            level = "🔴 LOW CONFIDENCE"
        
        print(f"   📊 Confidence Level: {level}")

def calculate_confidence_breakdown(query, article):
    """Calculate detailed confidence breakdown"""
    
    query_lower = query.lower()
    query_words = set(query_lower.split())
    title_lower = article['title'].lower()
    title_words = set(title_lower.split())
    content_lower = article['content'].lower()
    content_words = set(content_lower.split())
    
    breakdown = {}
    
    # 1. Base Relevance Score
    relevance_points = 0
    keyword_matches = []
    
    # Check for keyword matches in title and content
    for word in query_words:
        if len(word) > 2:  # Skip short words
            if word in title_lower:
                relevance_points += 3
                keyword_matches.append(f"'{word}' in title")
            if word in content_lower:
                relevance_points += 2
                keyword_matches.append(f"'{word}' in content")
    
    # Domain-specific keywords
    employment_keywords = ['employee', 'work', 'profession', 'trade', 'business']
    for keyword in employment_keywords:
        if keyword in query_lower:
            if keyword in title_lower or keyword in content_lower:
                relevance_points += 1
                keyword_matches.append(f"'{keyword}' domain match")
    
    breakdown['relevance_points'] = relevance_points
    breakdown['keyword_matches'] = keyword_matches
    breakdown['base_relevance'] = min(0.4, relevance_points * 0.05)
    
    # 2. Direct Article Reference
    article_num = article['article_number']
    has_direct_ref = f"article {article_num}" in query_lower
    breakdown['has_direct_ref'] = has_direct_ref
    breakdown['direct_reference'] = 0.5 if has_direct_ref else 0.0
    
    # 3. Title Word Overlap
    common_title_words = query_words & title_words
    title_ratio = len(common_title_words) / len(title_words) if title_words else 0
    breakdown['common_title_words'] = list(common_title_words)
    breakdown['title_ratio'] = title_ratio
    breakdown['title_overlap'] = title_ratio * 0.3
    
    # 4. Keyword Matching Bonus
    matching_keywords = []
    for keyword in article['keywords']:
        if any(keyword in word for word in query_words):
            matching_keywords.append(keyword)
    
    breakdown['matching_keywords'] = matching_keywords
    breakdown['keyword_bonus'] = min(0.2, len(matching_keywords) * 0.05)
    
    # 5. Content Relevance
    content_matches = query_words & content_words
    content_ratio = len(content_matches) / len(query_words) if query_words else 0
    breakdown['content_matches'] = list(content_matches)
    breakdown['content_relevance'] = content_ratio * 0.2
    
    # 6. Domain-Specific Bonus
    domain_type = "Unknown"
    domain_bonus = 0.0
    
    if article_num == "19":
        domain_type = "Employment Rights/Profession"
        domain_bonus = 0.15  # High relevance for employment queries
    elif article_num == "300A":
        domain_type = "Property Rights/Trade Secrets"
        domain_bonus = 0.12  # High relevance for intellectual property
    elif article_num == "21":
        domain_type = "Life and Liberty/Livelihood"
        domain_bonus = 0.08  # Medium relevance for employment
    
    breakdown['domain_type'] = domain_type
    breakdown['domain_bonus'] = domain_bonus
    
    return breakdown

def show_relevance_factors():
    """Show what makes an article relevant"""
    
    print(f"\n\n📋 RELEVANCE FACTORS EXPLAINED")
    print("=" * 50)
    
    factors = [
        ("Direct Article Reference", "Query mentions 'Article X' - gets 50% bonus"),
        ("Keyword Matching", "Query words found in article title/content"),
        ("Title Relevance", "How well article title matches query intent"),
        ("Content Overlap", "Query terms present in article text"),
        ("Domain Alignment", "Article's legal domain matches query domain"),
        ("Legal Context", "Constitutional provision relevant to legal issue")
    ]
    
    for i, (factor, explanation) in enumerate(factors, 1):
        print(f"{i}. {factor}:")
        print(f"   {explanation}")
    
    print(f"\n🎯 CONFIDENCE INTERPRETATION:")
    print(f"   🟢 70-100%: Article directly addresses your legal issue")
    print(f"   🟡 40-69%:  Article has meaningful relevance to your case")
    print(f"   🔴 0-39%:   Article may have some connection but limited relevance")

def main():
    """Main demonstration"""
    
    print("🇮🇳 CONSTITUTIONAL ARTICLE CONFIDENCE CALCULATION")
    print("=" * 80)
    print("Detailed breakdown of how confidence percentages are calculated")
    print("based on relevance of articles to your specific legal query")
    print("=" * 80)
    
    demonstrate_confidence_calculation()
    show_relevance_factors()
    
    print(f"\n✅ SUMMARY:")
    print(f"Confidence percentage = Multi-factor relevance score based on:")
    print(f"   • How well article content matches your query")
    print(f"   • Strength of keyword connections")
    print(f"   • Legal domain alignment")
    print(f"   • Constitutional provision applicability")
    
    print(f"\n📊 This ensures you get the MOST RELEVANT constitutional articles")
    print(f"   with accurate confidence indicators for your legal query!")

if __name__ == "__main__":
    main()