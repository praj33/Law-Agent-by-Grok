"""
Confidence Score Analysis
========================

Analyze why confidence scores might appear to change when asking the same query.
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

def analyze_confidence_logic():
    """Analyze the confidence calculation logic"""
    
    safe_print("🔍 CONFIDENCE SCORE ANALYSIS")
    safe_print("=" * 50)
    
    # Test 1: ML Classifier Consistency
    safe_print("\n1. Testing ML Classifier Consistency:")
    safe_print("-" * 40)
    
    from ml_domain_classifier import create_ml_domain_classifier
    classifier = create_ml_domain_classifier()
    
    query = "my neighbor girl is being harassed"
    safe_print(f"Query: \"{query}\"")
    
    safe_print("\nML Classifier Results (5 attempts):")
    for i in range(5):
        domain, confidence, alternatives = classifier.classify_with_confidence(query)
        safe_print(f"  Attempt {i+1}: {domain} (confidence: {confidence:.6f})")
    
    # Test 2: Enhanced Working Agent
    safe_print(f"\n2. Testing Enhanced Working Agent:")
    safe_print("-" * 40)
    
    from working_enhanced_agent import create_working_enhanced_agent
    agent = create_working_enhanced_agent()
    
    safe_print(f"Enhanced Agent Results (3 attempts):")
    for i in range(3):
        response = agent.process_query(query)
        safe_print(f"  Attempt {i+1}: {response.domain} (confidence: {response.confidence:.6f})")
    
    # Test 3: Explain the Logic
    safe_print(f"\n3. Confidence Calculation Logic:")
    safe_print("-" * 40)
    
    safe_print("🧠 ML Classifier Logic:")
    safe_print("   Formula: (Naive Bayes * 0.7) + (Cosine Similarity * 0.3)")
    safe_print("   Result: DETERMINISTIC - Same input = Same output")
    
    safe_print("\n🔧 Enhanced Agent Logic:")
    safe_print("   1. Get ML confidence (always same)")
    safe_print("   2. If confidence < 0.15 OR domain = 'unknown':")
    safe_print("      → Run enhanced_unknown_analysis()")
    safe_print("   3. Enhanced analysis uses FIXED confidence values:")
    safe_print("      → neighbor_harassment: 0.75")
    safe_print("      → sexual_harassment: 0.85")
    safe_print("      → workplace_harassment: 0.80")
    safe_print("   4. Result: DETERMINISTIC - Same input = Same output")
    
    # Test 4: Show the actual calculation
    safe_print(f"\n4. Step-by-Step Calculation for Your Query:")
    safe_print("-" * 40)
    
    # Simulate the calculation
    ml_domain, ml_confidence, ml_alternatives = classifier.classify_with_confidence(query)
    safe_print(f"Step 1 - ML Result: {ml_domain} (confidence: {ml_confidence:.6f})")
    
    if ml_domain == "unknown" or ml_confidence < 0.15:
        safe_print(f"Step 2 - ML confidence {ml_confidence:.6f} < 0.15, so run enhanced analysis")
        
        # Check harassment detection
        query_lower = query.lower()
        harassment_indicators = ['harass', 'bother', 'trouble', 'disturb', 'threaten', 'intimidat', 'stalk', 'abuse']
        has_harassment = any(indicator in query_lower for indicator in harassment_indicators)
        
        if has_harassment:
            safe_print(f"Step 3 - Harassment detected: YES")
            
            # Check neighbor harassment
            neighbor_keywords = ['neighbor', 'neighbour', 'building', 'society']
            has_neighbor = any(keyword in query_lower for keyword in neighbor_keywords)
            
            if has_neighbor:
                safe_print(f"Step 4 - Neighbor harassment detected: YES")
                safe_print(f"Step 5 - Final result: criminal_law (confidence: 0.750)")
                safe_print(f"         This is a FIXED value, not calculated!")
            else:
                safe_print(f"Step 4 - No specific harassment type detected")
        else:
            safe_print(f"Step 3 - No harassment detected")
    else:
        safe_print(f"Step 2 - ML confidence {ml_confidence:.6f} >= 0.15, use ML result")
    
    # Test 5: Why it might seem to change
    safe_print(f"\n5. Why Confidence Might Seem to Change:")
    safe_print("-" * 40)
    
    safe_print("❌ NOT because of learning/feedback (that's not implemented)")
    safe_print("❌ NOT because of randomness (calculations are deterministic)")
    safe_print("❌ NOT because of session memory (each query is independent)")
    
    safe_print("\n✅ Possible reasons for perceived changes:")
    safe_print("   1. Different query wording (even slight changes)")
    safe_print("   2. Typos or extra spaces")
    safe_print("   3. Different system state (rare)")
    safe_print("   4. Looking at different parts of output")
    safe_print("   5. Comparing ML confidence vs Enhanced confidence")
    
    # Test 6: Demonstrate with variations
    safe_print(f"\n6. Testing Query Variations:")
    safe_print("-" * 40)
    
    variations = [
        "my neighbor girl is being harassed",
        "my neighbour girl is being harassed",  # British spelling
        "my neighbor girl is being harassed.",  # With period
        " my neighbor girl is being harassed ",  # With spaces
        "My neighbor girl is being harassed",   # Capitalized
    ]
    
    for variation in variations:
        response = agent.process_query(variation)
        safe_print(f"'{variation}' → {response.confidence:.6f}")

def main():
    """Main analysis function"""
    
    analyze_confidence_logic()
    
    safe_print(f"\n🎯 CONCLUSION:")
    safe_print("=" * 30)
    safe_print("The confidence scores are DETERMINISTIC and should NOT increase")
    safe_print("for the exact same query. If you're seeing changes, it's likely due to:")
    safe_print("1. Slight differences in query wording")
    safe_print("2. Comparing different types of confidence scores")
    safe_print("3. System state differences (very rare)")
    
    safe_print(f"\n📊 For your specific query:")
    safe_print("'my neighbor girl is being harassed' should ALWAYS return:")
    safe_print("Domain: criminal_law")
    safe_print("Confidence: 0.750000 (exactly)")
    safe_print("This is a FIXED value in the harassment detection logic!")

if __name__ == "__main__":
    main()
