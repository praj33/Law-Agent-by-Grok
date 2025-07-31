"""Debug class structure"""

try:
    from working_enhanced_agent import WorkingEnhancedAgent
    print("✅ Class imported successfully")
    
    agent = WorkingEnhancedAgent()
    print("✅ Agent created successfully")
    
    methods = [method for method in dir(agent) if not method.startswith('_')]
    print(f"📋 Available methods: {methods}")
    
    if hasattr(agent, 'generate_session_id'):
        print("✅ generate_session_id method exists")
    else:
        print("❌ generate_session_id method missing")
        
    # Check if there are syntax errors by trying to call a simple method
    try:
        status = agent.get_system_status()
        print(f"✅ get_system_status works: {status}")
    except Exception as e:
        print(f"❌ get_system_status error: {e}")
        
except Exception as e:
    print(f"❌ Import/creation error: {e}")
    import traceback
    traceback.print_exc()
