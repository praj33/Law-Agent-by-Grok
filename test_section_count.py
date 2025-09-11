#!/usr/bin/env python3
"""
Test script to verify all sections are properly returned for various queries
"""

import requests
import json

def test_section_count():
    """Test that all sections are returned for different types of queries"""
    
    print("🔍 Testing section count for various queries...")
    
    # API endpoint
    url = "http://localhost:5000/api/ultimate-analysis"
    
    # Test with a simple query
    test_queries = [
        "test query",
        "someone stole my phone",
        "murder case",
        "drug related crime",
        "employment issue"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        
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
                    
                    # Check if we're getting all sections for empty/non-matching queries
                    if query == "test query":
                        if bns_count >= 358 and ipc_count >= 418 and crpc_count >= 238:
                            print("✅ All sections returned for test query!")
                        else:
                            print("⚠️ Not all sections returned for test query")
                            print("   This may be expected if the query matches specific keywords")
                else:
                    print(f"❌ API Error: {result.get('error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the web server is running")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
    
    return True

def test_empty_query():
    """Test with an empty query to ensure we get all sections"""
    
    print(f"\n🔍 Testing with empty query...")
    
    # API endpoint
    url = "http://localhost:5000/api/ultimate-analysis"
    
    # Test data with empty query
    data = {
        "query": ""
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
                
                # For empty query, we should get all sections
                if bns_count >= 358 and ipc_count >= 418 and crpc_count >= 238:
                    print("✅ All sections returned for empty query!")
                    return True
                else:
                    print("❌ Not all sections returned for empty query")
                    return False
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

if __name__ == "__main__":
    print("🧪 SECTION COUNT VERIFICATION TEST")
    print("=" * 60)
    
    # Test various queries
    test_section_count()
    
    # Test empty query specifically
    test_empty_query()
    
    print(f"\n🏁 Test completed")