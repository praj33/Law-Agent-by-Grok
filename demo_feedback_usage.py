"""
Practical Feedback Usage Demo
=============================

This script shows you exactly how to use the feedback system
with real examples and step-by-step instructions.
"""

from cli_interface import LegalAgentCLI
import time

def demo_basic_feedback():
    """Demonstrate basic feedback usage"""
    
    print("🎯 DEMO 1: BASIC FEEDBACK USAGE")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    print("\n📝 STEP 1: Ask a legal question")
    print("👤 You type: my boss is not paying overtime")
    
    # Process query
    cli.process_command("my boss is not paying overtime")
    
    print(f"\n✅ Agent responded with:")
    print(f"   Domain: {cli.last_response.domain}")
    print(f"   Confidence: {cli.last_response.confidence:.3f}")
    
    print("\n📝 STEP 2: Give simple feedback")
    print("👤 You type: helpful")
    
    # Process feedback
    cli.process_command("helpful")
    
    print("\n✅ Feedback processed! The agent learned from your input.")


def demo_different_feedback_types():
    """Demonstrate different types of feedback"""
    
    print("\n\n🎯 DEMO 2: DIFFERENT FEEDBACK TYPES")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    # Set up context
    cli.process_command("workplace harassment issue")
    
    feedback_examples = [
        ("helpful", "Simple positive feedback"),
        ("not helpful", "Simple negative feedback"),
        ("feedback excellent", "Explicit positive feedback"),
        ("feedback wrong domain", "Explicit negative with reason"),
        ("good", "Short positive"),
        ("bad", "Short negative"),
        ("thank you", "Polite positive"),
        ("wrong", "Direct negative")
    ]
    
    print("\n📝 DIFFERENT WAYS TO GIVE FEEDBACK:")
    print("-" * 40)
    
    for feedback, description in feedback_examples:
        is_feedback = cli.is_feedback_response(feedback.lower())
        detection = "✅ FEEDBACK" if is_feedback else "❌ QUERY"
        print(f"   '{feedback}' → {detection} ({description})")


def demo_conversation_flow():
    """Demonstrate complete conversation flow with feedback"""
    
    print("\n\n🎯 DEMO 3: COMPLETE CONVERSATION FLOW")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    conversation_steps = [
        ("my phone got stolen", "Initial query"),
        ("helpful", "Positive feedback"),
        ("what about filing complaint", "Follow-up query"),
        ("good", "More positive feedback"),
        ("how long does it take", "Another follow-up"),
        ("perfect", "Final positive feedback")
    ]
    
    print("\n📝 CONVERSATION SIMULATION:")
    print("-" * 30)
    
    for i, (user_input, description) in enumerate(conversation_steps, 1):
        print(f"\n{i}. {description}")
        print(f"   👤 User: {user_input}")
        
        # Determine what system will detect
        if i == 1:  # First query
            detection = "QUERY"
        else:
            is_feedback = cli.is_feedback_response(user_input.lower())
            detection = "FEEDBACK" if is_feedback else "QUERY"
        
        print(f"   🧠 System: Detected as {detection}")
        
        # Process the command
        cli.process_command(user_input)
        
        if detection == "FEEDBACK":
            print("   ✅ Feedback processed, learning applied")
        else:
            print(f"   ✅ Query processed, domain: {cli.last_response.domain}")


def show_feedback_effects():
    """Show the effects of feedback on the system"""
    
    print("\n\n🎯 DEMO 4: FEEDBACK EFFECTS")
    print("=" * 50)
    
    cli = LegalAgentCLI()
    
    print("\n📊 TESTING CONFIDENCE CHANGES:")
    print("-" * 35)
    
    # Initial query
    print("\n1. Initial query:")
    print("   👤 User: employment law question")
    cli.process_command("employment law question")
    initial_confidence = cli.last_response.confidence
    print(f"   📈 Initial confidence: {initial_confidence:.3f}")
    
    # Positive feedback
    print("\n2. Positive feedback:")
    print("   👤 User: excellent")
    cli.process_command("excellent")
    
    # Same query again to see effect
    print("\n3. Same query after positive feedback:")
    print("   👤 User: employment law question")
    cli.process_command("employment law question")
    after_positive = cli.last_response.confidence
    print(f"   📈 Confidence after positive feedback: {after_positive:.3f}")
    print(f"   📊 Change: {after_positive - initial_confidence:+.3f}")
    
    # Negative feedback
    print("\n4. Negative feedback:")
    print("   👤 User: not helpful")
    cli.process_command("not helpful")
    
    # Same query again
    print("\n5. Same query after negative feedback:")
    print("   👤 User: employment law question")
    cli.process_command("employment law question")
    after_negative = cli.last_response.confidence
    print(f"   📈 Confidence after negative feedback: {after_negative:.3f}")
    print(f"   📊 Change from positive: {after_negative - after_positive:+.3f}")


def show_practical_tips():
    """Show practical tips for using feedback"""
    
    print("\n\n💡 PRACTICAL TIPS FOR USING FEEDBACK")
    print("=" * 50)
    
    print("\n✅ DO:")
    print("   • Give feedback immediately after each response")
    print("   • Use simple words: 'helpful', 'good', 'bad'")
    print("   • Be consistent with your feedback style")
    print("   • Use follow-up questions after feedback")
    print("   • Try the adaptive mode: --adaptive")
    
    print("\n❌ DON'T:")
    print("   • Give feedback without asking a question first")
    print("   • Use very long sentences as feedback")
    print("   • Mix feedback with new questions in one input")
    print("   • Expect feedback on very old responses")
    
    print("\n🎯 BEST FEEDBACK EXAMPLES:")
    print("   Instead of: 'This response was somewhat helpful but could be better'")
    print("   Use: 'helpful' (then ask follow-up questions)")
    print("")
    print("   Instead of: 'The legal advice seems wrong for my situation'")
    print("   Use: 'wrong' or 'not helpful'")
    print("")
    print("   Instead of: 'Can you explain more about this helpful information?'")
    print("   Use: 'helpful' (then ask: 'can you explain more?')")


def main():
    """Run all feedback usage demos"""
    
    print("🎓 FEEDBACK RATING SYSTEM - PRACTICAL USAGE GUIDE")
    print("=" * 70)
    
    demo_basic_feedback()
    demo_different_feedback_types()
    demo_conversation_flow()
    show_feedback_effects()
    show_practical_tips()
    
    print("\n" + "=" * 70)
    print("🚀 NOW YOU'RE READY TO USE THE FEEDBACK SYSTEM!")
    print("=" * 70)
    
    print("\n📋 QUICK REFERENCE:")
    print("   Start CLI: python cli_interface.py")
    print("   Ask question: [your legal question]")
    print("   Give feedback: helpful / not helpful / good / bad")
    print("   Continue: [follow-up questions]")
    print("   See stats: stats")
    print("   Get help: help")
    print("   Quit: quit")
    
    print("\n🎉 The agent will learn and improve with every interaction!")
    print("💡 Watch for debug messages to see what the system detects!")


if __name__ == "__main__":
    main()
