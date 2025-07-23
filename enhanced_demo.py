"""
Enhanced Legal Agent Demo - Multi-Dataset Integration
====================================================

This demo showcases the Legal Agent with enhanced data integration using:
- crime_data.json: Senior citizen crimes (2020-2022)
- INSERT2_fixed.json: General IPC crimes and population data (2020-2022)
- INSERT3_fixed.json: Senior citizen crimes (2019-2021) and other categories

Usage: python enhanced_demo.py
"""

from adaptive_legal_agent import create_adaptive_legal_agent, LegalQueryInput
from enhanced_data_integration import create_enhanced_legal_system
import json

def print_header(title):
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70)

def print_subheader(title):
    print(f"\n📋 {title}")
    print("-" * 50)

def demo_enhanced_data_integration():
    """Demo enhanced data integration with multiple datasets"""
    print_header("ENHANCED DATA INTEGRATION - MULTI-DATASET ANALYSIS")
    
    # Create enhanced analyzer
    analyzer = create_enhanced_legal_system()
    
    print_subheader("Dataset Coverage Analysis")
    trends = analyzer.analyze_enhanced_crime_trends()
    
    print(f"📊 Data Coverage:")
    print(f"   States with Senior Citizen Data: {trends['data_coverage']['states_with_senior_data']}")
    print(f"   States with IPC Crime Data: {trends['data_coverage']['states_with_ipc_data']}")
    print(f"   States with Population Data: {trends['data_coverage']['states_with_population_data']}")
    
    print(f"\n📈 Crime Trends (2019-2022):")
    if trends['senior_citizen_crimes']['2019']:
        print(f"   2019: {trends['senior_citizen_crimes']['2019']:,} senior citizen crimes")
    print(f"   2020: {trends['senior_citizen_crimes']['2020']:,} senior citizen crimes")
    print(f"   2021: {trends['senior_citizen_crimes']['2021']:,} senior citizen crimes")
    print(f"   2022: {trends['senior_citizen_crimes']['2022']:,} senior citizen crimes")
    print(f"   Overall Trend: {trends['senior_crime_trend'].title()}")
    
    print_subheader("High-Risk States Analysis")
    high_risk_states = analyzer.get_enhanced_high_risk_states(50.0)
    
    print("🚨 Top 5 High-Risk States for Senior Citizen Crimes:")
    for i, state in enumerate(high_risk_states[:5], 1):
        rate = state.senior_crime_rate_2022 or state.senior_crime_rate_2021
        trend = state.senior_crime_trend_2019_2022
        print(f"   {i}. {state.state_ut}: {rate} per lakh (Trend: {trend})")
    
    print_subheader("Location-Specific Enhanced Analysis")
    
    # Test multiple locations
    test_locations = ["Delhi", "Maharashtra", "Assam", "Tamil Nadu", "Uttar Pradesh"]
    
    for location in test_locations:
        advice = analyzer.get_comprehensive_location_advice(location, "senior_citizen_abuse")
        if advice['location_found']:
            print(f"\n🌍 {location}:")
            print(f"   Risk Level: {advice['risk_level'].replace('_', ' ').title()}")
            print(f"   Crime Rate 2022: {advice['senior_crime_rate_2022']} per lakh")
            print(f"   Crime Trend: {advice['senior_crime_trend'].replace('_', ' ').title()}")
            
            # Show enhanced statistics if available
            enhanced_stats = advice['enhanced_statistics']
            if enhanced_stats['senior_crimes_2019']:
                print(f"   Historical Data: {enhanced_stats['senior_crimes_2019']} (2019) → {enhanced_stats['senior_crimes_2022']} (2022)")

