#!/usr/bin/env python3
"""
Test script to verify the web interface is working correctly
"""

import requests
import time

def test_web_interface():
    """Test the web interface endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing Ultimate Legal Agent Web Interface")
    print("=" * 50)
    
    # Test 1: Health check
    print("Test 1: Health Check")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Health check passed")
                print(f"   Components: {data.get('components', {})}")
            else:
                print("❌ Health check failed")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Stats endpoint
    print("\nTest 2: Stats Endpoint")
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Stats endpoint working")
                coverage = data.get("legal_coverage", {})
                print(f"   BNS Sections: {coverage.get('bns_sections', 'N/A')}")
                print(f"   IPC Sections: {coverage.get('ipc_sections', 'N/A')}")
                print(f"   CrPC Sections: {coverage.get('crpc_sections', 'N/A')}")
            else:
                print("❌ Stats endpoint failed")
        else:
            print(f"❌ Stats endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
    
    # Test 3: Ultimate analysis
    print("\nTest 3: Ultimate Analysis")
    test_query = "Someone murdered my brother"
    try:
        response = requests.post(
            f"{base_url}/api/ultimate-analysis",
            json={"query": test_query},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Ultimate analysis working")
                print(f"   Query: {data.get('query', 'N/A')}")
                print(f"   Domain: {data.get('domain', 'N/A')}")
                print(f"   Subdomain: {data.get('subdomain', 'N/A')}")
                print(f"   Total Sections: {data.get('total_sections', 'N/A')}")
            else:
                print("❌ Ultimate analysis failed")
                print(f"   Error: {data.get('error', 'Unknown')}")
        else:
            print(f"❌ Ultimate analysis failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Ultimate analysis error: {e}")
    
    # Test 4: Feedback submission
    print("\nTest 4: Feedback Submission")
    try:
        response = requests.post(
            f"{base_url}/api/feedback",
            json={
                "query": test_query,
                "domain": "criminal_law",
                "subdomain": "murder",
                "confidence": 0.85,
                "feedback": "This analysis was very helpful",
                "rating": 5
            },
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Feedback submission working")
                print(f"   Message: {data.get('message', 'N/A')}")
            else:
                print("❌ Feedback submission failed")
        else:
            print(f"❌ Feedback submission failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Feedback submission error: {e}")
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    test_web_interface()