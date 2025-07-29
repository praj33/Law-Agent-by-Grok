"""
Test Script for Working Enhanced Agent
=====================================

Quick test to verify the working enhanced agent functionality.
"""

import sys
import os

# Fix Windows console encoding issues
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

from working_enhanced_agent import create_working_enhanced_agent

def test_working_agent():
    """Test the working enhanced agent"""
    
    safe_print("🧪 TESTING WORKING ENHANCED AGENT")
    safe_print("=" * 50)
    
    # Create agent
    agent = create_working_enhanced_agent()
    
    # Test queries
    test_queries = [
        "My landlord won't return my security deposit",
        "My phone is being hacked by someone", 
        "I was wrongfully terminated from work",
        "My elderly father is being abused"
    ]
    
    safe_print(f"\n🔍 Testing {len(test_queries)} queries:")
    safe_print("-" * 40)

    for i, query in enumerate(test_queries, 1):
        safe_print(f"\n{i}. Query: \"{query}\"")

        try:
            response = agent.process_query(query)

            safe_print(f"   ✅ Domain: {response.domain} (confidence: {response.confidence:.3f})")
            safe_print(f"   ⏱️ Timeline: {response.timeline}")
            safe_print(f"   📊 Success Rate: {response.success_rate:.1%}")
            safe_print(f"   🏛️ Constitutional: {'Yes' if response.constitutional_backing else 'No'}")
            safe_print(f"   ⚡ Response Time: {response.response_time:.3f}s")

        except Exception as e:
            safe_print(f"   ❌ Error: {e}")

    # System status
    safe_print(f"\n📊 System Status:")
    status = agent.get_system_status()
    for component, available in status.items():
        safe_print(f"   {component}: {'✅ Available' if available else '❌ Not Available'}")

    safe_print(f"\n🎉 Test Complete!")
    safe_print(f"   Queries Processed: {agent.session_count}")
    
    return True

if __name__ == "__main__":
    test_working_agent()
