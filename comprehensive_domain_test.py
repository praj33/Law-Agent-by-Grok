#!/usr/bin/env python3
"""
Comprehensive test to verify domain and subdomain classification for various legal queries
"""

from enhanced_legal_agent import create_enhanced_legal_agent
from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent

def test_comprehensive_classification():
    """Test domain and subdomain classification for various legal queries"""
    
    # Create agents
    legal_agent = create_enhanced_legal_agent()
    subdomain_agent = create_enhanced_subdomain_bns_agent()
    
    # Test cases with expected domains and subdomains
    test_cases = [
        # Criminal Law cases
        ("My 5-year-old daughter was kidnapped for ransom", "criminal_law", "kidnapping"),
        ("Someone stole my phone from my bag", "criminal_law", "theft"),
        ("I was raped by my neighbor", "criminal_law", "rape"),
        ("My house was burglarized and jewelry stolen", "criminal_law", "theft"),
        
        # Family Law cases
        ("I want to file for divorce from my spouse", "family_law", "divorce"),
        ("My ex-husband is not paying child support", "family_law", "child_support"),
        ("I'm experiencing domestic violence from my partner", "family_law", "domestic_violence"),
        
        # Employment Law cases
        ("My boss is not paying my salary for 3 months", "employment_law", "wage_issues"),
        ("I was fired unfairly from my job", "employment_law", "wrongful_termination"),
        ("My colleague is sexually harassing me at work", "employment_law", "workplace_harassment"),
        
        # Tenant Rights cases
        ("My landlord won't return my security deposit", "tenant_rights", "security_deposit"),
        ("Landlord is trying to evict me without proper notice", "tenant_rights", "eviction"),
        
        # Consumer Complaint cases
        ("I bought a defective phone and want refund", "consumer_complaint", "defective_products"),
        ("The restaurant served contaminated food and I got sick", "consumer_complaint", "food_safety"),
        
        # Personal Injury cases
        ("I was injured in a car accident and need compensation", "personal_injury", "motor_vehicle"),
        ("I slipped and fell at a shopping mall", "personal_injury", "slip_and_fall"),
        
        # Cyber Crime cases
        ("My phone is being hacked by someone", "cyber_crime", "computer_crimes"),
        ("Someone stole my identity online", "cyber_crime", "identity_theft"),
        
        # Immigration Law cases
        ("My visa application was denied", "immigration_law", "visa_issues"),
        ("I need to renew my passport", "immigration_law", "passport_issues"),
        
        # Contract Dispute cases
        ("The contractor didn't complete work as specified", "contract_dispute", "construction"),
        ("Business partner breached our agreement", "contract_dispute", "breach_of_contract"),
        
        # Elder Abuse cases
        ("My elderly father is being abused in nursing home", "elder_abuse", "institutional_abuse"),
    ]
    
    print("Comprehensive Domain and Subdomain Classification Test")
    print("=" * 65)
    print()
    
    correct_domain = 0
    correct_subdomain = 0
    total_tests = len(test_cases)
    
    for i, (query, expected_domain, expected_subdomain) in enumerate(test_cases, 1):
        print(f"Test {i:2d}: \"{query}\"")
        
        # Test domain classification
        domain, confidence, alternatives = legal_agent.ml_classifier.classify_with_confidence(query)
        
        # Test subdomain classification using the subdomain classifier directly
        subdomain, subdomain_confidence, subdomain_alternatives = subdomain_agent.subdomain_classifier.classify_subdomain(domain, query)
        
        # Check results
        domain_correct = domain == expected_domain
        subdomain_correct = subdomain == expected_subdomain
        
        if domain_correct:
            correct_domain += 1
            domain_status = "✅"
        else:
            domain_status = "❌"
            
        if subdomain_correct:
            correct_subdomain += 1
            subdomain_status = "✅"
        else:
            subdomain_status = "❌"
        
        print(f"         Domain: {domain} (expected: {expected_domain}) {domain_status}")
        print(f"         Subdomain: {subdomain} (expected: {expected_subdomain}) {subdomain_status}")
        print(f"         Confidence: Domain={confidence:.3f}, Subdomain={subdomain_confidence:.3f}")
        if not domain_correct or not subdomain_correct:
            print(f"         Alternatives: {alternatives[:3] if alternatives else []}")
        print()
    
    # Summary
    domain_accuracy = (correct_domain / total_tests) * 100
    subdomain_accuracy = (correct_subdomain / total_tests) * 100
    
    print("Summary")
    print("-" * 20)
    print(f"Domain Classification Accuracy: {correct_domain}/{total_tests} ({domain_accuracy:.1f}%)")
    print(f"Subdomain Classification Accuracy: {correct_subdomain}/{total_tests} ({subdomain_accuracy:.1f}%)")
    
    if domain_accuracy == 100 and subdomain_accuracy == 100:
        print("\n🎉 All tests passed! Domain and subdomain classification is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Review the incorrect classifications above.")

if __name__ == "__main__":
    test_comprehensive_classification()