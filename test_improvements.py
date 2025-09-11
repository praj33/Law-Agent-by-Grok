#!/usr/bin/env python3
"""
Test Script for Improved Legal Agent
====================================

This script tests the improvements made to domain classification
and legal sections coverage.
"""

import sys
import os

def test_improved_agent():
    """Test the improved legal agent"""
    
    print("🧪 TESTING IMPROVED LEGAL AGENT")
    print("=" * 60)
    
    try:
        from improved_final_legal_agent import create_improved_final_legal_agent
        agent = create_improved_final_legal_agent()
        print("✅ Improved agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize improved agent: {e}")
        return
    
    # Test queries that were problematic before
    test_cases = [
        {
            "query": "My phone was stolen from my bag",
            "expected_domain": "criminal_law",
            "description": "Physical theft case"
        },
        {
            "query": "Someone is hacking my phone",
            "expected_domain": "cyber_crime", 
            "description": "Cyber crime case"
        },
        {
            "query": "I was fired from my job",
            "expected_domain": "employment_law",
            "description": "Employment termination"
        },
        {
            "query": "My boss is not paying my salary",
            "expected_domain": "employment_law",
            "description": "Salary dispute"
        },
        {
            "query": "Employee disclosed company secrets",
            "expected_domain": "employment_law",
            "description": "Confidentiality breach"
        },
        {
            "query": "My husband beats me daily",
            "expected_domain": "family_law",
            "description": "Domestic violence"
        },
        {
            "query": "Landlord not returning deposit",
            "expected_domain": "tenant_rights",
            "description": "Security deposit issue"
        }
    ]
    
    print(f"\n🔍 Testing {len(test_cases)} problematic queries:")
    print("-" * 50)
    
    correct_classifications = 0
    total_sections_provided = 0
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected_domain = test_case["expected_domain"]
        description = test_case["description"]
        
        print(f"\n📋 Test {i}: {description}")
        print(f"   Query: \"{query}\"")
        print(f"   Expected Domain: {expected_domain}")
        
        try:
            response = agent.process_improved_legal_query(query)
            
            actual_domain = response["domain"]
            confidence = response["domain_confidence"]
            total_sections = response["total_sections"]
            
            is_correct = actual_domain == expected_domain
            if is_correct:
                correct_classifications += 1
            
            total_sections_provided += total_sections
            
            status = "✅" if is_correct else "❌"
            print(f"   {status} Actual Domain: {actual_domain} (confidence: {confidence:.3f})")
            print(f"   📚 Legal Sections: {total_sections} (BNS: {len(response['bns_sections'])}, IPC: {len(response['ipc_sections'])}, CrPC: {len(response['crpc_sections'])})")
            
            # Show system improvements
            improvements = response['system_capabilities']['total_improvements']
            print(f"   🎯 System Improvements: {improvements}/4")
            
        except Exception as e:
            print(f"   ❌ Error processing query: {e}")
    
    # Calculate results
    accuracy = correct_classifications / len(test_cases) * 100
    avg_sections = total_sections_provided / len(test_cases)
    
    print(f"\n📊 IMPROVEMENT TEST RESULTS:")
    print("=" * 50)
    print(f"✅ Domain Classification Accuracy: {accuracy:.1f}% ({correct_classifications}/{len(test_cases)})")
    print(f"📚 Average Sections per Query: {avg_sections:.1f}")
    print(f"🎯 Total Sections Provided: {total_sections_provided}")
    
    if accuracy >= 80:
        print(f"🎉 EXCELLENT! Domain classification significantly improved")
    elif accuracy >= 60:
        print(f"👍 GOOD! Domain classification improved")
    else:
        print(f"⚠️ NEEDS WORK! Domain classification needs further improvement")
    
    print(f"\n🔧 KEY IMPROVEMENTS MADE:")
    print("1. ✅ Enhanced domain classifier with better keyword matching")
    print("2. ✅ Context-aware classification (physical vs cyber crimes)")
    print("3. ✅ More BNS, IPC, and CrPC sections per query")
    print("4. ✅ Better subdomain classification")
    print("5. ✅ Comprehensive legal guidance")
    
    return accuracy, avg_sections


