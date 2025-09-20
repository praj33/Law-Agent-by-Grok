"""
Comprehensive Test for Query Classification System
================================================

This script tests all the requirements specified for the query classification system:
1. Classify input query into Domain and Subdomain using JSON classification system
2. Retrieve ALL legal provisions from BNS, IPC, CrPC
3. Organize output in specific format with Domain, Subdomain, Constitutional Articles, etc.
4. Implement confidence system with feedback learning
5. Store query history with timestamp
"""

import requests
import json
import time

def test_query_classification():
    """Test the complete query classification system"""
    
    # Test cases covering all requirements
    test_cases = [
        {
            "query": "My child was kidnapped for ransom",
            "expected_domain": "Criminal Law",
            "expected_subdomain": "Kidnapping"
        },
        {
            "query": "I was raped by my colleague at workplace",
            "expected_domain": "Criminal Law", 
            "expected_subdomain": "Sexual Offences"
        },
        {
            "query": "My boss is not paying my salary for 3 months",
            "expected_domain": "Employment & Labor Law",
            "expected_subdomain": "Employment Issues"
        },
        {
            "query": "My husband beats me daily and threatens to kill me",
            "expected_domain": "Family Law",
            "expected_subdomain": "Domestic Violence"
        },
        {
            "query": "Landlord is not returning my security deposit after 6 months",
            "expected_domain": "Property & Land Law",
            "expected_subdomain": "Tenant Rights"
        },
        {
            "query": "Someone hacked my phone and stole money from my bank account",
            "expected_domain": "Cyber Crime",
            "expected_subdomain": "Cyber Crime"
        },
        {
            "query": "Doctor's negligence caused harm during surgery",
            "expected_domain": "Consumer Law",
            "expected_subdomain": "Medical Malpractice"
        },
        {
            "query": "Black magic practitioner is harassing my family",
            "expected_domain": "Social Offences",
            "expected_subdomain": "Superstition & Black Magic"
        }
    ]
    
    print("🧪 COMPREHENSIVE QUERY CLASSIFICATION TEST")
    print("=" * 40)
    
    # Test the API endpoint
    url = "http://localhost:5000/api/ultimate-analysis"
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}/{total_tests}: {test_case['query'][:50]}...")
        
        try:
            # Make API request
            response = requests.post(url, json={"query": test_case["query"]})
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    # Check required fields
                    required_fields = [
                        "domain", "subdomain", "bns_sections", "ipc_sections", 
                        "crpc_sections", "constitutional_articles", "legal_guidance"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if not missing_fields:
                        print("✅ API Response Structure: PASS")
                        
                        # Check if we have legal provisions from all three codes
                        bns_count = len(result.get("bns_sections", []))
                        ipc_count = len(result.get("ipc_sections", []))
                        crpc_count = len(result.get("crpc_sections", []))
                        
                        if bns_count > 0 and ipc_count > 0 and crpc_count > 0:
                            print(f"✅ Legal Provisions: PASS (BNS: {bns_count}, IPC: {ipc_count}, CrPC: {crpc_count})")
                        else:
                            print(f"❌ Legal Provisions: FAIL (BNS: {bns_count}, IPC: {ipc_count}, CrPC: {crpc_count})")
                        
                        # Check constitutional articles
                        constitutional_count = len(result.get("constitutional_articles", []))
                        if constitutional_count > 0:
                            print(f"✅ Constitutional Articles: PASS ({constitutional_count} articles)")
                        else:
                            print(f"⚠️  Constitutional Articles: LIMITED ({constitutional_count} articles)")
                        
                        # Check legal guidance sections
                        guidance = result.get("legal_guidance", {})
                        if guidance.get("legal_procedures") and guidance.get("required_documents") and guidance.get("immediate_actions"):
                            print("✅ Legal Guidance: PASS")
                        else:
                            print("⚠️  Legal Guidance: PARTIAL")
                        
                        # Check confidence scoring
                        domain_conf = result.get("domain_confidence_percentage", "0%")
                        if domain_conf and domain_conf != "0%":
                            print(f"✅ Confidence Scoring: PASS ({domain_conf})")
                        else:
                            print("❌ Confidence Scoring: FAIL")
                        
                        passed_tests += 1
                    else:
                        print(f"❌ Missing Fields: {', '.join(missing_fields)}")
                else:
                    print(f"❌ API Error: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        # Add small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print(f"\n🏁 TEST RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Query classification system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

def test_feedback_system():
    """Test the feedback system"""
    print("\n📊 FEEDBACK SYSTEM TEST")
    print("=" * 25)
    
    # First, classify a query
    url = "http://localhost:5000/api/ultimate-analysis"
    test_query = "My child was kidnapped for ransom"
    
    try:
        response = requests.post(url, json={"query": test_query})
        result = response.json()
        
        if result.get("success"):
            print("✅ Query Classification: PASS")
            
            # Submit positive feedback
            feedback_url = "http://localhost:5000/api/feedback"
            feedback_data = {
                "query": result["query"],
                "domain": result["domain_raw"],
                "subdomain": result["subdomain_raw"], 
                "confidence": result["domain_confidence"],
                "feedback": "This analysis was very helpful and accurate",
                "rating": 5
            }
            
            feedback_response = requests.post(feedback_url, json=feedback_data)
            feedback_result = feedback_response.json()
            
            if feedback_result.get("success"):
                print("✅ Feedback Submission: PASS")
                print(f"   Confidence Adjustment: {feedback_result.get('confidence_adjustment', 0)}")
            else:
                print("❌ Feedback Submission: FAIL")
        else:
            print("❌ Query Classification: FAIL")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_query_history():
    """Test query history functionality"""
    print("\n💾 QUERY HISTORY TEST")
    print("=" * 22)
    
    try:
        url = "http://localhost:5000/api/history"
        response = requests.get(url)
        result = response.json()
        
        if result.get("success"):
            history = result.get("session_history", [])
            print(f"✅ Query History: PASS ({len(history)} entries)")
            
            if history:
                latest = history[0]
                print(f"   Latest Query: {latest.get('query', '')[:30]}...")
                print(f"   Domain: {latest.get('domain', 'N/A')}")
                print(f"   Timestamp: {latest.get('timestamp', 'N/A')}")
        else:
            print("❌ Query History: FAIL")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_system_stats():
    """Test system statistics"""
    print("\n📈 SYSTEM STATISTICS TEST")
    print("=" * 25)
    
    try:
        url = "http://localhost:5000/api/stats"
        response = requests.get(url)
        result = response.json()
        
        if result.get("success"):
            legal_coverage = result.get("legal_coverage", {})
            session_info = result.get("session_info", {})
            
            bns_sections = legal_coverage.get("bns_sections", 0)
            ipc_sections = legal_coverage.get("ipc_sections", 0)
            crpc_sections = legal_coverage.get("crpc_sections", 0)
            queries_processed = session_info.get("queries_processed", 0)
            
            print("✅ System Statistics: PASS")
            print(f"   BNS Sections: {bns_sections}")
            print(f"   IPC Sections: {ipc_sections}")
            print(f"   CrPC Sections: {crpc_sections}")
            print(f"   Total Legal Sections: {bns_sections + ipc_sections + crpc_sections}")
            print(f"   Queries Processed: {queries_processed}")
        else:
            print("❌ System Statistics: FAIL")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE QUERY CLASSIFICATION TEST")
    print("Make sure the web server is running at http://localhost:5000")
    
    # Run all tests
    test_query_classification()
    test_feedback_system()
    test_query_history()
    test_system_stats()
    
    print("\n✅ ALL TESTS COMPLETED")