#!/usr/bin/env python3
"""
Debug Comprehensive Guidance Detection
====================================

Debug why comprehensive guidance is showing 0.0% coverage.
"""

def debug_comprehensive_guidance():
    """Debug comprehensive guidance detection"""
    
    print("🔍 DEBUGGING COMPREHENSIVE GUIDANCE DETECTION")
    print("=" * 60)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        
        # Create enhanced adaptive agent
        agent = create_adaptive_agent()
        
        # Test single query
        test_query = "Employee discloses all the company secrets to another company"
        query_input = LegalQueryInput(user_input=test_query, session_id="debug_test")
        
        response = agent.process_query_with_learning(query_input)
        
        print(f"Query: {test_query}")
        print(f"Domain: {response.domain}")
        print(f"Confidence: {response.confidence:.3f}")
        print()
        
        # Check each attribute in detail
        print("📋 DETAILED ATTRIBUTE CHECK:")
        print("-" * 40)
        
        # Process steps
        has_process_steps = hasattr(response, 'process_steps') and response.process_steps
        print(f"✅ process_steps: {has_process_steps}")
        if has_process_steps:
            print(f"   Type: {type(response.process_steps)}")
            print(f"   Count: {len(response.process_steps)}")
            print(f"   First step: {response.process_steps[0][:50] if response.process_steps else 'None'}...")
        else:
            print(f"   process_steps exists: {hasattr(response, 'process_steps')}")
            if hasattr(response, 'process_steps'):
                print(f"   process_steps value: {response.process_steps}")
        print()
        
        # Constitutional backing
        has_constitutional = hasattr(response, 'constitutional_backing') and response.constitutional_backing
        print(f"✅ constitutional_backing: {has_constitutional}")
        if has_constitutional:
            print(f"   Type: {type(response.constitutional_backing)}")
            print(f"   Preview: {str(response.constitutional_backing)[:100]}...")
        else:
            print(f"   constitutional_backing exists: {hasattr(response, 'constitutional_backing')}")
            if hasattr(response, 'constitutional_backing'):
                print(f"   constitutional_backing value: {response.constitutional_backing}")
        print()
        
        # Timeline
        has_timeline = hasattr(response, 'timeline') and response.timeline
        print(f"✅ timeline: {has_timeline}")
        if has_timeline:
            print(f"   Type: {type(response.timeline)}")
            print(f"   Value: {response.timeline}")
        else:
            print(f"   timeline exists: {hasattr(response, 'timeline')}")
            if hasattr(response, 'timeline'):
                print(f"   timeline value: {response.timeline}")
        print()
        
        # Success rate
        has_success_rate = hasattr(response, 'success_rate') and response.success_rate
        print(f"✅ success_rate: {has_success_rate}")
        if has_success_rate:
            print(f"   Type: {type(response.success_rate)}")
            print(f"   Value: {response.success_rate}")
        else:
            print(f"   success_rate exists: {hasattr(response, 'success_rate')}")
            if hasattr(response, 'success_rate'):
                print(f"   success_rate value: {response.success_rate}")
        print()
        
        # Overall comprehensive check
        comprehensive = has_process_steps and has_constitutional and has_timeline and has_success_rate
        print(f"🎯 COMPREHENSIVE: {comprehensive}")
        
        # List all attributes for reference
        print("\n📋 ALL RESPONSE ATTRIBUTES:")
        print("-" * 40)
        for attr in dir(response):
            if not attr.startswith('_'):
                try:
                    value = getattr(response, attr)
                    if not callable(value):
                        value_str = str(value)[:50] if value else "None/Empty"
                        print(f"   {attr}: {value_str}...")
                except:
                    print(f"   {attr}: <error accessing>")
        
    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_comprehensive_guidance()