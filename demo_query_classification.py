"""
Demo Script for Query Classification System
==========================================

This script demonstrates the full functionality of the query classification system.
"""

import requests
import json


def demo_query_classification():
    """Demonstrate the query classification system"""
    
    print("🏛️  LEGAL QUERY CLASSIFICATION SYSTEM DEMO")
    print("=" * 50)
    
    # Test the stats endpoint
    print("\n📊 Fetching System Statistics...")
    try:
        stats_response = requests.get('http://localhost:5000/api/stats')
        stats_data = stats_response.json()
        print(f"✅ Stats API Response: {stats_data['success']}")
        print(f"   BNS Sections: {stats_data['legal_coverage']['bns_sections']}")
        print(f"   IPC Sections: {stats_data['legal_coverage']['ipc_sections']}")
        print(f"   CrPC Sections: {stats_data['legal_coverage']['crpc_sections']}")
        print(f"   Domains Covered: {stats_data['legal_coverage']['domains_covered']}")
        print(f"   Subdomains Covered: {stats_data['legal_coverage']['subdomains_covered']}")
    except Exception as e:
        print(f"❌ Error fetching stats: {e}")
    
    # Test query classification
    test_queries = [
        "My child was kidnapped for ransom",
        "I was sexually harassed at my workplace",
        "My landlord is not returning my security deposit",
        "I bought a defective phone and want a refund",
        "I had a car accident and need compensation",
        "My phone is being hacked by someone"
    ]
    
    print(f"\n🔍 Testing Query Classification...")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: '{query}'")
        try:
            # Send request to the API
            response = requests.post(
                'http://localhost:5000/api/ultimate-analysis',
                json={'query': query}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"   Domain: {data['domain']}")
                    print(f"   Subdomain: {data['subdomain']}")
                    print(f"   Confidence: {data['domain_confidence_percentage']}")
                    print(f"   Total Sections: {data['total_sections']}")
                    print(f"   Constitutional Articles: {len(data['constitutional_articles'])}")
                else:
                    print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Request Error: {e}")
    
    # Test history endpoint
    print(f"\n💾 Fetching Query History...")
    try:
        history_response = requests.get('http://localhost:5000/api/history')
        history_data = history_response.json()
        if history_data['success']:
            print(f"   ✅ History API Response: {history_data['success']}")
            print(f"   History Items: {len(history_data.get('session_history', []))}")
        else:
            print(f"   ❌ Error: {history_data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error fetching history: {e}")
    
    print(f"\n🎯 Demo completed!")
    print(f"\n🌐 Web Interface is available at: http://localhost:5000")
    print(f"   Open this URL in your browser to use the full web interface")


if __name__ == "__main__":
    demo_query_classification()