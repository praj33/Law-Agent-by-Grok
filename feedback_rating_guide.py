"""
Feedback Rating System - Complete Guide
=======================================

This guide shows you exactly how to use the feedback rating system
in the Legal Agent CLI interface.

Author: Legal Agent Team
Date: 2025-08-15
"""

def show_feedback_options():
    """Show all available feedback options"""
    
    print("💬 FEEDBACK RATING SYSTEM - HOW TO USE")
    print("=" * 60)
    
    print("\n🎯 AFTER ASKING A LEGAL QUESTION:")
    print("The agent will respond and ask: 'Was this response helpful?'")
    
    print("\n📝 YOU CAN GIVE FEEDBACK IN MULTIPLE WAYS:")
    print("-" * 50)
    
    print("\n1️⃣ SIMPLE FEEDBACK (Just type the word):")
    print("   • helpful")
    print("   • not helpful") 
    print("   • good")
    print("   • bad")
    print("   • wrong")
    print("   • excellent")
    print("   • perfect")
    print("   • poor")
    print("   • useful")
    print("   • useless")
    print("   • thank you")
    print("   • thanks")
    
    print("\n2️⃣ EXPLICIT FEEDBACK (Using 'feedback' command):")
    print("   • feedback helpful")
    print("   • feedback not helpful")
    print("   • feedback excellent")
    print("   • feedback wrong domain")
    print("   • feedback very good")
    print("   • feedback completely wrong")
    
    print("\n3️⃣ NATURAL RESPONSES:")
    print("   • yes (if asked 'was this helpful?')")
    print("   • no (if asked 'was this helpful?')")
    print("   • correct")
    print("   • incorrect")
    print("   • right")
    print("   • accurate")
    
    print("\n🧠 WHAT HAPPENS WHEN YOU GIVE FEEDBACK:")
    print("-" * 50)
    print("✅ Positive feedback (helpful, good, excellent):")
    print("   → Confidence increases (+0.1 to +0.3)")
    print("   → Agent learns this approach works")
    print("   → Similar queries get better responses")
    
    print("\n❌ Negative feedback (not helpful, wrong, bad):")
    print("   → Confidence decreases (-0.1 to -0.2)")
    print("   → Agent learns to avoid this approach")
    print("   → Future responses are adjusted")
    
    print("\n🔄 CONTINUING THE CONVERSATION:")
    print("-" * 50)
    print("After giving feedback, you can:")
    print("   • Ask follow-up questions")
    print("   • Request more details")
    print("   • Ask about next steps")
    print("   • Start a completely new query")


def demonstrate_feedback_flow():
    """Demonstrate the complete feedback flow"""
    
    print("\n\n🎭 DEMONSTRATION: COMPLETE FEEDBACK FLOW")
    print("=" * 60)
    
    print("\n📋 EXAMPLE CONVERSATION:")
    print("-" * 30)
    
    print("👤 User: my landlord is not returning my security deposit")
    print("🤖 Agent: [Provides legal advice about tenant rights...]")
    print("🤖 Agent: Was this response helpful?")
    print("")
    print("👤 User: helpful")
    print("🧠 System: Detected as FEEDBACK ✅")
    print("🤖 Agent: Thank you! The agent has learned from your feedback.")
    print("📈 System: Confidence increased from 0.75 to 0.95")
    print("")
    print("👤 User: what documents do I need?")
    print("🔍 System: Detected as QUERY ✅")
    print("🤖 Agent: [Provides information about required documents...]")
    print("")
    print("👤 User: perfect")
    print("🧠 System: Detected as FEEDBACK ✅")
    print("🤖 Agent: Excellent! Learning applied.")
    print("📈 System: Confidence boosted further")


def show_advanced_features():
    """Show advanced feedback features"""
    
    print("\n\n🚀 ADVANCED FEEDBACK FEATURES")
    print("=" * 50)
    
    print("\n🎯 ADAPTIVE AGENT MODE:")
    print("Start with: python cli_interface.py --adaptive")
    print("Benefits:")
    print("   • Enhanced learning from feedback")
    print("   • Multi-turn conversation tracking")
    print("   • Pattern recognition across sessions")
    print("   • Confidence adjustment over time")
    
    print("\n📊 FEEDBACK STATISTICS:")
    print("Type 'stats' to see:")
    print("   • Total queries processed")
    print("   • Feedback received")
    print("   • Learning improvements")
    print("   • Domain performance")
    
    print("\n🔍 DEBUG MODE:")
    print("The CLI now shows debug messages:")
    print("   🔍 Detected as QUERY: 'your question'")
    print("   🧠 Detected as FEEDBACK: 'helpful'")
    print("   📈 Confidence boost applied: +0.300")


def show_troubleshooting():
    """Show troubleshooting tips"""
    
    print("\n\n🔧 TROUBLESHOOTING FEEDBACK")
    print("=" * 40)
    
    print("\n❓ COMMON ISSUES:")
    print("-" * 20)
    
    print("\n1. 'My feedback is treated as a query'")
    print("   Solution: Make sure you asked a question first")
    print("   The system needs context to detect feedback")
    
    print("\n2. 'I want to give detailed feedback'")
    print("   Use: feedback [your detailed comment]")
    print("   Example: feedback this was very helpful but needs more detail")
    
    print("\n3. 'How do I know if feedback was processed?'")
    print("   Look for: 🧠 Detected as FEEDBACK")
    print("   And: ✅ Thank you! The agent has learned...")
    
    print("\n4. 'Can I give feedback on old responses?'")
    print("   Feedback applies to the most recent response")
    print("   For older responses, ask the question again")
    
    print("\n✅ BEST PRACTICES:")
    print("-" * 20)
    print("   • Give feedback immediately after each response")
    print("   • Be specific: 'helpful' vs 'not helpful'")
    print("   • Use follow-up questions to get more details")
    print("   • Try both simple and explicit feedback methods")


def main():
    """Show complete feedback rating guide"""
    
    print("📚 LEGAL AGENT - FEEDBACK RATING SYSTEM GUIDE")
    print("=" * 70)
    
    show_feedback_options()
    demonstrate_feedback_flow()
    show_advanced_features()
    show_troubleshooting()
    
    print("\n" + "=" * 70)
    print("🚀 QUICK START GUIDE")
    print("=" * 70)
    
    print("\n1️⃣ START THE CLI:")
    print("   python cli_interface.py")
    print("   (or python cli_interface.py --adaptive for enhanced learning)")
    
    print("\n2️⃣ ASK A LEGAL QUESTION:")
    print("   > my employer is not paying overtime")
    
    print("\n3️⃣ GIVE FEEDBACK:")
    print("   > helpful")
    print("   (or 'not helpful', 'good', 'bad', etc.)")
    
    print("\n4️⃣ CONTINUE CONVERSATION:")
    print("   > what should I do next?")
    
    print("\n5️⃣ GIVE MORE FEEDBACK:")
    print("   > excellent")
    
    print("\n🎉 THAT'S IT! The agent learns and improves with each interaction!")
    
    print("\n💡 PRO TIPS:")
    print("   • Watch for debug messages showing detection results")
    print("   • Use 'stats' to see learning progress")
    print("   • Try both simple ('helpful') and explicit ('feedback helpful') methods")
    print("   • Give feedback after each response for best learning")


if __name__ == "__main__":
    main()
