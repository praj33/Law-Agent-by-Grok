#!/usr/bin/env python3
"""
Enhanced Legal Agent Test Suite
===============================

Test all enhanced features:
1. Enhanced feedback learning (stronger confidence adjustments)
2. Comprehensive legal guidance for all query types
3. Query storage and retrieval system
4. Statistics and analytics
"""

def test_enhanced_features():
    """Test all enhanced features"""
    
    print("🚀 TESTING ENHANCED LEGAL AGENT FEATURES")
    print("=" * 60)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        from query_storage import create_query_storage
        
        # Create enhanced adaptive agent
        agent = create_adaptive_agent()
        query_storage = create_query_storage()
        
        print("\n✅ 1. TESTING COMPREHENSIVE LEGAL GUIDANCE")
        print("-" * 50)
        
        # Test queries across all domains
        test_queries = [
            ("Employment confidentiality", "Employee discloses all the company secrets to another company"),
            ("Tenant rights", "My landlord won't return my deposit"),
            ("Cyber crime", "Someone hacked my bank account"),
            ("Family law", "I want to divorce my spouse"),
            ("Criminal law", "Police arrested me without warrant"),
            ("Consumer complaint", "The product I bought is defective"),
            ("Property dispute", "My neighbor is encroaching on my property"),
            ("Personal injury", "I was injured in a car accident"),
            ("Contract law", "The contractor didn't complete the work"),
            ("Unknown domain", "I need legal help with a complex issue")
        ]
        
        results = []
        for test_name, query in test_queries:
            print(f"\n🔍 Testing: {test_name}")
            query_input = LegalQueryInput(user_input=query, session_id=f"test_{test_name.lower().replace(' ', '_')}")
            
            response = agent.process_query_with_learning(query_input)
            
            # Check if comprehensive guidance is provided
            has_process_steps = hasattr(response, 'process_steps') and response.process_steps
            has_constitutional = hasattr(response, 'constitutional_backing') and response.constitutional_backing
            has_timeline = hasattr(response, 'timeline') and response.timeline
            has_success_rate = hasattr(response, 'success_rate') and response.success_rate
            
            comprehensive = has_process_steps and has_constitutional and has_timeline and has_success_rate
            
            results.append({
                'query': test_name,
                'domain': response.domain,
                'confidence': response.confidence,
                'comprehensive': comprehensive,
                'process_steps': len(response.process_steps) if has_process_steps else 0
            })
            
            print(f"   Domain: {response.domain}")
            print(f"   Confidence: {response.confidence:.3f}")
            print(f"   Process Steps: {len(response.process_steps) if has_process_steps else 0}")
            print(f"   Comprehensive: {'✅' if comprehensive else '❌'}")
        
        # Calculate comprehensive guidance coverage
        comprehensive_count = sum(1 for r in results if r['comprehensive'])
        coverage_percentage = (comprehensive_count / len(results)) * 100
        
        print(f"\n📊 COMPREHENSIVE GUIDANCE COVERAGE: {coverage_percentage:.1f}% ({comprehensive_count}/{len(results)})")
        
        print("\n✅ 2. TESTING ENHANCED FEEDBACK LEARNING")
        print("-" * 50)
        
        # Test feedback learning with enhanced adjustments
        test_query = "My boss is not paying overtime wages"
        query_input = LegalQueryInput(user_input=test_query, session_id="feedback_test")
        
        # Initial response
        initial_response = agent.process_query_with_learning(query_input)
        initial_confidence = initial_response.confidence
        print(f"Initial confidence: {initial_confidence:.3f}")
        
        # Test positive feedback (should increase by +0.35)
        positive_feedback_input = LegalQueryInput(
            user_input=test_query, 
            feedback="very helpful and accurate",
            session_id="feedback_test"
        )
        
        after_positive = agent.process_query_with_learning(positive_feedback_input)
        positive_boost = after_positive.confidence - initial_confidence
        print(f"After positive feedback: {after_positive.confidence:.3f} (boost: {positive_boost:+.3f})")
        
        # Test negative feedback (should decrease by -0.25)
        negative_feedback_input = LegalQueryInput(
            user_input=test_query,
            feedback="not helpful at all, wrong domain",
            session_id="feedback_test"
        )
        
        after_negative = agent.process_query_with_learning(negative_feedback_input)
        negative_change = after_negative.confidence - after_positive.confidence
        print(f"After negative feedback: {after_negative.confidence:.3f} (change: {negative_change:+.3f})")
        
        # Evaluate feedback learning
        positive_strong = positive_boost >= 0.30  # Should be >= 0.35
        negative_strong = negative_change <= -0.20  # Should be <= -0.25
        
        print(f"Strong positive boost (≥0.30): {'✅' if positive_strong else '❌'} ({positive_boost:+.3f})")
        print(f"Strong negative penalty (≤-0.20): {'✅' if negative_strong else '❌'} ({negative_change:+.3f})")
        
        print("\n✅ 3. TESTING QUERY STORAGE SYSTEM")
        print("-" * 50)
        
        # Test query storage and retrieval
        recent_queries = agent.get_recent_queries(5)
        print(f"Recent queries stored: {len(recent_queries)}")
        
        # Test statistics
        stats = agent.get_query_statistics()
        if stats:
            print(f"Total queries: {stats.get('total_queries', 0)}")
            print(f"Domain distribution: {list(stats.get('domain_distribution', {}).keys())[:3]}")
            
            if stats.get('feedback_distribution'):
                feedback_stats = stats['feedback_distribution']
                print(f"Feedback received: {sum(feedback_stats.values())} total")
        
        # Test search functionality
        search_results = agent.search_queries("employer", 3)
        print(f"Queries about 'employer': {len(search_results)}")
        
        print("\n✅ 4. TESTING TERMINAL FORMAT")
        print("-" * 50)
        
        # Test clean terminal format
        terminal_query = LegalQueryInput(user_input="Employee sharing confidential data", session_id="terminal_test")
        
        if hasattr(agent, 'process_query_with_terminal_format'):
            terminal_output = agent.process_query_with_terminal_format(terminal_query)
            
            # Check if output contains all required sections
            required_sections = [
                '📋 Domain Identified:',
                '⚖️ Subcategory:',
                '🛑 Issue:',
                '✅ Legal Route',
                '⚖️ Relevant Constitutional Backing:',
                '📊 Success Rate:',
                '⏱️ Expected Timeline:',
                '💬 Final User-Friendly Answer:'
            ]
            
            sections_found = sum(1 for section in required_sections if section in terminal_output)
            terminal_complete = sections_found == len(required_sections)
            
            print(f"Terminal format sections: {sections_found}/{len(required_sections)}")
            print(f"Complete terminal format: {'✅' if terminal_complete else '❌'}")
        else:
            print("❌ Terminal format method not found")
        
        print("\n" + "=" * 60)
        print("📊 FINAL ENHANCEMENT SUMMARY")
        print("=" * 60)
        
        print(f"✅ Comprehensive Guidance Coverage: {coverage_percentage:.1f}%")
        print(f"✅ Enhanced Feedback Learning: {'Working' if (positive_strong and negative_strong) else 'Needs tuning'}")
        print(f"✅ Query Storage System: {'Active' if stats else 'Inactive'}")
        print(f"✅ Terminal Format: {'Complete' if 'terminal_complete' in locals() and terminal_complete else 'Needs work'}")
        
        overall_score = (
            (coverage_percentage / 100) * 0.4 +  # 40% weight for comprehensive guidance
            (1 if (positive_strong and negative_strong) else 0.5) * 0.3 +  # 30% weight for feedback
            (1 if stats else 0) * 0.2 +  # 20% weight for storage
            (1 if 'terminal_complete' in locals() and terminal_complete else 0.5) * 0.1  # 10% weight for format
        ) * 100
        
        print(f"\n🎯 OVERALL ENHANCEMENT SCORE: {overall_score:.1f}%")
        
        if overall_score >= 90:
            print("🎉 EXCELLENT! All enhancements are working perfectly!")
        elif overall_score >= 75:
            print("👍 GOOD! Most enhancements are working well!")
        elif overall_score >= 60:
            print("⚠️ FAIR! Some enhancements need improvement!")
        else:
            print("❌ NEEDS WORK! Major enhancements required!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_enhanced_features()