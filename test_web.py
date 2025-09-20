#!/usr/bin/env python3
"""
Quick test script to verify the web interface works
"""

import sys
import time
import threading
import requests
from web_interface import app

def test_web_interface():
    """Test the web interface"""
    print("🧪 Testing Web Interface...")
    
    # Start the Flask app in a separate thread
    def run_app():
        app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
    
    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test main page
        print("📍 Testing main page...")
        response = requests.get('http://127.0.0.1:5001/', timeout=10)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
        
        # Test API endpoint
        print("📍 Testing API endpoint...")
        api_response = requests.post(
            'http://127.0.0.1:5001/api/query',
            json={'query': 'My phone is stolen'},
            timeout=15
        )
        
        if api_response.status_code == 200:
            data = api_response.json()
            if data.get('success'):
                print("✅ API endpoint works successfully")
                print(f"   Domain: {data.get('domain', 'N/A')}")
                print(f"   Confidence: {data.get('confidence_percentage', 'N/A')}")
                return True
            else:
                print(f"❌ API returned error: {data.get('error', 'Unknown')}")
                return False
        else:
            print(f"❌ API endpoint failed: {api_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_web_interface()
    if success:
        print("\n🎉 Web interface test PASSED!")
        print("🌐 You can now run: python run.py --web")
        print("📍 Then open: http://localhost:5000")
    else:
        print("\n❌ Web interface test FAILED!")
        print("🔧 Check the error messages above")
    
    sys.exit(0 if success else 1)