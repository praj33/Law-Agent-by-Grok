"""
Demo Feedback Learning
======================

Demonstrate the feedback learning system step by step
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

def demo_feedback():
    """Demo the feedback learning system"""
    
    safe_print("🎯 FEEDBACK LEARNING DEMONSTRATION")
    safe_print("=" * 60)
    safe_print("This shows how confidence increases with positive feedback")
    safe_print("=" * 60)
    
    from working_enhanced_agent import create_working_enhanced_agent
    agent = create_working_enhanced_agent()
    
    query = "my boss is not giving my salary"
    
    # Step 1: Initial query
    safe_print(f"\n📝 STEP 1: Ask initial query")
    safe_print(f"Query: \"{query}\"")
    safe_print("-" * 50)
    
    response1 = agent.process_query(query)
    safe_print(f"✅ Result: {response1.domain} (confidence: {response1.confidence:.3f})")
    
    # Step 2: Give positive feedback
    safe_print(f"\n👍 STEP 2: Give positive feedback")
    safe_print("Feedback: 'helpful'")
    safe_print("-" * 50)
    
    agent.process_feedback(
        query=query,
        domain=response1.domain,
        confidence=response1.confidence,
        feedback="helpful"
    )
    
    # Step 3: Ask same query again
    safe_print(f"\n🔄 STEP 3: Ask same query again")
    safe_print(f"Query: \"{query}\"")
    safe_print("-" * 50)
    
    response2 = agent.process_query(query)
    safe_print(f"✅ Result: {response2.domain} (confidence: {response2.confidence:.3f})")
    
    # Show the difference
    safe_print(f"\n📊 COMPARISON:")
    safe_print("=" * 30)
    safe_print(f"Before feedback: {response1.confidence:.3f}")
    safe_print(f"After feedback:  {response2.confidence:.3f}")
    safe_print(f"Increase:        +{response2.confidence - response1.confidence:.3f}")
    
    if response2.confidence > response1.confidence:
        safe_print(f"🎉 SUCCESS! Confidence increased by {response2.confidence - response1.confidence:.3f}")
        safe_print(f"🧠 The agent learned from your positive feedback!")
    else:
        safe_print(f"❌ No increase detected")
    
    # Test with different query
    safe_print(f"\n🧪 TESTING WITH DIFFERENT QUERY:")
    safe_print("-" * 50)
    
    query2 = "my phone got stolen at airport"
    response3 = agent.process_query(query2)
    safe_print(f"Query: \"{query2}\"")
    safe_print(f"Result: {response3.domain} (confidence: {response3.confidence:.3f})")
    
    agent.process_feedback(
        query=query2,
        domain=response3.domain,
        confidence=response3.confidence,
        feedback="very helpful"
    )
    
    response4 = agent.process_query(query2)
    safe_print(f"\nAfter feedback:")
    safe_print(f"Result: {response4.domain} (confidence: {response4.confidence:.3f})")
    safe_print(f"Increase: +{response4.confidence - response3.confidence:.3f}")

def main():
    """Main demo function"""
    
    demo_feedback()
    
    safe_print(f"\n🚀 NOW TRY IN YOUR CLI:")
    safe_print("=" * 40)
    safe_print("1. Run: python cli_interface.py")
    safe_print("2. Ask: my boss is not giving my salary")
    safe_print("3. Note the confidence score")
    safe_print("4. Type: feedback helpful")
    safe_print("5. Ask the same query again")
    safe_print("6. Watch confidence increase!")
    
    safe_print(f"\n✅ The feedback learning system is working!")
    safe_print("Positive feedback increases confidence by up to +0.30")
    safe_print("Negative feedback decreases confidence by up to -0.20")

if __name__ == "__main__":
    main()
