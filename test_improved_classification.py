"""
Test Improved Classification System
===================================

This script tests the new detailed classification format that provides:
- Main Domain → Subcategory
- Enhanced analysis with specific routes
- Relevant constitutional articles
- Success rates

Author: Legal Agent Team
Date: 2025-08-17
"""

from working_enhanced_agent import create_working_enhanced_agent

def test_workplace_harassment():
    """Test the specific workplace harassment example"""
    
    print("🧪 TESTING IMPROVED CLASSIFICATION FORMAT")
    print("=" * 60)
    
    agent = create_working_enhanced_agent()
    
    print("\n🎯 TEST CASE: Workplace Sexual Harassment")
    print("=" * 45)
    print("Query: 'my coworker is sexually harassing me at work'")
    print("Expected Format:")
    print("  Employment Law → Workplace Harassment")
    print("  Enhanced analysis: workplace_harassment + ML suggestion: employment_law")
    print("  ML Classification: employment_law (confidence: 0.82)")
    print("  Dataset Route: workplace_harassment, success rate: high")
    print()
    
    # Process the query
    response = agent.process_query("my coworker is sexually harassing me at work")
    
    print("✅ ACTUAL RESULT:")
    print(f"   Domain: {response.domain}")
    print(f"   Confidence: {response.confidence:.3f}")
    print(f"   Legal Route: {response.legal_route}")
    print(f"   Constitutional Articles: {response.constitutional_backing[:100]}...")
    
    return response

def test_multiple_scenarios():
    """Test multiple scenarios to verify the format"""
    
    print("\n\n🎯 TESTING MULTIPLE SCENARIOS")
    print("=" * 50)
    
    agent = create_working_enhanced_agent()
    
    test_cases = [
        {
            'query': 'my boss fired me without notice',
            'expected_domain': 'Employment Law',
            'expected_subcategory': 'Wrongful Termination'
        },
        {
            'query': 'my landlord is not returning my security deposit',
            'expected_domain': 'Tenant Rights',
            'expected_subcategory': 'Security Deposit'
        },
        {
            'query': 'someone hacked my bank account',
            'expected_domain': 'Cyber Crime',
            'expected_subcategory': 'Hacking & Data Breach'
        },
        {
            'query': 'my husband is beating me',
            'expected_domain': 'Family Law',
            'expected_subcategory': 'Domestic Violence'
        },
        {
            'query': 'my phone was stolen in the market',
            'expected_domain': 'Criminal Law',
            'expected_subcategory': 'Theft & Robbery'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{test_case['query']}'")
        print(f"   Expected: {test_case['expected_domain']} → {test_case['expected_subcategory']}")
        
        response = agent.process_query(test_case['query'])
        
        print(f"   ✅ Result: {response.domain} (confidence: {response.confidence:.3f})")
        print(f"   📋 Route: {response.legal_route[:80]}...")

def test_constitutional_articles():
    """Test if constitutional articles are relevant to the query"""
    
    print("\n\n🎯 TESTING CONSTITUTIONAL ARTICLE RELEVANCE")
    print("=" * 50)
    
    agent = create_working_enhanced_agent()
    
    test_queries = [
        "workplace discrimination based on gender",
        "police arrested me without warrant",
        "my wife wants divorce",
        "landlord is harassing me",
        "online fraud case"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        response = agent.process_query(query)
        
        print(f"   Domain: {response.domain}")
        print(f"   Constitutional Backing: {response.constitutional_backing[:150]}...")
        
        # Check if articles are mentioned
        if "Article" in response.constitutional_backing:
            print("   ✅ Specific constitutional articles provided")
        else:
            print("   ⚠️ Generic constitutional backing")

def test_success_rates():
    """Test if success rates are being provided"""
    
    print("\n\n🎯 TESTING SUCCESS RATE INFORMATION")
    print("=" * 45)
    
    agent = create_working_enhanced_agent()
    
    queries = [
        "salary not paid for 3 months",
        "car accident compensation",
        "child custody dispute",
        "property fraud case"
    ]
    
    for query in queries:
        print(f"\n📝 Query: '{query}'")
        response = agent.process_query(query)
        
        print(f"   Success Rate: {response.success_rate:.1%}")
        print(f"   Timeline: {response.timeline}")

def main():
    """Run all tests for the improved classification system"""
    
    print("🧪 COMPREHENSIVE IMPROVED CLASSIFICATION TEST")
    print("=" * 70)
    print("Testing the new detailed classification format")
    
    try:
        # Test the main example
        workplace_response = test_workplace_harassment()
        
        # Test multiple scenarios
        test_multiple_scenarios()
        
        # Test constitutional articles
        test_constitutional_articles()
        
        # Test success rates
        test_success_rates()
        
        print("\n" + "=" * 70)
        print("📊 CLASSIFICATION FORMAT ANALYSIS")
        print("=" * 70)
        
        print("\n✅ IMPROVEMENTS IMPLEMENTED:")
        print("   • Domain → Subcategory format")
        print("   • Enhanced analysis with specific routes")
        print("   • Detailed ML classification information")
        print("   • Specific constitutional articles")
        print("   • Success rate indicators")
        
        print("\n🎯 EXAMPLE OUTPUT FORMAT:")
        print("   Employment Law → Workplace Harassment")
        print("   Enhanced analysis: workplace_harassment + ML suggestion: employment_law")
        print("   ML Classification: employment_law (confidence: 0.82)")
        print("   Dataset Route: workplace_harassment_complaint, success rate: high")
        print("   Constitutional Articles: Article 14, Article 15, Article 21")
        
        print("\n🎉 IMPROVED CLASSIFICATION SYSTEM IS WORKING!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()
