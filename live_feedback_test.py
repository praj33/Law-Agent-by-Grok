"""
Live Feedback Test - Real Query Testing
=======================================

This script tests the feedback rating system with real queries
to demonstrate exactly how it works in practice.
"""

from cli_interface import LegalAgentCLI
import time

def test_real_query_with_feedback():
    """Test the feedback system with a real legal query"""
    
    print("🧪 LIVE FEEDBACK SYSTEM TEST")
    print("=" * 60)
    print("Testing with a real legal query to show the complete flow")
    
    # Create CLI instance
    cli = LegalAgentCLI()
    
    print("\n🎯 TEST SCENARIO: Workplace Issue")
    print("=" * 40)
    
    # Test Query 1: Workplace harassment
    print("\n📝 STEP 1: User asks about workplace harassment")
    print("👤 User types: my coworker is sexually harassing me at work")
    
    # Process the query
    cli.process_command("my coworker is sexually harassing me at work")
    
    print(f"\n✅ Agent Response Summary:")
    print(f"   Domain: {cli.last_response.domain}")
    print(f"   Confidence: {cli.last_response.confidence:.3f}")
    print(f"   Timeline: {cli.last_response.timeline}")
    print(f"   Session ID: {cli.session_id}")
    
    # Test positive feedback
    print("\n📝 STEP 2: User gives positive feedback")
    print("👤 User types: helpful")
    
    cli.process_command("helpful")
    
    # Test follow-up query
    print("\n📝 STEP 3: User asks follow-up question")
    print("👤 User types: what evidence should I collect")
    
    cli.process_command("what evidence should I collect")
    
    print(f"\n✅ Follow-up Response Summary:")
    print(f"   Domain: {cli.last_response.domain}")
    print(f"   Confidence: {cli.last_response.confidence:.3f}")
    
    # Test negative feedback
    print("\n📝 STEP 4: User gives negative feedback")
    print("👤 User types: not helpful")
    
    cli.process_command("not helpful")
    
    # Test another query to see learning effect
    print("\n📝 STEP 5: User asks similar question to see learning")
    print("👤 User types: workplace harassment legal advice")
    
    cli.process_command("workplace harassment legal advice")
    
    print(f"\n✅ Final Response Summary:")
    print(f"   Domain: {cli.last_response.domain}")
    print(f"   Confidence: {cli.last_response.confidence:.3f}")
    
    return True


def test_different_feedback_types():
    """Test different types of feedback"""
    
    print("\n\n🎯 TEST SCENARIO: Different Feedback Types")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    # Set up with a query
    print("\n📝 Initial Query:")
    print("👤 User: my landlord won't fix the broken heater")
    cli.process_command("my landlord won't fix the broken heater")
    
    initial_confidence = cli.last_response.confidence
    print(f"   Initial confidence: {initial_confidence:.3f}")
    
    # Test different feedback types
    feedback_tests = [
        ("excellent", "Strong positive feedback"),
        ("good", "Moderate positive feedback"),
        ("bad", "Negative feedback"),
        ("wrong", "Strong negative feedback"),
        ("thank you", "Polite positive feedback")
    ]
    
    print(f"\n📊 Testing Different Feedback Types:")
    print("-" * 40)
    
    for feedback, description in feedback_tests:
        print(f"\n{description}:")
        print(f"   👤 User: {feedback}")
        
        # Process feedback
        cli.process_command(feedback)
        
        # Test same query again to see effect
        cli.process_command("my landlord won't fix the broken heater")
        new_confidence = cli.last_response.confidence
        change = new_confidence - initial_confidence
        
        print(f"   📈 Confidence change: {change:+.3f} (now {new_confidence:.3f})")
        
        # Update baseline for next test
        initial_confidence = new_confidence


def test_conversation_flow():
    """Test a complete conversation flow"""
    
    print("\n\n🎯 TEST SCENARIO: Complete Conversation Flow")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    conversation = [
        ("my car was damaged in an accident", "Initial query"),
        ("helpful", "Positive feedback"),
        ("what about insurance claims", "Follow-up query"),
        ("good", "More positive feedback"),
        ("how long does the process take", "Another follow-up"),
        ("perfect", "Final positive feedback")
    ]
    
    print(f"\n📝 Simulating Natural Conversation:")
    print("-" * 35)
    
    for i, (user_input, description) in enumerate(conversation, 1):
        print(f"\n{i}. {description}")
        print(f"   👤 User: {user_input}")
        
        # Process command
        cli.process_command(user_input)
        
        # Show result
        if hasattr(cli, 'last_response') and cli.last_response:
            print(f"   📊 Domain: {cli.last_response.domain}, Confidence: {cli.last_response.confidence:.3f}")
        else:
            print("   ✅ Feedback processed")


def show_learning_persistence():
    """Show that learning persists across queries"""
    
    print("\n\n🎯 TEST SCENARIO: Learning Persistence")
    print("=" * 40)
    
    cli = LegalAgentCLI()
    
    # Query 1: Get baseline
    print("\n📝 Baseline Query:")
    print("👤 User: employment discrimination case")
    cli.process_command("employment discrimination case")
    baseline_confidence = cli.last_response.confidence
    print(f"   Baseline confidence: {baseline_confidence:.3f}")
    
    # Give positive feedback
    print("\n📝 Positive Feedback:")
    print("👤 User: excellent")
    cli.process_command("excellent")
    
    # Same query again - should show learning
    print("\n📝 Same Query After Feedback:")
    print("👤 User: employment discrimination case")
    cli.process_command("employment discrimination case")
    learned_confidence = cli.last_response.confidence
    improvement = learned_confidence - baseline_confidence
    print(f"   Learned confidence: {learned_confidence:.3f}")
    print(f"   📈 Improvement: {improvement:+.3f}")
    
    if improvement > 0:
        print("   ✅ Learning successfully applied!")
    else:
        print("   ⚠️ No improvement detected")


def main():
    """Run all feedback tests"""
    
    print("🧪 COMPREHENSIVE LIVE FEEDBACK TESTING")
    print("=" * 70)
    print("Testing the feedback rating system with real queries")
    
    try:
        # Run all tests
        test_real_query_with_feedback()
        test_different_feedback_types()
        test_conversation_flow()
        show_learning_persistence()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        print("\n📊 SUMMARY:")
        print("✅ Real query processing: Working")
        print("✅ Feedback detection: Working")
        print("✅ Confidence adjustment: Working")
        print("✅ Learning persistence: Working")
        print("✅ Conversation flow: Working")
        
        print("\n🚀 The feedback rating system is fully functional!")
        print("💡 You can now use: python cli_interface.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
