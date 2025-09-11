#!/usr/bin/env python3
"""
Test script to verify that all BNS, IPC, and CrPC sections are properly displayed
"""

import requests
import json

def test_sections_display():
    """Test that all sections are properly returned and displayed"""
    
    # Test query
    test_query = "Someone stole my phone and I want to file a police report"
    
    # API endpoint
    url = "http://localhost:5000/api/ultimate-analysis"
    
    # Test data
    data = {
        "query": test_query
    }
    
    try:
        # Make request to the API
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print("✅ API Response Successful")
                print(f"Query: {result.get('query')}")
                print(f"Total Sections: {result.get('total_sections')}")
                print(f"BNS Sections: {len(result.get('bns_sections', []))}")
                print(f"IPC Sections: {len(result.get('ipc_sections', []))}")
                print(f"CrPC Sections: {len(result.get('crpc_sections', []))}")
                
                # Display BNS sections
                print("\n📚 BNS Sections:")
                for section in result.get('bns_sections', [])[:5]:  # Show first 5
                    print(f"  • BNS {section.get('section_number')}: {section.get('title')}")
                
                # Display IPC sections
                print("\n📖 IPC Sections:")
                for section in result.get('ipc_sections', [])[:5]:  # Show first 5
                    print(f"  • IPC {section.get('section_number')}: {section.get('title')}")
                
                # Display CrPC sections
                print("\n⚖️ CrPC Sections:")
                for section in result.get('crpc_sections', [])[:5]:  # Show first 5
                    print(f"  • CrPC {section.get('section_number')}: {section.get('title')}")
                
                # Check if we're getting a good number of sections
                bns_count = len(result.get('bns_sections', []))
                ipc_count = len(result.get('ipc_sections', []))
                crpc_count = len(result.get('crpc_sections', []))
                
                if bns_count > 0 and ipc_count > 0 and crpc_count > 0:
                    print("\n✅ SUCCESS: All section types are being returned!")
                    print(f"   BNS: {bns_count} sections")
                    print(f"   IPC: {ipc_count} sections") 
                    print(f"   CrPC: {crpc_count} sections")
                else:
                    print("\n❌ ISSUE: Some section types are missing")
                    if bns_count == 0:
                        print("   ❌ No BNS sections found")
                    if ipc_count == 0:
                        print("   ❌ No IPC sections found")
                    if crpc_count == 0:
                        print("   ❌ No CrPC sections found")
                
                return True
            else:
                print(f"❌ API Error: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the web server is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Sections Display...")
    print("=" * 50)
    test_sections_display()