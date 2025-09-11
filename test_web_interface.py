#!/usr/bin/env python3
"""
Test the web interface to verify section display
"""

import requests
import json

def test_web_interface():
    """Test the web interface with various queries"""
    
    print("🔍 Testing web interface...")
    
    # API endpoint
    url = "http://localhost:5000/api/ultimate-analysis"
    
    # Test queries
    test_queries = [
        # Test with a general query that should return all sections
        {
            "query": "legal advice",
            "description": "General legal advice query"
        },
        # Test with a specific query that should return specific sections
        {
            "query": "someone stole my phone",
            "description": "Theft-related query"
        },
        # Test with another specific query
        {
            "query": "murder case",
            "description": "Murder-related query"
        }
    ]
    
    for test_case in test_queries:
        query = test_case["query"]
        description = test_case["description"]
        
        print(f"\n📝 {description}: '{query}'")
        
        # Test data
        data = {
            "query": query
        }
        
        try:
            # Make request to the API
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    bns_count = len(result.get('bns_sections', []))
                    ipc_count = len(result.get('ipc_sections', []))
                    crpc_count = len(result.get('crpc_sections', []))
                    total = result.get('total_sections', 0)
                    
                    print(f"✅ Success - Total Sections: {total}")
                    print(f"   BNS: {bns_count} | IPC: {ipc_count} | CrPC: {crpc_count}")
                    
                    # Show some examples of sections returned
                    if bns_count > 0:
                        bns_sections = result.get('bns_sections', [])[:3]
                        bns_nums = [s.get('section_number') for s in bns_sections]
                        print(f"   BNS Examples: {bns_nums}")
                    
                    if ipc_count > 0:
                        ipc_sections = result.get('ipc_sections', [])[:3]
                        ipc_nums = [s.get('section_number') for s in ipc_sections]
                        print(f"   IPC Examples: {ipc_nums}")
                    
                    if crpc_count > 0:
                        crpc_sections = result.get('crpc_sections', [])[:3]
                        crpc_nums = [s.get('section_number') for s in crpc_sections]
                        print(f"   CrPC Examples: {crpc_nums}")
                        
                else:
                    print(f"❌ API Error: {result.get('error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the web server is running")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    print("🌐 WEB INTERFACE TEST")
    print("=" * 40)
    
    test_web_interface()
    
    print(f"\n🏁 Web interface test completed")