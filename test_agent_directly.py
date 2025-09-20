#!/usr/bin/env python3
"""
Direct Agent Test
================

This script tests the working enhanced agent directly to verify it works properly.
"""

def test_working_enhanced_agent():
    """Test the working enhanced agent directly"""
    
    print("🧪 TESTING WORKING ENHANCED AGENT DIRECTLY")
    print("=" * 50)
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        # Create agent
        agent = create_working_enhanced_agent()
        print("✅ Agent created successfully")
        print(f"   ML Available: {agent.ml_available}")
        print(f"   Routes Available: {agent.routes_available}")
        print(f"   Constitutional Available: {agent.constitutional_available}")
        
        # Test queries
        test_queries = [
            "my boss is not giving my salary",
            "my phone is being hacked by someone", 
            "landlord not returning deposit",
            "I want to divorce my husband",
            "someone stole my wallet"
        ]
        
        print("\n📋 Testing Common Queries:")
        print("-" * 30)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            try:
                response = agent.process_query(query)
                print(f"   Domain: {response.domain}")
                print(f"   Confidence: {response.confidence:.3f}")
                print(f"   Timeline: {response.timeline}")
                print(f"   Legal Route: {response.legal_route[:50]}...")
                
                if response.domain == "unknown":
                    print("   ❌ ISSUE: Getting 'unknown' domain")
                else:
                    print("   ✅ SUCCESS: Proper domain classification")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                import traceback
                traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_working_enhanced_agent()