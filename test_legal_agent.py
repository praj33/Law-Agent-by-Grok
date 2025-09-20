#!/usr/bin/env python3
"""
Test script for Legal Agent system
Tests if the system provides proper answers with constitutional articles and process steps
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_working_enhanced_agent():
    """Test the working enhanced agent"""
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        print("🧪 TESTING WORKING ENHANCED LEGAL AGENT")
        print("=" * 60)
        
        # Create agent
        agent = create_working_enhanced_agent()
        
        # Test query about tenant rights
        test_query = "My landlord is not returning my security deposit of Rs 25000 and is asking me to vacate without proper notice"
        
        print(f"Query: {test_query}")
        print("=" * 60)
        
        # Process the query
        response = agent.process_query(test_query)
        
        # Display comprehensive response
        print(f"📋 DOMAIN: {response.domain.replace('_', ' ').title()}")
        print(f"🎯 CONFIDENCE: {response.confidence:.3f}")
        print(f"📝 LEGAL ROUTE: {response.legal_route}")
        print(f"⏱️ TIMELINE: {response.timeline}")
        print(f"📊 SUCCESS RATE: {response.success_rate:.1%}")
        
        # Process steps
        if hasattr(response, 'process_steps') and response.process_steps:
            print(f"\n📋 DETAILED PROCESS STEPS:")
            for i, step in enumerate(response.process_steps, 1):
                print(f"   {i}. {step}")
        
        # Constitutional backing - RESTORED with enhanced display
        if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
            print(f"\n🏛️ CONSTITUTIONAL BACKING:")
            print(f"   {response.constitutional_backing}")
        
        print(f"\n⚡ RESPONSE TIME: {response.response_time:.2f} seconds")
        print(f"🔗 SESSION ID: {response.session_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing working enhanced agent: {e}")
        traceback.print_exc()
        return False

def test_enhanced_legal_agent():
    """Test the enhanced legal agent"""
    try:
        from enhanced_legal_agent import create_enhanced_legal_agent
        
        print("\n🧪 TESTING ENHANCED LEGAL AGENT")
        print("=" * 60)
        
        # Create agent
        agent = create_enhanced_legal_agent()
        
        # Test query about elder abuse
        test_query = "My elderly father is being financially exploited by his caregiver in Delhi"
        
        print(f"Query: {test_query}")
        print("=" * 60)
        
        # Process the query
        response = agent.process_enhanced_query(test_query)
        
        # Display comprehensive response
        print(f"📋 DOMAIN: {response.domain.replace('_', ' ').title()}")
        print(f"🎯 CONFIDENCE: {response.confidence:.3f}")
        print(f"📝 LEGAL ROUTE: {response.legal_route}")
        print(f"⏱️ TIMELINE: {response.timeline_range[0]}-{response.timeline_range[1]} days")
        print(f"💰 ESTIMATED COST: Rs {response.estimated_cost[0]:,}-{response.estimated_cost[1]:,}")
        print(f"📊 SUCCESS RATE: {response.success_rate:.1%}")
        print(f"🏛️ JURISDICTION: {response.jurisdiction}")
        
        # Constitutional backing - RESTORED with enhanced article details
        if response.constitutional_backing:
            print(f"\n🏛️ CONSTITUTIONAL BACKING:")
            print(f"   {response.constitutional_backing}")
            
            if response.constitutional_articles:
                print(f"\n📜 RELEVANT CONSTITUTIONAL ARTICLES:")
                for article in response.constitutional_articles:
                    article_num = article.get('article_number', 'N/A')
                    title = article.get('title', 'N/A')
                    confidence = article.get('confidence_percentage')
                    
                    if confidence:
                        if confidence >= 70:
                            conf_icon = "🟢"  # Green
                        elif confidence >= 40:
                            conf_icon = "🟡"  # Yellow  
                        else:
                            conf_icon = "🔴"  # Red
                        print(f"   {conf_icon} Article {article_num}: {title} ({confidence}% confidence)")
                    else:
                        print(f"   • Article {article_num}: {title}")
                    
                    if article.get('summary'):
                        summary = article['summary'][:150] + "..." if len(article.get('summary', '')) > 150 else article.get('summary')
                        print(f"     Summary: {summary}")
        
        # Process steps
        if response.process_steps:
            print(f"\n📋 DETAILED PROCESS STEPS:")
            for step in response.process_steps:
                print(f"   Step {step['step_number']}: {step['title']}")
                print(f"   Description: {step['description']}")
                if "estimated_duration" in step:
                    print(f"   Duration: {step['estimated_duration']}")
                if "required_documents" in step:
                    print(f"   Documents: {', '.join(step['required_documents'])}")
                print()
        
        # Required documents
        if response.required_documents:
            print(f"📄 REQUIRED DOCUMENTS:")
            for doc in response.required_documents:
                print(f"   • {doc}")
        
        # Crime data insights
        if response.crime_data_advice:
            print(f"\n🚨 CRIME DATA INSIGHTS:")
            print(f"   {response.crime_data_advice}")
            if response.risk_assessment:
                print(f"   Risk Level: {response.risk_assessment}")
        
        # Jargon detection
        if response.detected_jargon:
            print(f"\n📚 LEGAL TERMS EXPLAINED:")
            for term in response.detected_jargon:
                if term in response.glossary_definitions:
                    print(f"   • {term}: {response.glossary_definitions[term]}")
        
        print(f"\n⚡ RESPONSE TIME: {response.response_time:.2f} seconds")
        print(f"🔗 SESSION ID: {response.session_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhanced legal agent: {e}")
        traceback.print_exc()
        return False

def test_cli_interface():
    """Test the CLI interface"""
    try:
        from legal_agent import create_legal_agent
        
        print("\n🧪 TESTING BASIC LEGAL AGENT")
        print("=" * 60)
        
        # Create agent
        agent = create_legal_agent()
        
        # Test query about employment law
        test_query = "My boss is sexually harassing me at workplace and not paying my salary"
        
        print(f"Query: {test_query}")
        print("=" * 60)
        
        # Process the query
        from legal_agent import LegalQueryInput
        query_input = LegalQueryInput(user_input=test_query)
        response = agent.process_query(query_input)
        
        # Display response
        print(f"📋 DOMAIN: {response.domain}")
        print(f"🎯 CONFIDENCE: {response.confidence:.3f}")
        print(f"📝 LEGAL ROUTE: {response.legal_route}")
        print(f"⏱️ TIMELINE: {response.timeline}")
        print(f"📊 OUTCOME: {response.outcome}")
        
        # Process steps
        if hasattr(response, 'process_steps') and response.process_steps:
            print(f"\n📋 PROCESS STEPS:")
            print(f"   {response.process_steps}")
        
        # Glossary
        if hasattr(response, 'glossary') and response.glossary:
            print(f"\n📚 LEGAL TERMS:")
            for term, definition in response.glossary.items():
                print(f"   • {term}: {definition}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing basic legal agent: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🏛️ LEGAL AGENT SYSTEM TESTING")
    print("=" * 70)
    
    results = []
    
    # Test 1: Working Enhanced Agent
    results.append(test_working_enhanced_agent())
    
    # Test 2: Enhanced Legal Agent
    results.append(test_enhanced_legal_agent())
    
    # Test 3: Basic Legal Agent
    results.append(test_cli_interface())
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    successful_tests = sum(results)
    total_tests = len(results)
    
    print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
    print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Legal Agent system is working properly.")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)