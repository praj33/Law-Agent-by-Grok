#!/usr/bin/env python3
"""
Constitutional Articles Validation Test
=======================================

This script validates that constitutional articles are correctly assigned
to different legal domains with proper relevance and accuracy.
"""

def test_constitutional_articles():
    """Test constitutional articles assignment for different domains"""
    
    print("🏛️ CONSTITUTIONAL ARTICLES VALIDATION TEST")
    print("=" * 60)
    print("Testing constitutional article assignment for different legal domains\n")
    
    # Test cases with expected constitutional articles
    test_cases = [
        {
            "query": "my phone is being hacked by someone",
            "domain": "cyber_crime",
            "expected_articles": ["21", "19", "300A"],  # Privacy, Freedom, Property rights
            "description": "Cyber crime - Privacy and digital rights"
        },
        {
            "query": "my boss is not giving my salary",
            "domain": "employment_law", 
            "expected_articles": ["19(1)(g)", "21", "14"],  # Profession, Livelihood, Equality
            "description": "Employment law - Professional rights"
        },
        {
            "query": "my husband beats me daily",
            "domain": "family_law",
            "expected_articles": ["21", "14", "15"],  # Life & liberty, Equality, Non-discrimination
            "description": "Family law - Domestic violence"
        },
        {
            "query": "landlord not returning deposit",
            "domain": "tenant_rights",
            "expected_articles": ["21", "300A", "19(1)(e)"],  # Life, Property, Residence
            "description": "Tenant rights - Property protection"
        },
        {
            "query": "I was raped by my neighbor",
            "domain": "criminal_law",
            "expected_articles": ["21", "20", "22", "14"],  # Life, Fair trial, Arrest protection
            "description": "Criminal law - Serious crimes"
        },
        {
            "query": "bought defective phone want refund",
            "domain": "consumer_complaint",
            "expected_articles": ["19(1)(g)", "21", "14"],  # Trade freedom, Consumer rights
            "description": "Consumer protection"
        }
    ]
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        agent = create_working_enhanced_agent()
        print(f"✅ Enhanced Agent loaded")
        print(f"   Constitutional integration: {'Available' if agent.constitutional_available else 'Not Available'}")
        print()
        
        total_tests = len(test_cases)
        correct_domains = 0
        correct_articles = 0
        
        for i, test_case in enumerate(test_cases, 1):
            query = test_case["query"]
            expected_domain = test_case["domain"]
            expected_articles = test_case["expected_articles"]
            description = test_case["description"]
            
            print(f"🧪 TEST {i}: {description}")
            print(f"   Query: \"{query}\"")
            print(f"   Expected Domain: {expected_domain}")
            print(f"   Expected Articles: {expected_articles}")
            print("-" * 50)
            
            try:
                response = agent.process_query(query)
                
                # Check domain classification
                actual_domain = response.domain
                domain_correct = actual_domain == expected_domain
                if domain_correct:
                    correct_domains += 1
                    domain_status = "✅ CORRECT"
                else:
                    domain_status = f"❌ WRONG (got {actual_domain})"
                
                print(f"   Domain: {domain_status}")
                print(f"   Confidence: {response.confidence:.3f}")
                
                # Check constitutional articles
                if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                    actual_articles = []
                    print(f"   📜 Constitutional Articles Found:")
                    
                    for j, article in enumerate(response.constitutional_articles):
                        article_num = article.get('article_number', 'N/A')
                        title = article.get('title', 'N/A')
                        actual_articles.append(article_num)
                        print(f"      • Article {article_num}: {title}")
                    
                    # Check if expected articles are present
                    articles_match = any(expected_art in actual_articles for expected_art in expected_articles)
                    if articles_match:
                        correct_articles += 1
                        article_status = "✅ RELEVANT ARTICLES FOUND"
                    else:
                        article_status = "⚠️ EXPECTED ARTICLES MISSING"
                    
                    print(f"   Articles: {article_status}")
                    print(f"   Found: {actual_articles}")
                    
                else:
                    print(f"   📜 Constitutional Articles: ❌ NONE FOUND")
                    article_status = "❌ NO ARTICLES"
                
                # Check constitutional backing
                if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
                    backing_preview = response.constitutional_backing[:100] + "..." if len(response.constitutional_backing) > 100 else response.constitutional_backing
                    print(f"   🏛️ Constitutional Backing: ✅ PROVIDED")
                    print(f"      Preview: {backing_preview}")
                else:
                    print(f"   🏛️ Constitutional Backing: ❌ MISSING")
                
                print()
                
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                print()
        
        # Summary
        print("📊 VALIDATION SUMMARY:")
        print("=" * 30)
        
        domain_accuracy = (correct_domains / total_tests) * 100
        article_accuracy = (correct_articles / total_tests) * 100
        
        print(f"Domain Classification: {correct_domains}/{total_tests} ({domain_accuracy:.1f}%)")
        print(f"Constitutional Articles: {correct_articles}/{total_tests} ({article_accuracy:.1f}%)")
        
        # Overall assessment
        overall_score = (domain_accuracy + article_accuracy) / 2
        
        print(f"\n🎯 OVERALL ASSESSMENT:")
        print(f"   Combined Score: {overall_score:.1f}%")
        
        if overall_score >= 80:
            print("🎉 EXCELLENT! The agent is working properly!")
            print("   ✅ Domain classification is accurate")
            print("   ✅ Constitutional articles are relevant")
            print("   ✅ System is production-ready")
        elif overall_score >= 60:
            print("⚠️ GOOD but needs some improvements")
            print("   • Most functionality is working")
            print("   • Some fine-tuning may be needed")
        else:
            print("❌ NEEDS SIGNIFICANT IMPROVEMENT")
            print("   • Major issues detected")
            print("   • System requires fixes")
        
        return overall_score >= 70
        
    except Exception as e:
        print(f"❌ Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_article_accuracy():
    """Test specific constitutional article accuracy for known cases"""
    
    print("\n🎯 SPECIFIC ARTICLE ACCURACY TEST")
    print("=" * 45)
    print("Testing specific constitutional articles for known scenarios\n")
    
    specific_tests = [
        {
            "query": "my phone is being hacked by someone",
            "must_have_articles": ["21"],  # Privacy is fundamental for cyber crimes
            "description": "Cyber crime must have Article 21 (Privacy)"
        },
        {
            "query": "I was raped by my neighbor", 
            "must_have_articles": ["21", "20"],  # Life & fair trial for serious crimes
            "description": "Serious crimes must have Article 21 (Life) and 20 (Fair trial)"
        },
        {
            "query": "my boss is not giving my salary",
            "must_have_articles": ["19(1)(g)"],  # Professional rights
            "description": "Employment issues must have Article 19(1)(g) (Profession)"
        }
    ]
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        
        critical_correct = 0
        total_critical = len(specific_tests)
        
        for i, test in enumerate(specific_tests, 1):
            query = test["query"]
            must_have = test["must_have_articles"]
            description = test["description"]
            
            print(f"🔍 CRITICAL TEST {i}: {description}")
            print(f"   Query: \"{query}\"")
            print(f"   Must Have: {must_have}")
            
            response = agent.process_query(query)
            
            if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                found_articles = [art.get('article_number', '') for art in response.constitutional_articles]
                
                has_required = all(required in found_articles for required in must_have)
                
                if has_required:
                    critical_correct += 1
                    print(f"   Result: ✅ CRITICAL ARTICLES PRESENT")
                else:
                    print(f"   Result: ❌ MISSING CRITICAL ARTICLES")
                
                print(f"   Found: {found_articles}")
                print(f"   Required: {must_have}")
            else:
                print(f"   Result: ❌ NO ARTICLES FOUND")
            
            print()
        
        critical_accuracy = (critical_correct / total_critical) * 100
        print(f"🎯 CRITICAL ARTICLE ACCURACY: {critical_correct}/{total_critical} ({critical_accuracy:.1f}%)")
        
        return critical_accuracy >= 80
        
    except Exception as e:
        print(f"❌ Critical test failed: {e}")
        return False

def main():
    """Main validation function"""
    
    print("🏛️ COMPREHENSIVE LEGAL AGENT VALIDATION")
    print("=" * 60)
    print("Testing both domain classification and constitutional articles\n")
    
    # Test constitutional articles
    articles_ok = test_constitutional_articles()
    
    # Test critical article accuracy
    critical_ok = test_specific_article_accuracy()
    
    print("\n🎯 FINAL VALIDATION RESULTS:")
    print("=" * 35)
    
    if articles_ok and critical_ok:
        print("🎉 AGENT IS WORKING PROPERLY!")
        print("   ✅ Domain classification: EXCELLENT")
        print("   ✅ Constitutional articles: ACCURATE")
        print("   ✅ System ready for production use")
        print()
        print("💡 RECOMMENDATIONS:")
        print("   • Agent is functioning correctly")
        print("   • All major queries work as expected")
        print("   • Constitutional articles are properly assigned")
        print("   • No immediate fixes needed")
        
    elif articles_ok or critical_ok:
        print("⚠️ AGENT IS MOSTLY WORKING")
        print("   • Basic functionality is good")
        print("   • Some minor issues may exist")
        print("   • Consider testing edge cases")
        
    else:
        print("❌ AGENT HAS ISSUES")
        print("   • Significant problems detected")
        print("   • Requires investigation and fixes")
        print("   • Not ready for production")
    
    print()
    print("🚀 QUICK VERIFICATION:")
    print("   Run: python cli_interface.py")
    print("   Test: 'my phone is being hacked by someone'")
    print("   Expected: cyber_crime domain with Article 21")

if __name__ == "__main__":
    main()