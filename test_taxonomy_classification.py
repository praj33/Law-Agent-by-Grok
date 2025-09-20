#!/usr/bin/env python3
"""
Test Taxonomy Classification
============================

Test the legal query classification according to the provided taxonomy.
"""

import sys
import os

# Add the parent directory to the path so we can import the agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ultimate_legal_agent import create_ultimate_legal_agent


def test_taxonomy_classification():
    """Test that queries are correctly classified according to the taxonomy"""
    
    # Create the agent
    agent = create_ultimate_legal_agent()
    
    # Test cases for each domain and subdomain in the taxonomy
    test_cases = [
        # Criminal Law
        ("Someone murdered my brother", "Criminal Law", "Murder"),
        ("My child was kidnapped for ransom", "Criminal Law", "Kidnapping / Abduction"),
        ("I was raped by my neighbor", "Criminal Law", "Sexual Offences"),
        ("Caught with drugs at airport", "Criminal Law", "Drug Crime"),
        ("Business partner embezzled funds", "Criminal Law", "Financial Crime"),
        ("Hackers stole money from my bank account", "Criminal Law", "Cyber Crime"),
        
        # Family Law
        ("My husband beats me daily", "Family Law", "Domestic Violence"),
        ("I want to file for divorce", "Family Law", "Marriage & Divorce"),
        ("Fighting for child custody", "Family Law", "Child Custody & Maintenance"),
        
        # Property & Land Law
        ("Landlord won't return security deposit", "Property & Land Law", "Tenant Rights"),
        ("Property dispute with neighbor", "Property & Land Law", "Real Estate & Land Disputes"),
        
        # Traffic & Motor Vehicle Law
        ("Car accident with injuries", "Traffic & Motor Vehicle Law", "Road Accidents"),
        ("Drink and drive incident", "Traffic & Motor Vehicle Law", "Drunk Driving"),
        
        # Employment & Labor Law
        ("My boss is not paying my salary", "Employment & Labor Law", "Employment Issues"),
        ("Workplace sexual harassment", "Employment & Labor Law", "Workplace Harassment"),
        
        # Consumer Law
        ("Company sold defective product", "Consumer Law", "Consumer Protection"),
        ("Doctor's negligence caused harm", "Consumer Law", "Medical Malpractice"),
        
        # Social Offences
        ("Black magic practitioner harmed family", "Social Offences", "Superstition & Black Magic"),
        
        # Edge cases
        ("Airport drug possession case", "Criminal Law", "Drug Crime"),
        ("Sexual assault at workplace", "Criminal Law", "Sexual Offences"),
        ("Wrong treatment at hospital", "Consumer Law", "Medical Malpractice"),
    ]
    
    print("🧪 Testing Taxonomy Classification")
    print("=" * 50)
    
    correct_classifications = 0
    total_tests = len(test_cases)
    
    for query, expected_domain, expected_subdomain in test_cases:
        # Classify the query according to taxonomy
        domain, subdomain, confidence = agent.classify_query_according_to_taxonomy(query)
        
        # Check if classification is correct
        is_correct = (domain == expected_domain and subdomain == expected_subdomain)
        if is_correct:
            correct_classifications += 1
            
        status = "✅" if is_correct else "❌"
        print(f"{status} Query: '{query}'")
        print(f"   Expected: {expected_domain} → {expected_subdomain}")
        print(f"   Got:      {domain} → {subdomain} (confidence: {confidence:.3f})")
        print()
    
    accuracy = correct_classifications / total_tests * 100
    print(f"📊 Accuracy: {accuracy:.1f}% ({correct_classifications}/{total_tests})")
    
    if accuracy >= 80:
        print("🎉 Good! Taxonomy classification is working well.")
        return True
    else:
        print("⚠️  Classification needs improvement.")
        return False


if __name__ == "__main__":
    success = test_taxonomy_classification()
    if success:
        print("\n✅ Taxonomy classification test passed!")
    else:
        print("\n❌ Taxonomy classification test failed!")
        sys.exit(1)