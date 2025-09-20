"""
Test Feedback Learning System
=============================

Test that feedback actually increases confidence when marked as helpful
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

def test_feedback_learning():
    """Test the feedback learning system"""
    
    safe_print("🧠 TESTING FEEDBACK LEARNING SYSTEM")
    safe_print("=" * 60)
    safe_print("Testing that 'helpful' feedback increases confidence")
    safe_print("=" * 60)
    
    from working_enhanced_agent import create_working_enhanced_agent
    agent = create_working_enhanced_agent()
    
    # Test query
    query = "my boss is not giving my salary"
    
    safe_print(f"\n🧪 Step 1: Initial query")
    safe_print(f"Query: \"{query}\"")
    safe_print("-" * 50)
    
    # First query
    response1 = agent.process_query(query)
    initial_confidence = response1.confidence
    
    safe_print(f"Initial result:")
    safe_print(f"  Domain: {response1.domain}")
    safe_print(f"  Confidence: {initial_confidence:.3f}")
    
    # Provide positive feedback
    safe_print(f"\n🧪 Step 2: Providing positive feedback")
    safe_print("-" * 50)
    
    agent.process_feedback(
        query=query,
        domain=response1.domain,
        confidence=response1.confidence,
        feedback="helpful"
    )
    
    # Query again to see learning effect
    safe_print(f"\n🧪 Step 3: Same query after positive feedback")
    safe_print("-" * 50)
    
    response2 = agent.process_query(query)
    learned_confidence = response2.confidence
    
    safe_print(f"After feedback result:")
    safe_print(f"  Domain: {response2.domain}")
    safe_print(f"  Confidence: {learned_confidence:.3f}")
    
    # Check if confidence increased
    safe_print(f"\n📊 LEARNING ANALYSIS:")
    safe_print("=" * 40)
    safe_print(f"Initial confidence: {initial_confidence:.3f}")
    safe_print(f"After feedback: {learned_confidence:.3f}")
    safe_print(f"Change: {learned_confidence - initial_confidence:+.3f}")
    
    if learned_confidence > initial_confidence:
        safe_print(f"✅ SUCCESS! Confidence increased by {learned_confidence - initial_confidence:.3f}")
        safe_print(f"🧠 The agent learned from positive feedback!")
    elif learned_confidence == initial_confidence:
        safe_print(f"⚠️ NO CHANGE: Confidence remained the same")
        safe_print(f"❌ Learning system may not be working")
    else:
        safe_print(f"❌ PROBLEM: Confidence decreased by {initial_confidence - learned_confidence:.3f}")
        safe_print(f"❌ This should not happen with positive feedback")
    
    # Test negative feedback
    safe_print(f"\n🧪 Step 4: Testing negative feedback")
    safe_print("-" * 50)
    
    agent.process_feedback(
        query=query,
        domain=response2.domain,
        confidence=response2.confidence,
        feedback="not helpful"
    )
    
    response3 = agent.process_query(query)
    negative_confidence = response3.confidence
    
    safe_print(f"After negative feedback:")
    safe_print(f"  Domain: {response3.domain}")
    safe_print(f"  Confidence: {negative_confidence:.3f}")
    safe_print(f"  Change from previous: {negative_confidence - learned_confidence:+.3f}")
    
    # Test multiple positive feedbacks
    safe_print(f"\n🧪 Step 5: Multiple positive feedbacks")
    safe_print("-" * 50)
    
    for i in range(3):
        agent.process_feedback(
            query=query,
            domain=response3.domain,
            confidence=response3.confidence,
            feedback="very helpful"
        )
        safe_print(f"  Positive feedback #{i+1} processed")
    
    response4 = agent.process_query(query)
    final_confidence = response4.confidence
    
    safe_print(f"\nAfter multiple positive feedbacks:")
    safe_print(f"  Domain: {response4.domain}")
    safe_print(f"  Confidence: {final_confidence:.3f}")
    
    safe_print(f"\n🎯 FINAL RESULTS:")
    safe_print("=" * 40)
    safe_print(f"Initial:           {initial_confidence:.3f}")
    safe_print(f"After 1 positive:  {learned_confidence:.3f} ({learned_confidence - initial_confidence:+.3f})")
    safe_print(f"After 1 negative:  {negative_confidence:.3f} ({negative_confidence - learned_confidence:+.3f})")
    safe_print(f"After 3 positive:  {final_confidence:.3f} ({final_confidence - negative_confidence:+.3f})")
    
    if final_confidence > initial_confidence:
        safe_print(f"✅ OVERALL SUCCESS! Learning system is working")
    else:
        safe_print(f"❌ OVERALL ISSUE: Learning system needs improvement")

def main():
    """Main test function"""
    
    test_feedback_learning()
    
    safe_print(f"\n🚀 TEST YOUR CLI WITH FEEDBACK:")
    safe_print("=" * 50)
    safe_print("1. Run: python cli_interface.py")
    safe_print("2. Ask: my boss is not giving my salary")
    safe_print("3. Give feedback: feedback helpful")
    safe_print("4. Ask the same query again")
    safe_print("5. Confidence should increase!")

if __name__ == "__main__":
    main()
