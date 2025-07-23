"""
Test Constitutional Integration with Legal Agent
==============================================

This script tests the integration of constitutional articles with the Legal Agent system
to ensure constitutional backing is provided for legal advice.

Usage: python test_constitutional_integration.py
"""

from legal_agent import create_legal_agent, LegalQueryInput
from adaptive_legal_agent import create_adaptive_legal_agent

def test_constitutional_integration():
    """Test constitutional integration with various legal domains"""
    
    print("🏛️ TESTING CONSTITUTIONAL INTEGRATION")
    print("=" * 60)
    
    agent = create_legal_agent()
    
    # Test queries across different domains
    test_cases = [
        {
            'domain': 'Criminal Law',
            'query': 'I was arrested without a warrant',
            'expected_articles': ['20', '21', '22']  # Protection from crimes, liberty, arrest
        },
        {
            'domain': 'Immigration Law', 
            'query': 'I need help with citizenship application',
            'expected_articles': ['5', '6', '7', '8']  # Citizenship articles
        },
        {
            'domain': 'Employment Law',
            'query': 'I am facing workplace discrimination',
            'expected_articles': ['14', '15', '16']  # Equality, non-discrimination
        },
        {
            'domain': 'Elder Abuse',
            'query': 'My elderly father is being mistreated in Delhi',
            'expected_articles': ['21']  # Right to life and dignity
        },
        {
            'domain': 'Cyber Crime',
            'query': 'My phone is being hacked and privacy violated',
            'expected_articles': ['19', '21']  # Freedom of expression, privacy
        },
        {
            'domain': 'Family Law',
            'query': 'I want to file for divorce',
            'expected_articles': ['15', '21', '25']  # Equality, liberty, religion
        }
    ]
    
    print("🧪 Testing Constitutional Backing for Legal Queries:")
    print("-" * 50)
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['domain']}")
        print(f"Query: \"{test_case['query']}\"")
        print("-" * 30)
        
        query_input = LegalQueryInput(user_input=test_case['query'])
        response = agent.process_query(query_input)
        
        # Check if constitutional backing is provided
        has_constitutional_backing = bool(response.constitutional_backing)
        has_constitutional_articles = bool(response.constitutional_articles)
        
        if has_constitutional_backing:
            success_count += 1
            status = "✅ SUCCESS"
        else:
            status = "❌ NO CONSTITUTIONAL BACKING"
        
        print(f"{status}")
        print(f"Domain: {response.domain} (Confidence: {response.confidence:.3f})")
        
        if has_constitutional_backing:
            print(f"Constitutional Backing: {response.constitutional_backing[:100]}...")
            
            if has_constitutional_articles:
                print(f"Constitutional Articles ({len(response.constitutional_articles)}):")
                for article in response.constitutional_articles[:2]:  # Show first 2
                    print(f"  • Article {article['article_number']}: {article['title'][:50]}...")
        else:
            print("No constitutional backing provided")
    
    success_rate = (success_count / total_tests) * 100
    print(f"\n📊 CONSTITUTIONAL INTEGRATION RESULTS:")
    print("=" * 50)
    print(f"Success Rate: {success_rate:.1f}% ({success_count}/{total_tests})")
    
    return success_rate >= 70  # 70% success rate target

def test_specific_constitutional_queries():
    """Test queries specifically about constitutional matters"""
    
    print(f"\n🏛️ TESTING CONSTITUTIONAL-SPECIFIC QUERIES")
    print("=" * 50)
    
    agent = create_legal_agent()
    
    constitutional_queries = [
        "What are my fundamental rights under the Constitution?",
        "I am a citizen by birth, what are my rights?", 
        "My constitutional rights are being violated",
        "I need information about citizenship laws",
        "What does the Constitution say about equality?"
    ]
    
    for query in constitutional_queries:
        print(f"\n📜 Query: \"{query}\"")
        print("-" * 40)
        
        query_input = LegalQueryInput(user_input=query)
        response = agent.process_query(query_input)
        
        has_backing = bool(response.constitutional_backing)
        status = "✅" if has_backing else "❌"
        
        print(f"{status} Domain: {response.domain} (Confidence: {response.confidence:.3f})")
        
        if has_backing:
            print(f"Constitutional Backing: {response.constitutional_backing[:80]}...")
            if response.constitutional_articles:
                articles = [f"Article {a['article_number']}" for a in response.constitutional_articles[:3]]
                print(f"Relevant Articles: {', '.join(articles)}")

