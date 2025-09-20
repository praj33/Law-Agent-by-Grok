#!/usr/bin/env python3
"""
Test Script for Legal AI Agent
==============================

This script tests the Legal AI Agent with various queries to ensure
it properly classifies domains and retrieves relevant legal provisions.
"""

from legal_ai_agent import create_legal_ai_agent

def test_legal_ai_agent():
    """Test the Legal AI Agent with various queries"""
    
    # Create the agent
    agent = create_legal_ai_agent()
    
    # Test cases based on the JSON mapping provided
    test_cases = [
        {
            "query": "My child was kidnapped for ransom",
            "expected_domain": "Criminal Law",
            "expected_subdomain": "Kidnapping / Abduction"
        },
        {
            "query": "Someone murdered my brother in cold blood",
            "expected_domain": "Criminal Law",
            "expected_subdomain": "Homicide"
        },
        {
            "query": "I was raped by my colleague",
            "expected_domain": "Criminal Law",
            "expected_subdomain": "Sexual Offences"
        },
        {
            "query": "Hackers stole money from my bank account",
            "expected_domain": "Cyber Law",
            "expected_subdomain": "Hacking / Online Fraud / Identity Theft"
        },
        {
            "query": "My boss fired me for reporting harassment",
            "expected_domain": "Labour & Employment Law",
            "expected_subdomain": "Contract Disputes / Workplace Harassment / Compensation"
        },
        {
            "query": "My husband beats me daily",
            "expected_domain": "Family Law / Criminal Law",
            "expected_subdomain": "Domestic Abuse / Cruelty"
        },
        {
            "query": "Business partner embezzled funds",
            "expected_domain": "Criminal Law / Economic Offences",
            "expected_subdomain": "Fraud / White Collar Crimes"
        },
        {
            "query": "Caught with drugs at airport",
            "expected_domain": "Criminal Law",
            "expected_subdomain": "Narcotics & Psychotropic Substances"
        },
        {
            "query": "Landlord won't return security deposit",
            "expected_domain": "Property Law",
            "expected_subdomain": "Rent Control / Tenancy Disputes"
        },
        {
            "query": "Company sold defective product",
            "expected_domain": "Consumer Law",
            "expected_subdomain": "Product Liability / Service Deficiency"
        }
    ]
    
    print("🧪 Testing Legal AI Agent")
    print("=" * 80)
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected_domain = test_case["expected_domain"]
        expected_subdomain = test_case["expected_subdomain"]
        
        print(f"\n📝 Test {i}/{total_tests}")
        print(f"Query: {query}")
        print(f"Expected Domain: {expected_domain}")
        print(f"Expected Subdomain: {expected_subdomain}")
        
        # Process the query
        try:
            result = agent.process_query(query)
            actual_domain = result["domain"]
            actual_subdomain = result["subdomain"]
            
            # Check if classification is correct
            domain_match = expected_domain.lower() in actual_domain.lower() or actual_domain.lower() in expected_domain.lower()
            subdomain_match = expected_subdomain.lower() in actual_subdomain.lower() or actual_subdomain.lower() in expected_subdomain.lower()
            
            if domain_match and subdomain_match:
                print("✅ Test PASSED")
                passed_tests += 1
            else:
                print("❌ Test FAILED")
                print(f"   Actual Domain: {actual_domain}")
                print(f"   Actual Subdomain: {actual_subdomain}")
            
            # Show some results
            print(f"   Sections Found - BNS: {len(result['bns_sections'])}, IPC: {len(result['ipc_sections'])}, CrPC: {len(result['crpc_sections'])}")
            
        except Exception as e:
            print(f"❌ Test FAILED with exception: {e}")
    
    print("\n" + "=" * 80)
    print(f"🏁 Test Results: {passed_tests}/{total_tests} tests passed")
    print(f"📈 Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    # Test the formatting
    print("\n📄 Testing Output Formatting")
    print("-" * 40)
    
    sample_query = "My child was kidnapped for ransom"
    result = agent.process_query(sample_query)
    formatted_output = agent.format_output(result)
    
    print("Formatted Output:")
    print(formatted_output[:1000] + "..." if len(formatted_output) > 1000 else formatted_output)


if __name__ == "__main__":
    test_legal_ai_agent()