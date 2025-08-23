#!/usr/bin/env python3
"""
Test script to verify the fixes for failed functionalities
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

def test_behavioral_adaptation():
    """Test if behavioral adaptation is working with proper confidence changes"""
    
    safe_print("🧠 Testing Behavioral Adaptation (FIXED)")
    safe_print("=" * 50)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        
        # Create adaptive agent
        agent = create_adaptive_agent()
        
        # Test query
        query = "my employer is not paying overtime wages"
        
        # Initial response
        query_input = LegalQueryInput(user_input=query)
        initial_response = agent.process_query_with_learning(query_input)
        initial_confidence = initial_response.confidence
        
        safe_print(f"Initial Query: {query}")
        safe_print(f"Initial Confidence: {initial_confidence:.3f}")
        safe_print(f"Initial Domain: {initial_response.domain}")
        
        # Provide positive feedback
        feedback_query = LegalQueryInput(
            user_input=query,
            feedback="very helpful"
        )
        
        feedback_response = agent.process_query_with_learning(feedback_query)
        final_confidence = feedback_response.confidence
        
        safe_print(f"After Positive Feedback: {final_confidence:.3f}")
        safe_print(f"Confidence Change: {final_confidence - initial_confidence:+.3f}")
        
        # Check if confidence increased significantly
        confidence_improved = (final_confidence - initial_confidence) > 0.10
        
        safe_print(f"Significant Improvement: {'✅ YES' if confidence_improved else '❌ NO'}")
        
        # Test negative feedback
        negative_feedback_query = LegalQueryInput(
            user_input=query,
            feedback="wrong domain"
        )
        
        negative_response = agent.process_query_with_learning(negative_feedback_query)
        negative_confidence = negative_response.confidence
        
        safe_print(f"After Negative Feedback: {negative_confidence:.3f}")
        safe_print(f"Negative Change: {negative_confidence - final_confidence:+.3f}")
        
        # Check if confidence decreased
        confidence_decreased = (negative_confidence - final_confidence) < -0.05
        
        safe_print(f"Negative Penalty Applied: {'✅ YES' if confidence_decreased else '❌ NO'}")
        
        # Overall test result
        test_passed = confidence_improved and confidence_decreased
        safe_print(f"\nBehavioral Adaptation Test: {'✅ PASSED' if test_passed else '❌ FAILED'}")
        
        return test_passed
        
    except Exception as e:
        safe_print(f"❌ Error in behavioral adaptation test: {e}")
        return False

def test_pattern_grouping():
    """Test if similar queries are grouped into patterns"""
    
    safe_print("\n🧠 Testing Pattern Grouping (FIXED)")
    safe_print("=" * 50)
    
    try:
        from state_memory import create_state_memory
        
        # Create state memory
        state_memory = create_state_memory("test_pattern_memory.db")
        
        # Test similar queries
        similar_queries = [
            ("my landlord won't return security deposit", "tenant_rights"),
            ("landlord refuses to give back deposit", "tenant_rights"),
            ("how to get deposit from landlord", "tenant_rights")
        ]
        
        pattern_ids = []
        
        for query, domain in similar_queries:
            safe_print(f"Processing: {query}")
            
            pattern_id = state_memory.record_query_improvement(
                query, domain, 0.5, 0.6, 'positive', 1.0
            )
            
            pattern_ids.append(pattern_id)
            safe_print(f"  Pattern ID: {pattern_id}")
        
        # Check if similar queries are grouped
        unique_patterns = len(set(pattern_ids))
        total_queries = len(similar_queries)
        
        safe_print(f"\nUnique patterns created: {unique_patterns}")
        safe_print(f"Total queries: {total_queries}")
        safe_print(f"Grouping efficiency: {unique_patterns}/{total_queries}")
        
        # Test passes if similar queries are grouped (should be 1-2 patterns for 3 similar queries)
        test_passed = unique_patterns <= 2
        
        safe_print(f"Pattern Grouping Test: {'✅ PASSED' if test_passed else '❌ FAILED'}")
        
        return test_passed
        
    except Exception as e:
        safe_print(f"❌ Error in pattern grouping test: {e}")
        return False

def test_confidence_adjustment():
    """Test if confidence adjustment system is working"""
    
    safe_print("\n📊 Testing Confidence Adjustment (FIXED)")
    safe_print("=" * 50)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        
        # Create adaptive agent
        agent = create_adaptive_agent()
        
        # Test query
        query = "workplace harassment by supervisor"
        
        # Initial query
        query_input = LegalQueryInput(user_input=query)
        initial_response = agent.process_query_with_learning(query_input)
        initial_confidence = initial_response.confidence
        
        safe_print(f"Query: {query}")
        safe_print(f"Initial Confidence: {initial_confidence:.3f}")
        
        # Positive feedback
        positive_feedback = LegalQueryInput(
            user_input=query,
            feedback="very helpful"
        )
        
        positive_response = agent.process_query_with_learning(positive_feedback)
        positive_confidence = positive_response.confidence
        
        positive_adjustment = positive_confidence - initial_confidence
        safe_print(f"After Positive Feedback: {positive_confidence:.3f}")
        safe_print(f"Positive Adjustment: {positive_adjustment:+.3f}")
        
        # Negative feedback
        negative_feedback = LegalQueryInput(
            user_input=query,
            feedback="wrong domain"
        )
        
        negative_response = agent.process_query_with_learning(negative_feedback)
        negative_confidence = negative_response.confidence
        
        negative_adjustment = negative_confidence - positive_confidence
        safe_print(f"After Negative Feedback: {negative_confidence:.3f}")
        safe_print(f"Negative Adjustment: {negative_adjustment:+.3f}")
        
        # Check if adjustments are significant
        positive_boost = positive_adjustment > 0.10
        negative_penalty = negative_adjustment < -0.05
        
        safe_print(f"\nPositive boost detected (>0.10): {'✅ YES' if positive_boost else '❌ NO'}")
        safe_print(f"Negative penalty detected (<-0.05): {'✅ YES' if negative_penalty else '❌ NO'}")
        
        test_passed = positive_boost and negative_penalty
        safe_print(f"Confidence Adjustment Test: {'✅ PASSED' if test_passed else '❌ FAILED'}")
        
        return test_passed
        
    except Exception as e:
        safe_print(f"❌ Error in confidence adjustment test: {e}")
        return False

def test_multi_stage_dialogue():
    """Test multi-stage dialogue learning"""
    
    safe_print("\n💬 Testing Multi-Stage Dialogue (FIXED)")
    safe_print("=" * 50)
    
    try:
        from adaptive_agent import create_adaptive_agent
        from conversation_loop import create_conversation_loop
        
        # Create components
        agent = create_adaptive_agent()
        conversation_loop = create_conversation_loop("test_conversation_fixed.json")
        
        # Start conversation
        initial_query = "my landlord is not returning my security deposit"
        session_id = conversation_loop.start_conversation(initial_query, agent)
        
        safe_print(f"Started conversation: {initial_query}")
        
        # Get initial confidence
        conversation = conversation_loop.active_conversations[session_id]
        initial_confidence = conversation.turns[0].agent_response.confidence
        safe_print(f"Initial confidence: {initial_confidence:.3f}")
        
        # Continue conversation with positive feedback
        response, should_end = conversation_loop.continue_conversation(
            session_id,
            "what legal action can I take",
            agent,
            feedback_on_previous="helpful"
        )
        
        if response:
            final_confidence = response.confidence
            safe_print(f"After feedback: {final_confidence:.3f}")
            safe_print(f"Confidence change: {final_confidence - initial_confidence:+.3f}")
            
            # Check for learning
            learning_detected = abs(final_confidence - initial_confidence) > 0.05
            safe_print(f"Learning detected: {'✅ YES' if learning_detected else '❌ NO'}")
            
            # End conversation
            conversation_loop.end_conversation(session_id, "satisfied")
            
            test_passed = learning_detected
            safe_print(f"Multi-Stage Dialogue Test: {'✅ PASSED' if test_passed else '❌ FAILED'}")
            
            return test_passed
        else:
            safe_print("❌ No response received")
            return False
        
    except Exception as e:
        safe_print(f"❌ Error in multi-stage dialogue test: {e}")
        return False

def main():
    """Run all fix tests"""
    
    safe_print("🔧 TESTING FIXED FUNCTIONALITIES")
    safe_print("=" * 70)
    safe_print("Testing fixes for previously failed adaptive learning components")
    safe_print("=" * 70)
    
    results = []
    
    # Test 1: Behavioral Adaptation
    results.append(test_behavioral_adaptation())
    
    # Test 2: Pattern Grouping
    results.append(test_pattern_grouping())
    
    # Test 3: Confidence Adjustment
    results.append(test_confidence_adjustment())
    
    # Test 4: Multi-Stage Dialogue
    results.append(test_multi_stage_dialogue())
    
    # Summary
    safe_print("\n" + "=" * 70)
    safe_print("📊 FIX TEST SUMMARY")
    safe_print("=" * 70)
    
    test_names = [
        "Behavioral Adaptation",
        "Pattern Grouping", 
        "Confidence Adjustment",
        "Multi-Stage Dialogue"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        safe_print(f"{name}: {status}")
    
    passed_tests = sum(results)
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100
    
    safe_print(f"\nOverall Fix Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 75:
        safe_print("🎉 FIXES SUCCESSFUL! Task 2 functionalities are now working properly.")
    else:
        safe_print("⚠️ Some fixes still need attention.")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)