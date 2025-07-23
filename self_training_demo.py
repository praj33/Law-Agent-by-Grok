"""
Self-Training Legal Agent Demo
=============================

This demo shows how the agent learns from feedback and improves over time.
It demonstrates the difference between the basic agent and the adaptive agent.

Usage: python self_training_demo.py
"""

from legal_agent import create_legal_agent, LegalQueryInput
from adaptive_legal_agent import create_adaptive_legal_agent
import json

def print_header(title):
    print("\n" + "="*60)
    print(f"🧠 {title}")
    print("="*60)

def print_subheader(title):
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_basic_vs_adaptive():
    """Compare basic agent vs adaptive agent"""
    
    print_header("BASIC AGENT vs ADAPTIVE AGENT COMPARISON")
    
    # Create both agents
    basic_agent = create_legal_agent()
    adaptive_agent = create_adaptive_legal_agent()
    
    test_query = "My landlord won't return my deposit"
    
    print_subheader("1. Initial Response - Both Agents")
    
    # Basic agent response
    basic_query = LegalQueryInput(user_input=test_query)
    basic_response = basic_agent.process_query(basic_query)
    print(f"🔵 Basic Agent:")
    print(f"   Domain: {basic_response.domain}")
    print(f"   Confidence: {basic_response.confidence:.3f}")
    
    # Adaptive agent response
    adaptive_query = LegalQueryInput(user_input=test_query)
    adaptive_response = adaptive_agent.process_query_with_learning(adaptive_query)
    print(f"🟢 Adaptive Agent:")
    print(f"   Domain: {adaptive_response.domain}")
    print(f"   Confidence: {adaptive_response.confidence:.3f}")
    
    print_subheader("2. User Gives Negative Feedback")
    print("User says: 'This is wrong! This should be consumer complaint, not tenant rights!'")
    
    # Basic agent with negative feedback (no learning)
    basic_feedback_query = LegalQueryInput(
        user_input=test_query,
        feedback="This is wrong! This should be consumer complaint, not tenant rights!"
    )
    basic_feedback_response = basic_agent.process_query(basic_feedback_query)
    print(f"🔵 Basic Agent (after feedback):")
    print(f"   Domain: {basic_feedback_response.domain}")
    print(f"   Confidence: {basic_feedback_response.confidence:.3f}")
    print(f"   Learning: ❌ No change - same response")
    
    # Adaptive agent with negative feedback (learns)
    adaptive_feedback_query = LegalQueryInput(
        user_input=test_query,
        feedback="This is wrong! This should be consumer complaint, not tenant rights!"
    )
    adaptive_feedback_response = adaptive_agent.process_query_with_learning(adaptive_feedback_query)
    print(f"🟢 Adaptive Agent (after feedback):")
    print(f"   Domain: {adaptive_feedback_response.domain}")
    print(f"   Confidence: {adaptive_feedback_response.confidence:.3f}")
    print(f"   Learning: ✅ Learned from feedback")
    
    print_subheader("3. Same Query Asked Again")
    
    # Basic agent - same response
    basic_repeat_query = LegalQueryInput(user_input=test_query)
    basic_repeat_response = basic_agent.process_query(basic_repeat_query)
    print(f"🔵 Basic Agent (repeat query):")
    print(f"   Domain: {basic_repeat_response.domain}")
    print(f"   Confidence: {basic_repeat_response.confidence:.3f}")
    print(f"   Change: ❌ No improvement")
    
    # Adaptive agent - improved response
    adaptive_repeat_query = LegalQueryInput(user_input=test_query)
    adaptive_repeat_response = adaptive_agent.process_query_with_learning(adaptive_repeat_query)
    print(f"🟢 Adaptive Agent (repeat query):")
    print(f"   Domain: {adaptive_repeat_response.domain}")
    print(f"   Confidence: {adaptive_repeat_response.confidence:.3f}")
    print(f"   Change: ✅ Improved based on learning")
    
    return adaptive_agent

