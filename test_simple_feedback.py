#!/usr/bin/env python3
"""
Simple test to verify feedback learning works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

def test_same_session_feedback():
    """Test feedback learning within the same session"""
    
    safe_print("🧪 Testing Same Session Feedback Learning")
    safe_print("=" * 60)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        
        # Create adaptive agent
        agent = create_adaptive_agent()
        
        # Use a fixed session ID
        session_id = "test_session_123"
        
        # Step 1: Initial query
        query = "my employer is not paying overtime wages"
        query_input = LegalQueryInput(
            user_input=query,
            session_id=session_id
        )
        
        initial_response = agent.process_query_with_learning(query_input)
        initial_confidence = initial_response.confidence
        
        safe_print(f"Step 1 - Initial Query: {query}")
        safe_print(f"Initial Confidence: {initial_confidence:.3f}")
        safe_print(f"Domain: {initial_response.domain}")
        
        # Step 2: Same query with positive feedback
        feedback_query = LegalQueryInput(
            user_input=query,  # Same query
            session_id=session_id,  # Same session
            feedback="very helpful"  # Positive feedback
        )
        
        feedback_response = agent.process_query_with_learning(feedback_query)
        feedback_confidence = feedback_response.confidence
        
        safe_print(f"\nStep 2 - Same Query with Positive Feedback")
        safe_print(f"Feedback: 'very helpful'")
        safe_print(f"Confidence after feedback: {feedback_confidence:.3f}")
        safe_print(f"Confidence change: {feedback_confidence - initial_confidence:+.3f}")
        
        # Check if confidence increased
        positive_boost = (feedback_confidence - initial_confidence) > 0.10
        safe_print(f"Positive boost (>0.10): {'✅ YES' if positive_boost else '❌ NO'}")
        
        # Step 3: Same query with negative feedback
        negative_query = LegalQueryInput(
            user_input=query,  # Same query
            session_id=session_id,  # Same session
            feedback="wrong domain"  # Negative feedback
        )
        
        negative_response = agent.process_query_with_learning(negative_query)
        negative_confidence = negative_response.confidence
        
        safe_print(f"\nStep 3 - Same Query with Negative Feedback")
        safe_print(f"Feedback: 'wrong domain'")
        safe_print(f"Confidence after negative feedback: {negative_confidence:.3f}")
        safe_print(f"Confidence change: {negative_confidence - feedback_confidence:+.3f}")
        
        # Check if confidence decreased
        negative_penalty = (negative_confidence - feedback_confidence) < -0.05
        safe_print(f"Negative penalty (<-0.05): {'✅ YES' if negative_penalty else '❌ NO'}")
        
        # Overall test result
        test_passed = positive_boost and negative_penalty
        
        safe_print(f"\n📊 TEST SUMMARY:")
        safe_print(f"Initial Confidence: {initial_confidence:.3f}")
        safe_print(f"After Positive: {feedback_confidence:.3f} ({feedback_confidence - initial_confidence:+.3f})")
        safe_print(f"After Negative: {negative_confidence:.3f} ({negative_confidence - feedback_confidence:+.3f})")
        safe_print(f"Overall Result: {'✅ PASSED' if test_passed else '❌ FAILED'}")
        
        return test_passed
        
    except Exception as e:
        safe_print(f"❌ Error in same session feedback test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    
    safe_print("🔧 SIMPLE FEEDBACK LEARNING TEST")
    safe_print("=" * 70)
    
    success = test_same_session_feedback()
    
    if success:
        safe_print("\n🎉 FEEDBACK LEARNING IS WORKING!")
        safe_print("The adaptive agent properly adjusts confidence based on feedback.")
    else:
        safe_print("\n⚠️ FEEDBACK LEARNING NEEDS MORE WORK")
        safe_print("The confidence adjustments are not working as expected.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)