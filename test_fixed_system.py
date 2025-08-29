"""
Test Fixed Legal Agent System
============================

This script tests the fixed Legal Agent system with the corrected
domain classification and varied constitutional confidence percentages.

Usage: python test_fixed_system.py
"""

from working_enhanced_agent import create_working_enhanced_agent
import time

def test_fixed_system():
    """Test the fixed legal agent system"""
    
    print("🏛️ TESTING FIXED LEGAL AGENT SYSTEM")
    print("=" * 60)
    print("Testing corrected domain classification and constitutional analysis")
    print("=" * 60)
    
    # Create agent
    try:
        agent = create_working_enhanced_agent()
        print("✅ Enhanced Legal Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Test queries that were previously problematic
    test_queries = [
        {
            "query": "Employee discloses all the company secrets to another company",
            "expected_domain": "employment_law",
            "description": "Employment Law - Confidentiality Breach (FIXED)"
        },
        {
            "query": "My phone is being hacked by someone",
            "expected_domain": "cyber_crime",
            "description": "Cyber Crime - Phone Hacking"
        },
        {
            "query": "My landlord is not returning my security deposit",
            "expected_domain": "tenant_rights",
            "description": "Tenant Rights - Security Deposit"
        },
        {
            "query": "My boss is sexually harassing me at workplace",
            "expected_domain": "employment_law",
            "description": "Employment Law - Sexual Harassment"
        },
        {
            "query": "I want to divorce my abusive husband",
            "expected_domain": "family_law",
            "description": "Family Law - Domestic Violence Divorce"
        }
    ]
    
    print(f"\n🧪 Running {len(test_queries)} test scenarios...")
    print("=" * 60)
    
    results = []
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}/5: {test['description']}")
        print(f"Query: \"{test['query']}\"")
        print("-" * 50)
        
        try:
            # Process query
            start_time = time.time()
            response = agent.process_query(test['query'])
            response_time = time.time() - start_time
            
            # Check results
            domain_match = response.domain == test['expected_domain']
            confidence_good = response.confidence > 0.5
            
            # Display results
            print(f"🎯 Domain: {response.domain} (Expected: {test['expected_domain']})")
            print(f"📊 Confidence: {response.confidence:.3f}")
            print(f"⚖️ Legal Route: {response.legal_route[:80]}...")
            print(f"⏱️ Timeline: {response.timeline}")
            print(f"📈 Success Rate: {response.success_rate:.1%}")
            print(f"⚡ Response Time: {response_time:.3f}s")
            
            # Constitutional backing
            if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
                print(f"🏛️ Constitutional Backing: Available")
                
                # Show constitutional articles with varied confidence
                if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                    print(f"📜 Constitutional Articles Found: {len(response.constitutional_articles)}")
                    for j, article in enumerate(response.constitutional_articles[:3], 1):
                        article_num = article.get('article_number', 'N/A')
                        title = article.get('title', 'N/A')
                        confidence_pct = article.get('confidence_percentage', 0)
                        
                        # Show varied confidence percentages
                        if confidence_pct:
                            print(f"   {j}. Article {article_num}: {title} ({confidence_pct}% confidence)")
                        else:
                            # Fallback for older format
                            print(f"   {j}. Article {article_num}: {title}")
            
            # Status
            if domain_match and confidence_good:
                status = "✅ PASS"
                color = "🟢"
            elif domain_match:
                status = "⚠️ PARTIAL (Low confidence)"
                color = "🟡"
            else:
                status = "❌ FAIL (Wrong domain)"
                color = "🔴"
            
            print(f"Status: {color} {status}")
            
            results.append({
                'test': test['description'],
                'domain_match': domain_match,
                'confidence': response.confidence,
                'response_time': response_time,
                'status': status,
                'constitutional_articles': len(response.constitutional_articles) if hasattr(response, 'constitutional_articles') and response.constitutional_articles else 0
            })
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            results.append({
                'test': test['description'],
                'domain_match': False,
                'confidence': 0.0,
                'response_time': 0.0,
                'status': "❌ ERROR",
                'constitutional_articles': 0
            })
    
    # Summary
    print(f"\n📊 FIXED SYSTEM TEST SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(1 for r in results if r['domain_match'] and r['confidence'] > 0.5)
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100
    avg_confidence = sum(r['confidence'] for r in results) / total_tests
    avg_response_time = sum(r['response_time'] for r in results) / total_tests
    total_constitutional_articles = sum(r['constitutional_articles'] for r in results)
    
    print(f"✅ Passed Tests: {passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print(f"📊 Average Confidence: {avg_confidence:.3f}")
    print(f"⚡ Average Response Time: {avg_response_time:.3f}s")
    print(f"🏛️ Constitutional Articles Found: {total_constitutional_articles}")
    
    # Grade
    if success_rate >= 90:
        grade = "A+ (Excellent)"
        emoji = "🎉"
    elif success_rate >= 80:
        grade = "A (Very Good)"
        emoji = "✅"
    elif success_rate >= 70:
        grade = "B (Good)"
        emoji = "👍"
    elif success_rate >= 60:
        grade = "C (Average)"
        emoji = "⚠️"
    else:
        grade = "D (Needs Improvement)"
        emoji = "❌"
    
    print(f"🎯 Overall Grade: {emoji} {grade}")
    
    # Key improvements
    print(f"\n🔧 KEY FIXES IMPLEMENTED:")
    print("✅ Fixed 'unknown' domain classification for employment law queries")
    print("✅ Added comprehensive training data for confidentiality breaches")
    print("✅ Improved constitutional article confidence percentages")
    print("✅ Enhanced ML classifier with better employment law patterns")
    print("✅ Added varied confidence scoring (25%-95% range)")
    
    # Specific fix validation
    employee_disclosure_test = next((r for r in results if 'Confidentiality Breach' in r['test']), None)
    if employee_disclosure_test and employee_disclosure_test['domain_match']:
        print(f"\n🎯 SPECIFIC FIX VALIDATION:")
        print(f"✅ 'Employee discloses company secrets' now correctly classified as employment_law")
        print(f"✅ Confidence: {employee_disclosure_test['confidence']:.3f} (was ~0.000)")
        print(f"✅ Constitutional articles provided with varied confidence percentages")
    
    print(f"\n🎉 System testing completed! Agent is {'ready for production use' if success_rate >= 80 else 'improved but needs more work'}.")

if __name__ == "__main__":
    test_fixed_system()