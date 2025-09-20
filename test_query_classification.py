#!/usr/bin/env python3
"""
Test Script for Query Classification System
==========================================

This script tests the query classification system with the example query
from the user requirements to ensure all components are working correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_classification_system import create_query_classification_system, format_classification_result


def test_example_query():
    """Test the example query from user requirements"""
    print("🔍 Testing Query Classification System")
    print("=" * 50)
    
    # Create the classification system
    system = create_query_classification_system()
    
    # Test with the example query from user requirements
    test_query = "My child was kidnapped for ransom"
    
    print(f"Testing query: '{test_query}'")
    print("-" * 50)
    
    # Classify the query
    result = system.classify_query(test_query)
    
    # Display the result
    print("CLASSIFICATION RESULT:")
    print("-" * 30)
    print(f"Domain: {result.domain}")
    print(f"Subdomain: {result.subdomain}")
    print(f"Confidence: {result.confidence_percentage}%")
    
    print("\nCONSTITUTIONAL ARTICLES:")
    print("-" * 30)
    if result.constitutional_articles:
        for article in result.constitutional_articles:
            print(f"Article {article.get('article_number', 'N/A')}: {article.get('title', 'N/A')}")
            print(f"  Confidence: {article.get('confidence_percentage', 0)}%")
    else:
        print("No constitutional articles found")
    
    print("\nLEGAL SECTIONS:")
    print("-" * 30)
    print(f"BNS Sections: {len(result.bns_sections)}")
    print(f"IPC Sections: {len(result.ipc_sections)}")
    print(f"CrPC Sections: {len(result.crpc_sections)}")
    
    print("\nLEGAL PROCESS:")
    print("-" * 30)
    for i, step in enumerate(result.legal_process, 1):
        print(f"{i}. {step}")
    
    print("\nNOTES & SAFEGUARDS:")
    print("-" * 30)
    for note in result.notes_and_safeguards:
        print(f"• {note}")
    
    print("\nEMERGENCY CONTACTS:")
    print("-" * 30)
    for contact in result.emergency_contacts:
        print(f"• {contact}")
    
    # Test the formatted output
    print("\n" + "=" * 50)
    print("FULL FORMATTED OUTPUT:")
    print("=" * 50)
    formatted_output = format_classification_result(result)
    print(formatted_output)
    
    # Test system stats
    print("\n" + "=" * 50)
    print("SYSTEM STATISTICS:")
    print("=" * 50)
    stats = system.get_system_stats()
    print(f"Queries Processed: {stats.get('queries_processed', 'N/A')}")
    print(f"Legal Sections: {stats.get('legal_database_stats', {}).get('total_sections', 'N/A')}")
    print(f"Domains: {stats.get('subdomain_classifier_stats', {}).get('total_domains', 'N/A')}")
    print(f"Subdomains: {stats.get('subdomain_classifier_stats', {}).get('total_subdomains', 'N/A')}")
    
    print("\n✅ Test completed successfully!")


if __name__ == "__main__":
    test_example_query()