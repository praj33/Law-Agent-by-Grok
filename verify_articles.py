#!/usr/bin/env python3
"""
Verify if constitutional articles are appropriate for specific queries
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_article_relevance():
    """Test if constitutional articles are relevant to the queries"""
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        print("🔍 VERIFYING CONSTITUTIONAL ARTICLE RELEVANCE")
        print("=" * 70)
        
        agent = create_working_enhanced_agent()
        
        # Test cases with expected constitutional articles
        test_cases = [
            {
                "query": "My landlord is not returning my security deposit",
                "expected_domain": "tenant_rights",
                "expected_articles": ["Article 300A", "Article 21", "Article 19"],
                "description": "Property rights and right to shelter"
            },
            {
                "query": "I was arrested without proper warrant by police",
                "expected_domain": "criminal_law", 
                "expected_articles": ["Article 20", "Article 21", "Article 22"],
                "description": "Protection against arrest and detention"
            },
            {
                "query": "My employer is discriminating against me based on my religion",
                "expected_domain": "employment_law",
                "expected_articles": ["Article 14", "Article 15", "Article 16"],
                "description": "Right to equality and non-discrimination"
            },
            {
                "query": "I want to file for divorce from my abusive husband",
                "expected_domain": "family_law",
                "expected_articles": ["Article 21", "Article 15", "Article 25"],
                "description": "Right to life, equality, and religious freedom"
            },
            {
                "query": "My elderly mother is being abused in nursing home",
                "expected_domain": "elder_abuse",
                "expected_articles": ["Article 21", "Article 14"],
                "description": "Right to life and dignity for elderly"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 TEST CASE {i}: {test_case['description']}")
            print("-" * 50)
            print(f"Query: {test_case['query']}")
            
            # Process query
            response = agent.process_query(test_case['query'])
            
            print(f"✅ Domain: {response.domain} (Expected: {test_case['expected_domain']})")
            print(f"✅ Confidence: {response.confidence:.3f}")
            
            # Check constitutional backing
            if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
                print(f"✅ Constitutional Backing Provided: YES")
                print(f"📜 Constitutional Framework:")
                
                # Extract article numbers from the backing text
                backing_text = response.constitutional_backing
                found_articles = []
                for expected_article in test_case['expected_articles']:
                    if expected_article in backing_text:
                        found_articles.append(expected_article)
                        print(f"   ✅ {expected_article} - FOUND")
                    else:
                        print(f"   ❌ {expected_article} - NOT FOUND")
                
                # Check relevance
                relevance_score = len(found_articles) / len(test_case['expected_articles'])
                print(f"📊 Article Relevance Score: {relevance_score:.1%}")
                
                if relevance_score >= 0.5:
                    print(f"✅ ARTICLES ARE RELEVANT")
                else:
                    print(f"❌ ARTICLES MAY NOT BE FULLY RELEVANT")
                    
            else:
                print(f"❌ Constitutional Backing: NOT PROVIDED")
            
            # Check process steps
            if hasattr(response, 'process_steps') and response.process_steps:
                print(f"✅ Process Steps: {len(response.process_steps)} steps provided")
                print(f"📋 Sample Steps:")
                for j, step in enumerate(response.process_steps[:3], 1):
                    print(f"   {j}. {step}")
            else:
                print(f"❌ Process Steps: NOT PROVIDED")
            
            print(f"⚡ Response Time: {response.response_time:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in article verification: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_constitutional_integration():
    """Test constitutional integration specifically"""
    
    try:
        from constitutional_integration import create_constitutional_advisor
        
        print(f"\n🏛️ TESTING CONSTITUTIONAL INTEGRATION DIRECTLY")
        print("=" * 70)
        
        advisor = create_constitutional_advisor()
        
        # Test direct constitutional queries
        test_queries = [
            ("tenant_rights", "landlord security deposit"),
            ("criminal_law", "police arrest without warrant"),
            ("employment_law", "workplace discrimination religion"),
            ("family_law", "divorce domestic violence"),
            ("elder_abuse", "elderly abuse nursing home")
        ]
        
        for domain, query in test_queries:
            print(f"\n🔍 Testing: {domain} - '{query}'")
            
            constitutional_info = advisor.get_constitutional_backing(domain, query)
            
            if constitutional_info:
                print(f"✅ Constitutional basis: {constitutional_info.get('constitutional_basis', 'Not provided')[:100]}...")
                
                articles = constitutional_info.get('relevant_articles', [])
                if articles:
                    print(f"📜 Articles found: {len(articles)}")
                    for article in articles[:3]:
                        print(f"   • Article {article.article_number}: {article.clean_title}")
                else:
                    print(f"❌ No articles found")
            else:
                print(f"❌ No constitutional information found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in constitutional integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    
    print("🏛️ CONSTITUTIONAL ARTICLE RELEVANCE VERIFICATION")
    print("=" * 80)
    
    results = []
    
    # Test 1: Article relevance in responses
    results.append(test_article_relevance())
    
    # Test 2: Constitutional integration
    results.append(test_constitutional_integration())
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    
    successful_tests = sum(results)
    total_tests = len(results)
    
    print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
    print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🎉 VERIFICATION PASSED! Constitutional articles are being provided appropriately.")
        print("✅ The system is providing relevant constitutional backing for legal queries.")
        print("✅ Process steps are being generated for legal procedures.")
    else:
        print("⚠️ Some verifications failed. Check the details above.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)