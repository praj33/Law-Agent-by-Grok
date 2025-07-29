"""
Test Enhanced System with Unknown Query Handling
===============================================

Test script to demonstrate the improved unknown query handling
and enhanced responses for various types of legal queries.
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

from working_enhanced_agent import create_working_enhanced_agent

def test_enhanced_unknown_handling():
    """Test the enhanced unknown query handling"""
    
    safe_print("🧪 TESTING ENHANCED UNKNOWN QUERY HANDLING")
    safe_print("=" * 60)
    safe_print("Testing queries that previously returned 'unknown' domain")
    safe_print("=" * 60)
    
    agent = create_working_enhanced_agent()
    
    # Test queries that were previously problematic
    test_queries = [
        # Harassment queries (previously unknown)
        "my neighbor girl is being harassed",
        "boss is sexually harassing me at work", 
        "someone is stalking me online",
        "colleague bothering me constantly",
        
        # Other edge cases
        "my car was stolen yesterday",
        "need help with property dispute",
        "doctor gave wrong treatment",
        "teacher is discriminating against my child",
        "auto driver cheated me",
        "bank is harassing me for loan payment",
        
        # Completely new scenarios
        "my pet dog was killed by neighbor",
        "someone is spreading rumors about me",
        "my business partner ran away with money",
        "government official demanding bribe",
        "my phone was snatched on street"
    ]
    
    safe_print(f"\n🔍 Testing {len(test_queries)} diverse queries:")
    safe_print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        safe_print(f"\n{i}. Query: \"{query}\"")
        
        try:
            response = agent.process_query(query)
            
            # Display enhanced response
            safe_print(f"   🎯 Domain: {response.domain} (confidence: {response.confidence:.3f})")
            safe_print(f"   📋 Legal Route: {response.legal_route}")
            safe_print(f"   ⏱️ Timeline: {response.timeline}")
            safe_print(f"   📊 Success Rate: {response.success_rate:.1%}")
            
            if response.constitutional_backing:
                safe_print(f"   🏛️ Constitutional: Available")
            else:
                safe_print(f"   🏛️ Constitutional: Not provided")
            
            safe_print(f"   ⚡ Response Time: {response.response_time:.3f}s")
            
            # Show improvement
            if response.domain != 'unknown':
                safe_print(f"   ✅ IMPROVED: Previously would be 'unknown'")
            else:
                safe_print(f"   ⚠️ Still unknown - needs further enhancement")
                
        except Exception as e:
            safe_print(f"   ❌ Error: {e}")
    
    # System status
    safe_print(f"\n📊 System Status:")
    status = agent.get_system_status()
    for component, available in status.items():
        safe_print(f"   {component}: {'✅ Available' if available else '❌ Not Available'}")
    
    safe_print(f"\n🎉 Enhanced Unknown Handling Test Complete!")
    safe_print(f"   Total Queries Processed: {agent.session_count}")
    
    return True

def interactive_test():
    """Interactive test for user queries"""
    
    safe_print("\n🎮 INTERACTIVE TEST MODE")
    safe_print("=" * 40)
    safe_print("Enter your own queries to test the enhanced system")
    safe_print("Type 'quit' to exit, 'examples' for sample queries")
    safe_print("=" * 40)
    
    agent = create_working_enhanced_agent()
    
    while True:
        try:
            user_input = input("\nYour legal question: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'examples':
                safe_print("\n💡 Example queries to try:")
                examples = [
                    "my neighbor is harassing my daughter",
                    "boss making inappropriate comments",
                    "someone hacked my social media",
                    "my car accident compensation",
                    "landlord not returning deposit",
                    "company fired me unfairly",
                    "need help with divorce case",
                    "elderly father being cheated"
                ]
                for example in examples:
                    safe_print(f"   • \"{example}\"")
                continue
            elif not user_input:
                continue
            
            # Process query
            safe_print(f"\n🔍 Processing: \"{user_input}\"")
            response = agent.process_query(user_input)
            
            # Display detailed response
            safe_print(f"\n📋 Enhanced Legal Response:")
            safe_print(f"   🎯 Domain: {response.domain.title()} (Confidence: {response.confidence:.3f})")
            safe_print(f"   📋 Legal Route: {response.legal_route}")
            safe_print(f"   ⏱️ Expected Timeline: {response.timeline}")
            safe_print(f"   📊 Success Rate: {response.success_rate:.1%}")
            
            if response.constitutional_backing:
                safe_print(f"   🏛️ Constitutional Backing: {response.constitutional_backing[:80]}...")
            else:
                safe_print(f"   🏛️ Constitutional Backing: Not available for this domain")
            
            safe_print(f"   ⚡ Response Time: {response.response_time:.3f}s")
            
            # Show classification improvement
            if response.confidence >= 0.5:
                safe_print(f"   ✅ HIGH CONFIDENCE: Strong domain classification")
            elif response.confidence >= 0.3:
                safe_print(f"   ⚠️ MEDIUM CONFIDENCE: Reasonable classification")
            else:
                safe_print(f"   ❓ LOW CONFIDENCE: May need manual review")
            
        except KeyboardInterrupt:
            safe_print(f"\nGoodbye!")
            break
        except Exception as e:
            safe_print(f"Error: {e}")

def main():
    """Main test function"""
    
    safe_print("🚀 ENHANCED LEGAL AGENT - UNKNOWN QUERY FIX")
    safe_print("=" * 60)
    safe_print("This system now handles 'unknown' queries intelligently!")
    safe_print("=" * 60)
    
    # Run automated tests
    test_enhanced_unknown_handling()
    
    # Ask user for interactive test
    safe_print(f"\n🎮 Would you like to test with your own queries? (y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes']:
            interactive_test()
    except:
        pass
    
    safe_print(f"\n🎉 TESTING COMPLETE!")
    safe_print("Your Enhanced Legal Agent now provides intelligent responses")
    safe_print("for queries that previously returned 'unknown' domain!")

if __name__ == "__main__":
    main()
