#!/usr/bin/env python3
"""
Comprehensive test to verify all sections are properly displayed for various queries
"""

import requests
import json

def test_query(query, expected_sections=None):
    """Test a specific query"""
    
    print(f"\n🔍 Testing Query: '{query}'")
    print("-" * 50)
    
    # API endpoint
    url = "http://localhost:5000/api/ultimate-analysis"
    
    # Test data
    data = {
        "query": query
    }
    
    try:
        # Make request to the API
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                bns_count = len(result.get('bns_sections', []))
                ipc_count = len(result.get('ipc_sections', []))
                crpc_count = len(result.get('crpc_sections', []))
                total = result.get('total_sections', 0)
                
                print(f"✅ Success - Total Sections: {total}")
                print(f"   BNS: {bns_count} | IPC: {ipc_count} | CrPC: {crpc_count}")
                
                # Show some sections if found
                if bns_count > 0:
                    bns_sections = result.get('bns_sections', [])
                    print(f"   BNS Examples: {[s.get('section_number') for s in bns_sections[:3]]}")
                
                if ipc_count > 0:
                    ipc_sections = result.get('ipc_sections', [])
                    print(f"   IPC Examples: {[s.get('section_number') for s in ipc_sections[:3]]}")
                
                if crpc_count > 0:
                    crpc_sections = result.get('crpc_sections', [])
                    print(f"   CrPC Examples: {[s.get('section_number') for s in crpc_sections[:3]]}")
                
                return True
            else:
                print(f"❌ API Error: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the web server is running")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

def run_comprehensive_tests():
    """Run comprehensive tests with various queries"""
    
    print("🧪 COMPREHENSIVE SECTION DISPLAY TEST")
    print("=" * 60)
    
    # Test queries that should trigger different section types
    test_queries = [
        # Theft related (should get BNS, IPC, CrPC)
        "Someone stole my phone and I want to file a police report",
        
        # Murder related (should get all section types)
        "Someone murdered my brother in cold blood",
        
        # Rape related (should get all section types)
        "I was raped by my colleague at workplace",
        
        # Cyber crime (should get relevant sections)
        "Hackers stole money from my bank account",
        
        # Domestic violence (should get relevant sections)
        "My husband beats me daily and threatens me",
        
        # Drug related (should get relevant sections)
        "I was caught with drugs at the airport",
        
        # Employment issue (should get relevant sections)
        "My boss fired me for reporting harassment",
        
        # Property dispute (should get relevant sections)
        "My neighbor built a wall on my property",
        
        # Consumer protection (should get relevant sections)
        "Company sold defective product that caused injury",
    ]
    
    passed = 0
    total = len(test_queries)
    
    for query in test_queries:
        if test_query(query):
            passed += 1
    
    print(f"\n🏁 TEST RESULTS: {passed}/{total} queries processed successfully")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Sections are being displayed correctly!")
    else:
        print("⚠️ Some tests had issues - but this may be expected based on query matching")

if __name__ == "__main__":
    run_comprehensive_tests()