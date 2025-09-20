#!/usr/bin/env python3
"""
Verification test to ensure all queries are classified under their correct domains
"""

from enhanced_legal_agent import create_enhanced_legal_agent

def test_domain_classifications():
    """Test that all queries are classified under their correct domains"""
    
    # Create agent
    legal_agent = create_enhanced_legal_agent()
    
    # Test cases with queries and their expected domains
    test_cases = [
        # Criminal Law cases
        ("My 5-year-old daughter was kidnapped for ransom", "criminal_law"),
        ("Someone stole my phone from my bag", "criminal_law"),
        ("I was raped by my neighbor", "criminal_law"),
        ("My house was burglarized and jewelry stolen", "criminal_law"),
        ("Someone is hacking my computer", "criminal_law"),
        
        # Family Law cases
        ("I want to file for divorce from my spouse", "family_law"),
        ("My ex-husband is not paying child support", "family_law"),
        ("I'm experiencing domestic violence from my partner", "family_law"),
        ("I need custody of my children", "family_law"),
        
        # Employment Law cases
        ("My boss is not paying my salary for 3 months", "employment_law"),
        ("I was fired unfairly from my job", "employment_law"),
        ("My colleague is sexually harassing me at work", "employment_law"),
        
        # Tenant Rights cases
        ("My landlord won't return my security deposit", "tenant_rights"),
        ("Landlord is trying to evict me without proper notice", "tenant_rights"),
        
        # Consumer Complaint cases
        ("I bought a defective phone and want refund", "consumer_complaint"),
        ("The restaurant served contaminated food and I got sick", "consumer_complaint"),
        
        # Personal Injury cases
        ("I was injured in a car accident and need compensation", "personal_injury"),
        ("I slipped and fell at a shopping mall", "personal_injury"),
        
        # Cyber Crime cases
        ("My phone is being hacked by someone", "cyber_crime"),
        ("Someone stole my identity online", "cyber_crime"),
        
        # Immigration Law cases
        ("My visa application was denied", "immigration_law"),
        ("I need to renew my passport", "immigration_law"),
        
        # Contract Dispute cases
        ("The contractor didn't complete work as specified", "contract_dispute"),
        ("Business partner breached our agreement", "contract_dispute"),
        
        # Elder Abuse cases
        ("My elderly father is being abused in nursing home", "elder_abuse"),
    ]
    
    print("Domain Classification Verification Test")
    print("=" * 50)
    print()
    
    correct_domain = 0
    total_tests = len(test_cases)
    
    for i, (query, expected_domain) in enumerate(test_cases, 1):
        print(f"Test {i:2d}: \"{query}\"")
        
        # Test domain classification
        domain, confidence, alternatives = legal_agent.ml_classifier.classify_with_confidence(query)
        
        # Check results
        domain_correct = domain == expected_domain
        
        if domain_correct:
            correct_domain += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"         Domain: {domain} (expected: {expected_domain}) {status}")
        print(f"         Confidence: {confidence:.3f}")
        if not domain_correct:
            print(f"         Alternatives: {alternatives[:3] if alternatives else []}")
        print()
    
    # Summary
    domain_accuracy = (correct_domain / total_tests) * 100
    
    print("Summary")
    print("-" * 20)
    print(f"Domain Classification Accuracy: {correct_domain}/{total_tests} ({domain_accuracy:.1f}%)")
    
    if domain_accuracy == 100:
        print("\n🎉 All domain classifications are correct!")
    else:
        print(f"\n⚠️  Some domain classifications are incorrect. Review the failed tests above.")

if __name__ == "__main__":
    test_domain_classifications()