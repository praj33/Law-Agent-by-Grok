"""
Test Phone Theft Scenario - Exact User Issue
============================================

This script tests the exact scenario the user described:
1. Query: "my phone got stolen in market"
2. Feedback: "helpful" 
3. Follow-up: "what about filing a complaint"

Tests both detection and processing to identify any issues.

Author: Legal Agent Team
Date: 2025-08-15
"""

from cli_interface import LegalAgentCLI
import time


def test_exact_user_scenario():
    """Test the exact scenario the user described"""
    
    print("📱 TESTING EXACT USER SCENARIO")
    print("=" * 50)
    print("Scenario: Phone theft -> feedback -> follow-up question")
    
    # Create CLI instance
    cli = LegalAgentCLI()
    
    print("\n🔍 STEP 1: Initial Query")
    print("-" * 30)
    print("👤 User types: 'my phone got stolen in market'")
    
    # Process initial query exactly as CLI would
    initial_query = "my phone got stolen in market"
    cli.process_query(initial_query)
    
    print(f"✅ Query processed successfully")
    print(f"   Domain: {cli.last_response.domain}")
    print(f"   Confidence: {cli.last_response.confidence:.3f}")
    print(f"   Session ID: {cli.session_id}")
    
    print("\n🧠 STEP 2: User Feedback")
    print("-" * 30)
    print("👤 User types: 'helpful'")
    
    # Test feedback detection and processing
    feedback_input = "helpful"
    is_feedback = cli.is_feedback_response(feedback_input.lower())
    
    print(f"🔍 Detection result: {'FEEDBACK' if is_feedback else 'QUERY'}")
    
    if is_feedback:
        print("✅ Correctly detected as feedback")
        cli.process_feedback(feedback_input)
        print("✅ Feedback processed successfully")
    else:
        print("❌ ERROR: Should be detected as feedback!")
        return False
    
    print("\n💬 STEP 3: Follow-up Question")
    print("-" * 30)
    print("👤 User types: 'what about filing a complaint'")
    
    # Test follow-up detection and processing
    followup_input = "what about filing a complaint"
    is_feedback_followup = cli.is_feedback_response(followup_input.lower())
    
    print(f"🔍 Detection result: {'FEEDBACK' if is_feedback_followup else 'QUERY'}")
    
    if not is_feedback_followup:
        print("✅ Correctly detected as new query")
        
        # Process as new query
        print("🤖 Processing follow-up query...")
        cli.process_query(followup_input)
        
        print(f"✅ Follow-up processed successfully")
        print(f"   Domain: {cli.last_response.domain}")
        print(f"   Confidence: {cli.last_response.confidence:.3f}")
        
        return True
    else:
        print("❌ ERROR: Should be detected as query, not feedback!")
        return False


def test_command_processing_logic():
    """Test the command processing logic step by step"""
    
    print("\n\n🔧 TESTING COMMAND PROCESSING LOGIC")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    # Set up context
    cli.last_query = "my phone got stolen in market"
    cli.last_response = type('MockResponse', (), {
        'domain': 'criminal_law',
        'confidence': 0.9,
        'session_id': 'test_session'
    })()
    
    test_inputs = [
        ("helpful", "Should be FEEDBACK"),
        ("not helpful", "Should be FEEDBACK"),
        ("what about filing a complaint", "Should be QUERY"),
        ("how do I file a police report", "Should be QUERY"),
        ("good", "Should be FEEDBACK"),
        ("what are the next steps", "Should be QUERY"),
        ("thank you", "Should be FEEDBACK"),
        ("can I get compensation", "Should be QUERY")
    ]
    
    print("\nTesting various inputs:")
    all_correct = True
    
    for test_input, expected in test_inputs:
        # Simulate the CLI's command processing logic
        command_lower = test_input.lower()
        
        if command_lower in ['quit', 'exit', 'q']:
            detected_as = "QUIT"
        elif command_lower in ['help', 'h']:
            detected_as = "HELP"
        elif command_lower.startswith('query '):
            detected_as = "QUERY (explicit)"
        elif command_lower.startswith('feedback '):
            detected_as = "FEEDBACK (explicit)"
        elif command_lower == 'stats':
            detected_as = "STATS"
        elif command_lower == 'clear':
            detected_as = "CLEAR"
        elif cli.is_feedback_response(command_lower):
            detected_as = "FEEDBACK (detected)"
        else:
            detected_as = "QUERY (default)"
        
        # Check if detection matches expectation
        if "FEEDBACK" in expected and "FEEDBACK" in detected_as:
            result = "✅ CORRECT"
        elif "QUERY" in expected and "QUERY" in detected_as:
            result = "✅ CORRECT"
        else:
            result = "❌ WRONG"
            all_correct = False
        
        print(f"  '{test_input}' -> {detected_as} {result}")
        print(f"    Expected: {expected}")
    
    return all_correct


def simulate_interactive_session():
    """Simulate an interactive CLI session"""
    
    print("\n\n🎭 SIMULATING INTERACTIVE CLI SESSION")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    # Simulate the exact user interaction
    commands = [
        "my phone got stolen in market",
        "helpful", 
        "what about filing a complaint"
    ]
    
    print("\nSimulating user commands:")
    
    for i, command in enumerate(commands, 1):
        print(f"\n--- Command {i} ---")
        print(f"👤 User: {command}")
        
        # Process command through CLI logic
        try:
            cli.process_command(command)
            print("✅ Command processed successfully")
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            return False
    
    return True


def main():
    """Run all tests"""
    
    print("🧪 COMPREHENSIVE PHONE THEFT SCENARIO TEST")
    print("=" * 60)
    print("Testing the exact issue reported by the user")
    
    # Run tests
    test1_passed = test_exact_user_scenario()
    test2_passed = test_command_processing_logic()
    test3_passed = simulate_interactive_session()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"✅ Exact User Scenario: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Command Processing Logic: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Interactive Session Simulation: {'PASSED' if test3_passed else 'FAILED'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The phone theft scenario is working correctly")
        print("✅ 'helpful' is detected as feedback")
        print("✅ 'what about filing a complaint' is detected as query")
        print("✅ No issues found with the current implementation")
        
        print("\n💡 If you're still experiencing issues:")
        print("1. Make sure you're using the latest CLI: python cli_interface.py")
        print("2. Try the adaptive version: python cli_interface.py --adaptive")
        print("3. Check that you have a previous query before giving feedback")
        
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("⚠️ There may be an issue with the implementation")
    
    return all_passed


if __name__ == "__main__":
    main()
