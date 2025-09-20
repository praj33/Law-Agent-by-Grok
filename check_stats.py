#!/usr/bin/env python3
"""
Check system stats to verify section counts
"""

import requests
import json

def check_stats():
    """Check system stats"""
    
    print("🔍 Checking system stats...")
    
    # API endpoint
    url = "http://localhost:5000/api/stats"
    
    try:
        # Make request to the API
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                legal_coverage = result.get("legal_coverage", {})
                
                bns_sections = legal_coverage.get("bns_sections", 0)
                ipc_sections = legal_coverage.get("ipc_sections", 0)
                crpc_sections = legal_coverage.get("crpc_sections", 0)
                total_sections = legal_coverage.get("total_sections", 0)
                
                print(f"📊 System Stats:")
                print(f"   BNS Sections: {bns_sections}")
                print(f"   IPC Sections: {ipc_sections}")
                print(f"   CrPC Sections: {crpc_sections}")
                print(f"   Total Sections: {total_sections}")
                
                # Verify counts match expectations
                if bns_sections == 358 and ipc_sections == 418 and crpc_sections == 238:
                    print("✅ All section counts match expected values!")
                    return True
                else:
                    print("❌ Section counts don't match expected values")
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
    print("📈 SYSTEM STATISTICS CHECK")
    print("=" * 40)
    
    check_stats()
    
    print(f"\n🏁 Stats check completed")