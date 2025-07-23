"""
Legal Agent System Demo
======================

This script demonstrates all the key features of the Legal Agent System.
Run this to see the system in action!

Usage: python demo.py
"""

import json
from legal_agent import create_legal_agent, LegalQueryInput
from data_integration import CrimeDataAnalyzer

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_subheader(title):
    """Print a formatted subheader"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_basic_queries():
    """Demo basic legal query processing"""
    print_header("BASIC LEGAL QUERY PROCESSING")
    
    agent = create_legal_agent()
    
    test_queries = [
        "My landlord won't return my security deposit in Mumbai",
        "I want to divorce my husband and get custody",
        "My elderly father is being neglected in Delhi",
        "Someone hacked my bank account online"
    ]
    
    for i, query_text in enumerate(test_queries, 1):
        print_subheader(f"Query {i}: {query_text}")
        
        query = LegalQueryInput(user_input=query_text)
        response = agent.process_query(query)
        
        print(f"🏛️  Domain: {response.domain.title()}")
        print(f"🎯 Confidence: {response.confidence:.2f}")
        print(f"⏱️  Timeline: {response.timeline}")
        print(f"📝 Legal Route: {response.legal_route}")
        print(f"📋 Process Steps: {len(response.process_steps)} steps")
        
        if response.glossary:
            print(f"📚 Legal Terms Found: {', '.join(response.glossary.keys())}")
        
        if response.data_driven_advice:
            print(f"📊 Data-Driven Advice: Available")
            print(f"⚠️  Risk Level: {response.risk_assessment}")

def demo_data_integration():
    """Demo crime data integration features"""
    print_header("CRIME DATA INTEGRATION")
    
    try:
        analyzer = CrimeDataAnalyzer()
        
        print_subheader("High-Risk States for Senior Citizen Crimes")
        high_risk_states = analyzer.get_high_risk_states(50.0)
        
        for i, state in enumerate(high_risk_states[:5], 1):
            print(f"{i}. {state.state_ut}: {state.crime_rate_2022} per lakh population")
            print(f"   Trend: {state.crime_trend}, Chargesheeting: {state.chargesheeting_rate_2022}%")
        
        print_subheader("Location-Specific Analysis")
        locations = ["Delhi", "Maharashtra", "Tamil Nadu"]
        
        for location in locations:
            advice = analyzer.get_location_based_advice(location, "senior_citizen_abuse")
            if advice['location_found']:
                print(f"\n🌍 {location}:")
                print(f"   Risk Level: {advice['risk_level'].replace('_', ' ').title()}")
                print(f"   Crime Rate: {advice['crime_rate_2022']} per lakh")
                print(f"   Trend: {advice['crime_trend'].title()}")
        
        print_subheader("Overall Crime Trends")
        trends = analyzer.analyze_crime_trends()
        print(f"📈 Total Crimes 2022: {trends['total_crimes']['2022']:,}")
        print(f"📊 Overall Trend: {trends['overall_trend'].title()}")
        print(f"⚖️  Average Chargesheeting Rate: {trends['average_chargesheeting_rate']}%")
        print(f"🔴 Highest Crime Rate: {trends['highest_crime_rate_state']}")
        print(f"🟢 Lowest Crime Rate: {trends['lowest_crime_rate_state']}")
        
    except Exception as e:
        print(f"❌ Data integration error: {e}")

def demo_feedback_system():
    """Demo feedback collection and analysis"""
    print_header("FEEDBACK SYSTEM")
    
    agent = create_legal_agent()
    
    print_subheader("Collecting Feedback")
    
    # Simulate some feedback
    feedback_queries = [
        ("Tenant rights query", "helpful"),
        ("Family law question", "very helpful"),
        ("Employment issue", "not helpful")
    ]
    
    for query_text, feedback in feedback_queries:
        query = LegalQueryInput(user_input=query_text, feedback=feedback)
        response = agent.process_query(query)
        print(f"✅ Collected feedback '{feedback}' for {response.domain} query")
    
    print_subheader("Feedback Statistics")
    stats = agent.get_feedback_stats()
    
    print(f"📊 Total Feedback Entries: {stats['total_feedback']}")
    print(f"📈 Positive Feedback: {stats['positive_percentage']:.1f}%")
    
    if stats['domains']:
        print(f"🏛️  Most Queried Domains:")
        for domain, count in list(stats['domains'].items())[:3]:
            print(f"   • {domain.title()}: {count} queries")

def demo_performance():
    """Demo system performance"""
    print_header("SYSTEM PERFORMANCE")
    
    import time
    
    agent = create_legal_agent()
    
    print_subheader("Response Time Test")
    
    test_queries = [
        "Quick tenant rights question",
        "Family law query with location in Mumbai",
        "Elder abuse case in Delhi with data integration"
    ]
    
    total_time = 0
    for i, query_text in enumerate(test_queries, 1):
        start_time = time.time()
        
        query = LegalQueryInput(user_input=query_text)
        response = agent.process_query(query)
        
        end_time = time.time()
        response_time = end_time - start_time
        total_time += response_time
        
        print(f"Query {i}: {response_time:.3f}s - {response.domain}")
    
    avg_time = total_time / len(test_queries)
    print(f"\n⚡ Average Response Time: {avg_time:.3f}s")
    print(f"🎯 Performance Target: <2.0s {'✅ PASS' if avg_time < 2.0 else '❌ FAIL'}")

def demo_api_usage():
    """Demo different ways to use the API"""
    print_header("API USAGE EXAMPLES")
    
    print_subheader("Python API")
    print("""
# Basic usage
from legal_agent import create_legal_agent, LegalQueryInput

agent = create_legal_agent()
query = LegalQueryInput(user_input="Your legal question")
response = agent.process_query(query)
print(response.to_json())
""")
    
    print_subheader("FastAPI Server")
    print("""
# Start server
uvicorn main:app --reload

# Access endpoints
curl -X POST "http://127.0.0.1:8000/legal-query" \\
     -H "Content-Type: application/json" \\
     -d '{"user_input": "Legal question", "feedback": null}'
""")
    
    print_subheader("CLI Interface")
    print("""
# Interactive interface
python cli_interface.py

# Commands:
> My legal question here
> feedback helpful
> stats
> help
> quit
""")

def main():
    """Run all demos"""
    print("🏛️  LEGAL AGENT SYSTEM - COMPREHENSIVE DEMO")
    print("=" * 60)
    print("This demo showcases all features of the Legal Agent System")
    
    try:
        demo_basic_queries()
        demo_data_integration()
        demo_feedback_system()
        demo_performance()
        demo_api_usage()
        
        print_header("DEMO COMPLETE")
        print("✅ All features demonstrated successfully!")
        print("\n🚀 Next Steps:")
        print("1. Run 'python comprehensive_test.py' for full testing")
        print("2. Use 'python cli_interface.py' for interactive queries")
        print("3. Start 'uvicorn main:app --reload' for web API")
        print("4. Check 'SETUP_GUIDE.md' for detailed instructions")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()