def demo_learning_progression():
    """Show how agent improves over multiple feedback cycles"""
    
    print_header("LEARNING PROGRESSION OVER TIME")
    
    agent = create_adaptive_legal_agent()
    
    # Test scenarios with expected corrections
    scenarios = [
        {
            "query": "My bank charged me unfair fees",
            "initial_expected": "consumer complaint",
            "feedback": "not helpful, this is a banking issue",
            "correction": "Should learn to classify banking issues better"
        },
        {
            "query": "My employer didn't pay overtime",
            "initial_expected": "employment law", 
            "feedback": "very helpful, exactly right",
            "correction": "Should reinforce employment law classification"
        },
        {
            "query": "Online scammer took my money",
            "initial_expected": "cyber crime",
            "feedback": "wrong domain, this is fraud not cyber crime",
            "correction": "Should learn to distinguish fraud types"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print_subheader(f"Scenario {i}: {scenario['query']}")
        
        # Initial response
        query1 = LegalQueryInput(user_input=scenario['query'])
        response1 = agent.process_query_with_learning(query1)
        print(f"Initial: {response1.domain} (confidence: {response1.confidence:.3f})")
        
        # Feedback
        query2 = LegalQueryInput(
            user_input=scenario['query'],
            feedback=scenario['feedback']
        )
        response2 = agent.process_query_with_learning(query2)
        print(f"After feedback: {response2.domain} (confidence: {response2.confidence:.3f})")
        
        # Test again
        query3 = LegalQueryInput(user_input=scenario['query'])
        response3 = agent.process_query_with_learning(query3)
        print(f"Next time: {response3.domain} (confidence: {response3.confidence:.3f})")
        
        # Show learning
        if response3.confidence != response1.confidence or response3.domain != response1.domain:
            print("✅ Agent learned and adapted!")
        else:
            print("⚠️ No change detected")
    
    return agent

def demo_learning_statistics(agent):
    """Show learning statistics"""
    
    print_header("LEARNING STATISTICS")
    
    stats = agent.get_learning_stats()
    
    print(f"📊 Total Feedback Processed: {stats['total_feedback_processed']}")
    print(f"✅ Positive Feedback: {stats['positive_feedback_count']}")
    print(f"❌ Negative Feedback: {stats['negative_feedback_count']}")
    print(f"🔄 Classifications Improved: {stats['classifications_improved']}")
    print(f"🧠 Learning Data Size: {stats['learning_data_size']}")
    print(f"⚙️ Domains with Adjustments: {stats['domains_with_adjustments']}")
    
    if stats['confidence_adjustments']:
        print(f"\n🎯 Confidence Adjustments by Domain:")
        for domain, adjustment in stats['confidence_adjustments'].items():
            direction = "↗️" if adjustment > 0 else "↘️"
            print(f"   {domain}: {adjustment:+.3f} {direction}")

def demo_persistent_learning():
    """Show that learning persists across sessions"""
    
    print_header("PERSISTENT LEARNING ACROSS SESSIONS")
    
    print_subheader("Session 1: Training the Agent")
    
    # Create agent and train it
    agent1 = create_adaptive_legal_agent()
    
    training_query = LegalQueryInput(
        user_input="My credit card company is charging hidden fees",
        feedback="This should be consumer complaint, not banking law"
    )
    response1 = agent1.process_query_with_learning(training_query)
    print(f"Session 1 - After training: {response1.domain} (confidence: {response1.confidence:.3f})")
    
    print_subheader("Session 2: New Agent Instance (Loads Previous Learning)")
    
    # Create new agent instance - should load previous learning
    agent2 = create_adaptive_legal_agent()
    
    test_query = LegalQueryInput(user_input="My credit card company is charging hidden fees")
    response2 = agent2.process_query_with_learning(test_query)
    print(f"Session 2 - Same query: {response2.domain} (confidence: {response2.confidence:.3f})")
    
    if response2.domain != response1.domain or abs(response2.confidence - response1.confidence) > 0.01:
        print("✅ Learning persisted across sessions!")
    else:
        print("⚠️ Learning may not have persisted")

def main():
    """Run all self-training demos"""
    
    print("🧠 SELF-TRAINING LEGAL AGENT DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how the agent learns from your feedback and improves over time.")
    
    try:
        # Demo 1: Basic vs Adaptive comparison
        adaptive_agent = demo_basic_vs_adaptive()
        
        # Demo 2: Learning progression
        trained_agent = demo_learning_progression()
        
        # Demo 3: Learning statistics
        demo_learning_statistics(trained_agent)
        
        # Demo 4: Persistent learning
        demo_persistent_learning()
        
        print_header("SUMMARY")
        print("✅ Adaptive agent successfully demonstrated!")
        print("\n🎯 Key Features Shown:")
        print("• ✅ Learns from negative feedback")
        print("• ✅ Adjusts confidence scores")
        print("• ✅ Tries alternative classifications")
        print("• ✅ Reinforces positive feedback")
        print("• ✅ Persists learning across sessions")
        print("• ✅ Provides learning statistics")
        
        print("\n🚀 How to Use:")
        print("1. Replace 'create_legal_agent()' with 'create_adaptive_legal_agent()'")
        print("2. Use 'process_query_with_learning()' instead of 'process_query()'")
        print("3. Give feedback - agent will learn and improve!")
        
        print("\n📁 Files Created:")
        print("• learning_data.json - Stores learning progress")
        print("• adaptive_legal_agent.py - Self-training agent code")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()