def test_enhanced_domain_classifier():
    """Test the enhanced domain classifier separately"""
    
    print(f"\n🧪 TESTING ENHANCED DOMAIN CLASSIFIER")
    print("=" * 50)
    
    try:
        from enhanced_domain_classifier import create_enhanced_domain_classifier
        classifier = create_enhanced_domain_classifier()
        print("✅ Enhanced domain classifier loaded")
    except Exception as e:
        print(f"❌ Enhanced classifier not available: {e}")
        return
    
    # Test specific problematic cases
    test_cases = [
        ("my phone was stolen from my bag", "criminal_law"),
        ("someone is hacking my phone", "cyber_crime"),
        ("I was fired from my job", "employment_law"),
        ("my boss is not paying salary", "employment_law"),
        ("employee disclosed company secrets", "employment_law"),
        ("my husband beats me daily", "family_law"),
        ("landlord not returning deposit", "tenant_rights"),
    ]
    
    correct = 0
    for query, expected in test_cases:
        domain, confidence, alternatives = classifier.classify_domain(query)
        is_correct = domain == expected
        if is_correct:
            correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} \"{query}\" → {domain} (expected: {expected}) [{confidence:.3f}]")
    
    accuracy = correct / len(test_cases) * 100
    print(f"\n📊 Enhanced Classifier Accuracy: {accuracy:.1f}% ({correct}/{len(test_cases)})")


def test_expanded_legal_database():
    """Test the expanded legal database"""
    
    print(f"\n🧪 TESTING EXPANDED LEGAL DATABASE")
    print("=" * 50)
    
    try:
        from expanded_legal_sections import create_expanded_legal_database
        db = create_expanded_legal_database()
        print("✅ Expanded legal database loaded")
    except Exception as e:
        print(f"❌ Expanded database not available: {e}")
        return
    
    stats = db.get_stats()
    print(f"📊 Database Statistics:")
    print(f"   BNS Sections: {stats['total_bns_sections']}")
    print(f"   IPC Sections: {stats['total_ipc_sections']}")
    print(f"   CrPC Sections: {stats['total_crpc_sections']}")
    print(f"   Total Sections: {stats['total_sections']}")
    
    # Test section retrieval
    test_queries = [
        ("criminal_law", "theft", "My phone was stolen"),
        ("cyber_crime", "hacking", "Someone hacked my computer"),
        ("employment_law", "termination", "I was fired"),
    ]
    
    print(f"\n📚 Testing Section Retrieval:")
    for domain, subdomain, query in test_queries:
        sections = db.get_comprehensive_sections_for_query(domain, subdomain, query)
        total = len(sections['bns_sections']) + len(sections['ipc_sections']) + len(sections['crpc_sections'])
        print(f"   {query}: {total} sections (BNS: {len(sections['bns_sections'])}, IPC: {len(sections['ipc_sections'])}, CrPC: {len(sections['crpc_sections'])})")


if __name__ == "__main__":
    print("🚀 COMPREHENSIVE IMPROVEMENT TESTING")
    print("=" * 70)
    
    # Test 1: Enhanced Domain Classifier
    test_enhanced_domain_classifier()
    
    # Test 2: Expanded Legal Database
    test_expanded_legal_database()
    
    # Test 3: Complete Improved Agent
    accuracy, avg_sections = test_improved_agent()
    
    print(f"\n🎯 OVERALL IMPROVEMENT SUMMARY:")
    print("=" * 50)
    print(f"✅ Domain Classification: {accuracy:.1f}% accuracy")
    print(f"📚 Legal Coverage: {avg_sections:.1f} sections per query")
    print(f"🔧 System Enhancements: Multiple improvements implemented")
    
    if accuracy >= 80 and avg_sections >= 15:
        print(f"\n🎉 EXCELLENT! All improvements working successfully")
        print(f"🚀 System ready for production with enhanced capabilities")
    else:
        print(f"\n⚠️ Some improvements may need fine-tuning")
    
    print(f"\n✅ Testing completed!")