def demo_enhanced_legal_agent():
    """Demo the legal agent with enhanced data integration"""
    print_header("ENHANCED LEGAL AGENT WITH MULTI-DATASET INTEGRATION")
    
    # Create adaptive agent with enhanced data
    agent = create_adaptive_legal_agent()
    
    # Test queries that will trigger enhanced data integration
    test_queries = [
        {
            "query": "My 80-year-old grandmother is being abused in Delhi nursing home",
            "expected": "Elder abuse with Delhi high-risk analysis"
        },
        {
            "query": "Senior citizen financial fraud case in Maharashtra",
            "expected": "Elder abuse with Maharashtra crime statistics"
        },
        {
            "query": "Elderly harassment complaint in Assam",
            "expected": "Elder abuse with Assam low-risk analysis"
        },
        {
            "query": "My grandfather is being neglected in Tamil Nadu old age home",
            "expected": "Elder abuse with Tamil Nadu data"
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        print_subheader(f"Enhanced Query {i}: {test_case['query']}")
        
        query = LegalQueryInput(user_input=test_case['query'])
        response = agent.process_query_with_learning(query)
        
        print(f"🏛️  Domain: {response.domain.title()}")
        print(f"🎯 Confidence: {response.confidence:.3f}")
        print(f"⏱️  Timeline: {response.timeline}")
        
        if response.data_driven_advice:
            print(f"📊 Enhanced Data-Driven Advice:")
            print(f"   Risk Level: {response.risk_assessment}")
            print(f"   Advice: {response.data_driven_advice[:150]}...")
        
        if response.location_insights and response.location_insights.get('enhanced_statistics'):
            stats = response.location_insights['enhanced_statistics']
            print(f"📈 Enhanced Statistics Available:")
            if stats['senior_crimes_2019']:
                print(f"   Senior Crimes 2019-2022: {stats['senior_crimes_2019']} → {stats['senior_crimes_2022']}")
            if stats['total_population_2022_lakhs']:
                print(f"   Population 2022: {stats['total_population_2022_lakhs']} lakhs")

def demo_comparison_basic_vs_enhanced():
    """Compare basic vs enhanced data integration"""
    print_header("COMPARISON: BASIC vs ENHANCED DATA INTEGRATION")
    
    # Import basic data integration
    try:
        from data_integration import CrimeDataAnalyzer
        basic_analyzer = CrimeDataAnalyzer()
        basic_available = True
    except:
        basic_available = False
    
    # Enhanced data integration
    enhanced_analyzer = create_enhanced_legal_system()
    
    test_location = "Delhi"
    
    print_subheader(f"Analysis for {test_location}")
    
    if basic_available:
        print("🔵 Basic Data Integration:")
        basic_advice = basic_analyzer.get_location_based_advice(test_location, "senior_citizen_abuse")
        if basic_advice['location_found']:
            print(f"   Risk Level: {basic_advice['risk_level']}")
            print(f"   Crime Rate: {basic_advice['crime_rate_2022']}")
            print(f"   Data Points: Limited to 2020-2022 senior citizen crimes")
    
    print("\n🟢 Enhanced Data Integration:")
    enhanced_advice = enhanced_analyzer.get_comprehensive_location_advice(test_location, "senior_citizen_abuse")
    if enhanced_advice['location_found']:
        print(f"   Risk Level: {enhanced_advice['risk_level']}")
        print(f"   Crime Rate 2022: {enhanced_advice['senior_crime_rate_2022']}")
        print(f"   Crime Rate 2021: {enhanced_advice['senior_crime_rate_2021']}")
        print(f"   Crime Trend: {enhanced_advice['senior_crime_trend']}")
        
        stats = enhanced_advice['enhanced_statistics']
        data_points = []
        if stats['senior_crimes_2019']: data_points.append("2019-2022 senior crimes")
        if stats['ipc_crimes_2022']: data_points.append("IPC crimes")
        if stats['total_population_2022_lakhs']: data_points.append("population data")
        
        print(f"   Data Points: {', '.join(data_points) if data_points else 'Senior citizen crimes only'}")
    
    print(f"\n✅ Enhanced Integration Benefits:")
    print(f"   • Historical trend analysis (2019-2022)")
    print(f"   • Multiple crime categories")
    print(f"   • Population context")
    print(f"   • Cross-dataset correlation")

def demo_real_world_scenarios():
    """Demo real-world scenarios with enhanced data"""
    print_header("REAL-WORLD SCENARIOS WITH ENHANCED DATA")
    
    agent = create_adaptive_legal_agent()
    
    scenarios = [
        {
            "title": "Elder Abuse in High-Risk Area",
            "query": "My 75-year-old father in Delhi is being financially exploited by nursing home staff",
            "expectation": "High-risk warning with Delhi crime statistics"
        },
        {
            "title": "Elder Safety in Low-Risk Area", 
            "query": "Concerned about elderly mother's safety in Assam",
            "expectation": "Reassuring advice with low crime rate data"
        },
        {
            "title": "Comparative Analysis Query",
            "query": "Is it safer for elderly people in Tamil Nadu compared to Maharashtra?",
            "expectation": "Comparative crime statistics and advice"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print_subheader(f"Scenario {i}: {scenario['title']}")
        print(f"Query: {scenario['query']}")
        print(f"Expected: {scenario['expectation']}")
        
        query = LegalQueryInput(user_input=scenario['query'])
        response = agent.process_query_with_learning(query)
        
        print(f"\n🎯 Agent Response:")
        print(f"   Domain: {response.domain}")
        print(f"   Confidence: {response.confidence:.3f}")
        
        if response.data_driven_advice:
            print(f"   Enhanced Advice: {response.data_driven_advice[:100]}...")
            print(f"   Risk Assessment: {response.risk_assessment}")

def main():
    """Run all enhanced demos"""
    print("🚀 ENHANCED LEGAL AGENT DEMONSTRATION")
    print("Multi-Dataset Integration with crime_data.json, INSERT2.json, INSERT3.json")
    print("=" * 80)
    
    try:
        # Demo 1: Enhanced data integration
        demo_enhanced_data_integration()
        
        # Demo 2: Enhanced legal agent
        demo_enhanced_legal_agent()
        
        # Demo 3: Comparison
        demo_comparison_basic_vs_enhanced()
        
        # Demo 4: Real-world scenarios
        demo_real_world_scenarios()
        
        print_header("ENHANCED DEMO COMPLETE")
        print("✅ All enhanced features demonstrated successfully!")
        print("\n🎯 Key Enhancements Shown:")
        print("• ✅ Multi-dataset integration (3 JSON files)")
        print("• ✅ Historical crime trend analysis (2019-2022)")
        print("• ✅ Enhanced location-based insights")
        print("• ✅ Cross-dataset correlation analysis")
        print("• ✅ Comprehensive risk assessment")
        print("• ✅ Population context integration")
        
        print("\n📁 Files Integrated:")
        print("• crime_data.json - Senior citizen crimes (2020-2022)")
        print("• INSERT2_fixed.json - IPC crimes & population (2020-2022)")
        print("• INSERT3_fixed.json - Senior citizen crimes (2019-2021)")
        
        print("\n🚀 Your Enhanced Legal Agent is Ready!")
        print("Use: python cli_interface.py (now with enhanced data)")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your setup and data files.")

if __name__ == "__main__":
    main()
