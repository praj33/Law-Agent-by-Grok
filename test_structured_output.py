#!/usr/bin/env python3
"""
Test Structured Output Format
============================

This script demonstrates the new structured step-by-step output format
for the adaptive legal agent as requested by the user.
"""

from adaptive_agent import create_adaptive_agent
from legal_agent import LegalQueryInput


def test_structured_output():
    """Test the structured output format with different legal queries"""
    
    print("🏛️ TESTING STRUCTURED OUTPUT FORMAT")
    print("=" * 60)
    
    # Create adaptive agent
    agent = create_adaptive_agent()
    
    # Test queries for different domains
    test_queries = [
        "my phone is being hacked",
        "my landlord is not returning my security deposit", 
        "my employer is not paying overtime wages",
        "someone is threatening me online"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: {query}")
        print("=" * 60)
        
        # Create query input
        query_input = LegalQueryInput(user_input=query)
        
        try:
            # Get structured output
            structured_response = agent.process_query_with_structured_output(query_input)
            
            # Display the structured response
            print(structured_response)
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        print("\n" + "=" * 60)


def test_single_query():
    """Test a single query with the structured format"""
    
    print("🏛️ SINGLE QUERY TEST - STRUCTURED FORMAT")
    print("=" * 60)
    
    # Create adaptive agent
    agent = create_adaptive_agent()
    
    # Test with the example query from user's request
    query = "phone being hacked"
    
    print(f"Testing query: '{query}'")
    print("-" * 40)
    
    # Create query input
    query_input = LegalQueryInput(user_input=query)
    
    try:
        # Get structured output
        structured_response = agent.process_query_with_structured_output(query_input)
        
        # Display the structured response
        print(structured_response)
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")


if __name__ == "__main__":
    # Test single query first
    test_single_query()
    
    print("\n\n" + "🔄" * 20)
    print("MULTIPLE QUERIES TEST")
    print("🔄" * 20 + "\n")
    
    # Test multiple queries
    test_structured_output()