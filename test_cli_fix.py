"""
Test CLI Fix
============

Test the specific query that's showing unknown in CLI
"""

import sys
import os

# Fix Windows console encoding
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

def test_cli_query():
    """Test the specific query that's showing unknown"""
    
    safe_print("🔧 TESTING CLI QUERY FIX")
    safe_print("=" * 50)
    safe_print("Testing the exact query you mentioned")
    safe_print("=" * 50)
    
    from working_enhanced_agent import create_working_enhanced_agent
    agent = create_working_enhanced_agent()
    
    # Test the exact query you mentioned
    query = "my boss is not giving my salary"
    
    safe_print(f"\n🧪 Testing query: \"{query}\"")
    safe_print("-" * 60)
    
    try:
        response = agent.process_query(query)
        
        safe_print(f"✅ RESULT:")
        safe_print(f"   Domain: {response.domain}")
        safe_print(f"   Confidence: {response.confidence:.3f}")
        safe_print(f"   Legal Route: {response.legal_route[:60]}...")
        safe_print(f"   Timeline: {response.timeline}")
        safe_print(f"   Success Rate: {response.success_rate:.1%}")
        
        if response.domain == 'unknown':
            safe_print(f"\n❌ STILL SHOWING UNKNOWN!")
            safe_print(f"   This means the enhanced logic is not working properly")
        else:
            safe_print(f"\n✅ FIXED! No longer showing unknown")
            safe_print(f"   The enhanced agent is working correctly")
            
    except Exception as e:
        safe_print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test a few more salary-related queries
    salary_queries = [
        "my boss is not giving my salary",
        "my boss is not increasing my salary", 
        "company not paying my wages",
        "employer withholding salary",
        "boss not paying me for months"
    ]
    
    safe_print(f"\n🧪 Testing multiple salary queries:")
    safe_print("-" * 60)
    
    for query in salary_queries:
        try:
            response = agent.process_query(query)
            status = "✅ FIXED" if response.domain != 'unknown' else "❌ UNKNOWN"
            safe_print(f"{status}: \"{query}\" → {response.domain} ({response.confidence:.3f})")
        except Exception as e:
            safe_print(f"❌ ERROR: \"{query}\" → {e}")

def main():
    """Main test function"""
    
    test_cli_query()
    
    safe_print(f"\n🎯 CONCLUSION:")
    safe_print("=" * 30)
    safe_print("If queries are still showing 'unknown', the issue might be:")
    safe_print("1. CLI is using wrong agent (should use working_enhanced_agent)")
    safe_print("2. Enhanced patterns not matching properly")
    safe_print("3. ML classifier overriding enhanced logic")
    
    safe_print(f"\n🚀 TO FIX CLI:")
    safe_print("Make sure cli_interface.py imports and uses working_enhanced_agent")
    safe_print("The enhanced agent should handle salary queries correctly")

if __name__ == "__main__":
    main()