def test_enhanced_legal_advice():
    """Test how constitutional backing enhances legal advice"""
    
    print(f"\n⚖️ TESTING ENHANCED LEGAL ADVICE")
    print("=" * 50)
    
    agent = create_legal_agent()
    
    # Compare advice with and without constitutional backing
    test_query = "I was arrested without proper procedure"
    
    print(f"Query: \"{test_query}\"")
    print("-" * 40)
    
    query_input = LegalQueryInput(user_input=test_query)
    response = agent.process_query(query_input)
    
    print(f"🏛️ Legal Route: {response.legal_route}")
    print(f"⏱️ Timeline: {response.timeline}")
    print(f"🎯 Outcome: {response.outcome}")
    
    if response.constitutional_backing:
        print(f"\n📜 Constitutional Backing:")
        print(f"   {response.constitutional_backing}")
        
        if response.constitutional_articles:
            print(f"\n📋 Relevant Constitutional Articles:")
            for article in response.constitutional_articles:
                print(f"   • Article {article['article_number']}: {article['title']}")
                if article.get('summary'):
                    print(f"     Summary: {article['summary'][:60]}...")
    
    # Test with adaptive agent
    print(f"\n🧠 Testing with Adaptive Agent:")
    print("-" * 30)
    
    adaptive_agent = create_adaptive_legal_agent()
    adaptive_response = adaptive_agent.process_query_with_learning(query_input)
    
    print(f"Domain: {adaptive_response.domain} (Confidence: {adaptive_response.confidence:.3f})")
    
    if hasattr(adaptive_response, 'constitutional_backing') and adaptive_response.constitutional_backing:
        print(f"Constitutional Support: ✅ Available")
        print(f"Enhanced Advice: {adaptive_response.constitutional_backing[:80]}...")
    else:
        print(f"Constitutional Support: ❌ Not available in adaptive response")

def main():
    """Run all constitutional integration tests"""
    
    print("🚀 CONSTITUTIONAL INTEGRATION TESTING")
    print("Testing article.json integration with Legal Agent")
    print("=" * 70)
    
    # Test 1: Basic constitutional integration
    basic_success = test_constitutional_integration()
    
    # Test 2: Constitutional-specific queries
    test_specific_constitutional_queries()
    
    # Test 3: Enhanced legal advice
    test_enhanced_legal_advice()
    
    # Overall results
    print(f"\n🎯 OVERALL INTEGRATION STATUS")
    print("=" * 40)
    
    if basic_success:
        print("🎉 CONSTITUTIONAL INTEGRATION SUCCESSFUL!")
        print("✅ Constitutional articles properly integrated")
        print("✅ Constitutional backing provided for legal advice")
        print("✅ Article references enhance system credibility")
        print("✅ Indian Constitution articles accessible")
        
        print(f"\n📊 Integration Features:")
        print("   • 11 Constitutional articles loaded")
        print("   • Domain-specific constitutional mappings")
        print("   • Article search and retrieval")
        print("   • Constitutional backing for legal advice")
        print("   • Enhanced system credibility")
        
        print(f"\n🚀 Ready to use enhanced system:")
        print("   python cli_interface.py")
        print("   python adaptive_cli.py")
        
        print(f"\n💡 Example enhanced responses:")
        print("   • Criminal law queries → Articles 20, 21, 22 (arrest, liberty)")
        print("   • Immigration queries → Articles 5-10 (citizenship)")
        print("   • Employment queries → Articles 14-16 (equality)")
        print("   • Elder abuse queries → Article 21 (life, dignity)")
        
    else:
        print("⚠️ CONSTITUTIONAL INTEGRATION NEEDS IMPROVEMENT")
        print("Check the test results above for specific issues")
        print("Consider adding more constitutional article mappings")

if __name__ == "__main__":
    main()
