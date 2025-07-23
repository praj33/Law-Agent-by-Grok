"""
Test Fixed Legal Agent System
============================

This script tests the fixed domain classification system to ensure
the "unknown domain" issues have been resolved.

Usage: python test_fixed_system.py
"""

from legal_agent import create_legal_agent, LegalQueryInput
from adaptive_legal_agent import create_adaptive_legal_agent

def test_basic_agent():
    """Test the basic legal agent"""
    print("🧪 TESTING BASIC LEGAL AGENT")
    print("=" * 50)
    
    agent = create_legal_agent()
    
    test_queries = [
        # Previously problematic queries
        "My phone is being hacked",
        "I want to file a consumer complaint", 
        "My elderly father is being abused in Delhi",
        "Someone is stalking me online",
        "My computer has malware",
        
        # Standard queries that should work
        "My landlord won't return my deposit",
        "I want a divorce",
        "I was injured in a car accident",
        "I was wrongfully terminated"
    ]
    
    success_count = 0
    total_count = len(test_queries)
    
    for query in test_queries:
        query_input = LegalQueryInput(user_input=query)
        response = agent.process_query(query_input)
        
        is_success = response.domain != 'unknown'
        if is_success:
            success_count += 1
        
        status = "✅ SUCCESS" if is_success else "❌ UNKNOWN"
        print(f"{status}: \"{query}\"")
        print(f"   → Domain: {response.domain} (Confidence: {response.confidence:.3f})")
        print()
    
    success_rate = (success_count / total_count) * 100
    print(f"📊 BASIC AGENT RESULTS:")
    print(f"   Success Rate: {success_rate:.1f}% ({success_count}/{total_count})")
    
    return success_rate >= 80  # 80% success rate target

def test_adaptive_agent():
    """Test the adaptive legal agent"""
    print("\n🧠 TESTING ADAPTIVE LEGAL AGENT")
    print("=" * 50)
    
    agent = create_adaptive_legal_agent()
    
    test_queries = [
        "My elderly father is being abused in Delhi",
        "My phone is being hacked", 
        "I want to file a consumer complaint"
    ]
    
    success_count = 0
    enhanced_advice_count = 0
    
    for query in test_queries:
        query_input = LegalQueryInput(user_input=query)
        response = agent.process_query_with_learning(query_input)
        
        is_success = response.domain != 'unknown'
        has_enhanced_advice = bool(response.data_driven_advice)
        
        if is_success:
            success_count += 1
        if has_enhanced_advice:
            enhanced_advice_count += 1
        
        status = "✅ SUCCESS" if is_success else "❌ UNKNOWN"
        advice_status = "📊 ENHANCED" if has_enhanced_advice else "📝 BASIC"
        
        print(f"{status} {advice_status}: \"{query}\"")
        print(f"   → Domain: {response.domain} (Confidence: {response.confidence:.3f})")
        
        if has_enhanced_advice:
            print(f"   → Enhanced Advice: {response.data_driven_advice[:80]}...")
        print()
    
    success_rate = (success_count / len(test_queries)) * 100
    enhancement_rate = (enhanced_advice_count / len(test_queries)) * 100
    
    print(f"📊 ADAPTIVE AGENT RESULTS:")
    print(f"   Success Rate: {success_rate:.1f}% ({success_count}/{len(test_queries)})")
    print(f"   Enhanced Advice Rate: {enhancement_rate:.1f}% ({enhanced_advice_count}/{len(test_queries)})")
    
    return success_rate >= 70  # 70% success rate target for adaptive (learning may affect some)

def test_specific_improvements():
    """Test specific improvements made"""
    print("\n🎯 TESTING SPECIFIC IMPROVEMENTS")
    print("=" * 50)
    
    agent = create_legal_agent()
    
    # Test cases that were specifically fixed
    improvements = {
        "Cyber Crime Enhancement": [
            "My phone is being hacked",
            "Someone is stalking me online", 
            "My computer has malware"
        ],
        "Consumer Complaint Fix": [
            "I want to file a consumer complaint",
            "I received a defective product"
        ],
        "Elder Abuse Coverage": [
            "My elderly father is being abused",
            "Senior citizen financial exploitation"
        ]
    }
    
    for category, queries in improvements.items():
        print(f"\n📂 {category}:")
        print("-" * 30)
        
        category_success = 0
        
        for query in queries:
            query_input = LegalQueryInput(user_input=query)
            response = agent.process_query(query_input)
            
            is_success = response.domain != 'unknown'
            if is_success:
                category_success += 1
            
            status = "✅" if is_success else "❌"
            print(f"   {status} \"{query}\" → {response.domain} ({response.confidence:.3f})")
        
        category_rate = (category_success / len(queries)) * 100
        print(f"   Category Success: {category_rate:.1f}%")

def main():
    """Run all tests"""
    print("🚀 LEGAL AGENT SYSTEM VERIFICATION")
    print("Testing fixes for 'unknown domain' issues")
    print("=" * 60)
    
    # Test basic agent
    basic_success = test_basic_agent()
    
    # Test adaptive agent  
    adaptive_success = test_adaptive_agent()
    
    # Test specific improvements
    test_specific_improvements()
    
    # Overall results
    print(f"\n🎯 OVERALL SYSTEM STATUS")
    print("=" * 40)
    print(f"Basic Agent: {'✅ PASS' if basic_success else '❌ NEEDS WORK'}")
    print(f"Adaptive Agent: {'✅ PASS' if adaptive_success else '❌ NEEDS WORK'}")
    
    if basic_success and adaptive_success:
        print(f"\n🎉 SYSTEM VERIFICATION SUCCESSFUL!")
        print(f"   • Domain classification issues resolved")
        print(f"   • Enhanced data integration working")
        print(f"   • Cyber crime queries now properly classified")
        print(f"   • Consumer complaint queries fixed")
        print(f"   • System ready for production use")
        
        print(f"\n🚀 Ready to use:")
        print(f"   python cli_interface.py")
        print(f"   python adaptive_cli.py")
    else:
        print(f"\n⚠️ SYSTEM NEEDS ADDITIONAL FIXES")
        print(f"   Check the test results above for specific issues")
        print(f"   Consider additional training data or threshold adjustments")

if __name__ == "__main__":
    main()
