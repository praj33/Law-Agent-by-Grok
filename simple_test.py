"""Simple test for salary query"""

print("Testing salary query...")

try:
    from working_enhanced_agent import create_working_enhanced_agent
    print("✅ Successfully imported working_enhanced_agent")
    
    agent = create_working_enhanced_agent()
    print("✅ Successfully created agent")
    
    query = "my boss is not giving my salary"
    print(f"Testing query: {query}")
    
    response = agent.process_query(query)
    print(f"✅ Got response:")
    print(f"   Domain: {response.domain}")
    print(f"   Confidence: {response.confidence}")
    
    if response.domain == 'unknown':
        print("❌ Still showing unknown!")
    else:
        print("✅ Fixed! Not showing unknown")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
