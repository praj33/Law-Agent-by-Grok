"""
Simple Agent Testing Script
==========================

This script provides an easy way to test the Legal Agent with predefined queries.
Perfect for quick validation and demonstration.

Usage: python test_agent_simple.py
"""

from working_enhanced_agent import create_working_enhanced_agent
import time

def test_agent_with_queries():
    """Test agent with a variety of legal queries"""
    
    print("🏛️ LEGAL AGENT TESTING SCRIPT")
    print("=" * 50)
    print("Initializing Enhanced Legal Agent...")
    
    # Create agent
    try:
        agent = create_working_enhanced_agent()
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Test queries with expected domains
    test_queries = [
        {
            "query": "My landlord is not returning my security deposit of Rs. 50,000",
            "expected_domain": "tenant_rights",
            "description": "Tenant Rights - Security Deposit"
        },
        {
            "query": "My boss is sexually harassing me at workplace",
            "expected_domain": "employment_law", 
            "description": "Employment Law - Workplace Harassment"
        },
        {
            "query": "I bought a defective smartphone and want refund",
            "expected_domain": "consumer_complaint",
            "description": "Consumer Complaint - Defective Product"
        },
        {
            "query": "Someone stole my phone at the railway station",
            "expected_domain": "criminal_law",
            "description": "Criminal Law - Theft"
        },
        {
            "query": "My social media account was hacked and money stolen",
            "expected_domain": "cyber_crime",
            "description": "Cyber Crime - Account Hacking"
        },
        {
            "query": "I want to divorce my husband due to domestic violence",
            "expected_domain": "family_law",
            "description": "Family Law - Divorce"
        }
    ]
    
    print(f"\n🧪 Running {len(test_queries)} test scenarios...")
    print("=" * 50)
    
    results = []
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}/6: {test['description']}")
        print(f"Query: \"{test['query']}\"")
        print("-" * 40)
        
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
            
            # Status
            if domain_match and confidence_good:
                status = "✅ PASS"
            elif domain_match:
                status = "⚠️ PARTIAL (Low confidence)"
            else:
                status = "❌ FAIL (Wrong domain)"
            
            print(f"Status: {status}")
            
            results.append({
                'test': test['description'],
                'domain_match': domain_match,
                'confidence': response.confidence,
                'response_time': response_time,
                'status': status
            })
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            results.append({
                'test': test['description'],
                'domain_match': False,
                'confidence': 0.0,
                'response_time': 0.0,
                'status': "❌ ERROR"
            })
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 50)
    
    passed_tests = sum(1 for r in results if r['domain_match'] and r['confidence'] > 0.5)
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100
    avg_confidence = sum(r['confidence'] for r in results) / total_tests
    avg_response_time = sum(r['response_time'] for r in results) / total_tests
    
    print(f"✅ Passed Tests: {passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print(f"📊 Average Confidence: {avg_confidence:.3f}")
    print(f"⚡ Average Response Time: {avg_response_time:.3f}s")
    
    # Grade
    if success_rate >= 90:
        grade = "A+ (Excellent)"
    elif success_rate >= 80:
        grade = "A (Very Good)"
    elif success_rate >= 70:
        grade = "B (Good)"
    elif success_rate >= 60:
        grade = "C (Average)"
    else:
        grade = "D (Needs Improvement)"
    
    print(f"🎯 Overall Grade: {grade}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if success_rate < 80:
        print("• Consider retraining the ML classifier with more data")
        print("• Review domain classification patterns")
    if avg_confidence < 0.7:
        print("• Improve feature extraction for better confidence scores")
    if avg_response_time > 1.0:
        print("• Optimize processing pipeline for faster responses")
    
    print(f"\n🎉 Testing completed! Agent is {'ready for use' if success_rate >= 70 else 'needs improvements'}.")

def interactive_testing():
    """Interactive testing mode"""
    
    print("🔄 INTERACTIVE TESTING MODE")
    print("=" * 50)
    print("Enter your legal queries to test the agent.")
    print("Type 'quit' to exit, 'help' for sample queries.")
    print("=" * 50)
    
    try:
        agent = create_working_enhanced_agent()
        print("✅ Agent ready for interactive testing!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    while True:
        try:
            user_input = input("\n🔍 Your legal query: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("\n📝 Sample queries to try:")
                print("• My landlord won't return my deposit")
                print("• I was fired unfairly from my job")
                print("• Someone stole my wallet")
                print("• I want to file for divorce")
                print("• My account was hacked")
                continue
            elif not user_input:
                continue
            
            # Process query
            print("\n⏳ Processing...")
            start_time = time.time()
            response = agent.process_query(user_input)
            response_time = time.time() - start_time
            
            # Display results
            print(f"\n📋 RESULTS:")
            print(f"🎯 Domain: {response.domain}")
            print(f"📊 Confidence: {response.confidence:.3f}")
            print(f"⚖️ Legal Route: {response.legal_route}")
            print(f"⏱️ Timeline: {response.timeline}")
            print(f"📈 Success Rate: {response.success_rate:.1%}")
            print(f"⚡ Response Time: {response_time:.3f}s")
            
            # Constitutional backing
            if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
                print(f"🏛️ Constitutional Backing: {response.constitutional_backing[:100]}...")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏛️ LEGAL AGENT TESTING OPTIONS")
    print("=" * 50)
    print("1. Run predefined test scenarios")
    print("2. Interactive testing mode")
    print("=" * 50)
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        test_agent_with_queries()
    elif choice == "2":
        interactive_testing()
    else:
        print("Running predefined tests by default...")
        test_agent_with_queries()