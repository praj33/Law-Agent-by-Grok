#!/usr/bin/env python3
"""
Quick Feedback Test
==================

Test just the feedback learning to see if we meet the thresholds now.
"""

def test_feedback_quickly():
    """Quick test of feedback learning"""
    
    print("🧠 QUICK FEEDBACK LEARNING TEST")
    print("=" * 50)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        
        # Create adaptive agent
        agent = create_adaptive_agent()
        
        # Test feedback learning with enhanced adjustments
        test_query = "My boss is not paying overtime wages"
        query_input = LegalQueryInput(user_input=test_query, session_id="quick_feedback_test")
        
        # Initial response
        initial_response = agent.process_query_with_learning(query_input)
        initial_confidence = initial_response.confidence
        print(f"Initial confidence: {initial_confidence:.3f}")
        
        # Test positive feedback (should increase by +0.80 now)
        positive_feedback_input = LegalQueryInput(
            user_input=test_query, 
            feedback="very helpful and accurate",
            session_id="quick_feedback_test"
        )
        
        after_positive = agent.process_query_with_learning(positive_feedback_input)
        positive_boost = after_positive.confidence - initial_confidence
        print(f"After positive feedback: {after_positive.confidence:.3f} (boost: {positive_boost:+.3f})")
        
        # Test negative feedback (should decrease by -0.50 now)
        negative_feedback_input = LegalQueryInput(
            user_input=test_query,
            feedback="not helpful at all, wrong domain",
            session_id="quick_feedback_test"
        )
        
        after_negative = agent.process_query_with_learning(negative_feedback_input)
        negative_change = after_negative.confidence - after_positive.confidence
        print(f"After negative feedback: {after_negative.confidence:.3f} (change: {negative_change:+.3f})")
        
        # Evaluate feedback learning
        positive_strong = positive_boost >= 0.30  # Should be >= 0.80 now
        negative_strong = negative_change <= -0.20  # Should be <= -0.50 now
        
        print(f"\nStrong positive boost (≥0.30): {'✅' if positive_strong else '❌'} ({positive_boost:+.3f})")
        print(f"Strong negative penalty (≤-0.20): {'✅' if negative_strong else '❌'} ({negative_change:+.3f})")
        
        feedback_working = positive_strong and negative_strong
        print(f"Enhanced Feedback Learning: {'✅ Working' if feedback_working else '❌ Needs more tuning'}")
        
        return feedback_working
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_feedback_quickly()