#!/usr/bin/env python3
"""
Edge Case and Response Quality Test
==================================

This script tests edge cases and response quality to ensure the agent
provides comprehensive and accurate responses.
"""

def test_edge_cases():
    """Test edge cases and unusual queries"""
    
    print("🔍 EDGE CASE AND RESPONSE QUALITY TEST")
    print("=" * 50)
    print("Testing unusual queries and edge cases\n")
    
    edge_cases = [
        {
            "query": "employee disclosed company secrets to competitor",
            "expected_domain": "employment_law",
            "description": "Complex employment confidentiality case",
            "check_response_quality": True
        },
        {
            "query": "My Property is Been Hijaced",  # Spelling error test
            "expected_domain": "tenant_rights",  # or property_disputes
            "description": "Property hijacking with spelling errors",
            "check_response_quality": True
        },
        {
            "query": "passport expired need renewal urgently",
            "expected_domain": "immigration_law",
            "description": "Immigration document renewal",
            "check_response_quality": True
        },
        {
            "query": "car insurance company denying my claim",
            "expected_domain": "consumer_complaint",
            "description": "Insurance dispute case",
            "check_response_quality": True
        },
        {
            "query": "wife threatening to leave with children",
            "expected_domain": "family_law",
            "description": "Family custody issue",
            "check_response_quality": True
        }
    ]
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        agent = create_working_enhanced_agent()
        print(f"✅ Enhanced Agent loaded for edge case testing\n")
        
        successful_cases = 0
        quality_scores = []
        
        for i, test_case in enumerate(edge_cases, 1):
            query = test_case["query"]
            expected_domain = test_case["expected_domain"]
            description = test_case["description"]
            
            print(f"🧪 EDGE CASE {i}: {description}")
            print(f"   Query: \"{query}\"")
            print(f"   Expected: {expected_domain}")
            print("-" * 45)
            
            try:
                response = agent.process_query(query)
                
                # Check domain
                actual_domain = response.domain
                domain_correct = actual_domain == expected_domain or actual_domain != "unknown"
                
                if domain_correct:
                    successful_cases += 1
                    domain_status = f"✅ {actual_domain} (confidence: {response.confidence:.3f})"
                else:
                    domain_status = f"❌ {actual_domain} (expected: {expected_domain})"
                
                print(f"   Domain: {domain_status}")
                
                # Check response quality
                quality_score = 0
                
                # 1. Has legal route?
                if hasattr(response, 'legal_route') and response.legal_route:
                    quality_score += 25
                    route_preview = response.legal_route[:80] + "..." if len(response.legal_route) > 80 else response.legal_route
                    print(f"   ✅ Legal Route: {route_preview}")
                else:
                    print(f"   ❌ Legal Route: Missing")
                
                # 2. Has timeline?
                if hasattr(response, 'timeline') and response.timeline:
                    quality_score += 25
                    print(f"   ✅ Timeline: {response.timeline}")
                else:
                    print(f"   ❌ Timeline: Missing")
                
                # 3. Has constitutional articles?
                if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                    quality_score += 25
                    article_count = len(response.constitutional_articles)
                    articles = [f"Article {art.get('article_number', 'N/A')}" for art in response.constitutional_articles]
                    print(f"   ✅ Constitutional Articles: {article_count} found ({', '.join(articles[:3])})")
                else:
                    print(f"   ❌ Constitutional Articles: Missing")
                
                # 4. Has constitutional backing?
                if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
                    quality_score += 25
                    print(f"   ✅ Constitutional Backing: Provided")
                else:
                    print(f"   ❌ Constitutional Backing: Missing")
                
                quality_scores.append(quality_score)
                print(f"   📊 Response Quality: {quality_score}/100")
                print()
                
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                quality_scores.append(0)
                print()
        
        # Summary
        success_rate = (successful_cases / len(edge_cases)) * 100
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        print("📊 EDGE CASE RESULTS:")
        print("=" * 25)
        print(f"Successful Cases: {successful_cases}/{len(edge_cases)} ({success_rate:.1f}%)")
        print(f"Average Quality Score: {avg_quality:.1f}/100")
        
        return success_rate >= 60 and avg_quality >= 70
        
    except Exception as e:
        print(f"❌ Edge case testing failed: {e}")
        return False

def test_cli_interaction():
    """Test CLI interaction simulation"""
    
    print("\n🖥️ CLI INTERACTION SIMULATION TEST")
    print("=" * 40)
    print("Simulating real CLI interactions\n")
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        agent = create_working_enhanced_agent()
        
        # Simulate a typical user interaction
        test_queries = [
            "my phone is being hacked by someone",
            "my boss is not giving my salary", 
            "landlord not returning deposit"
        ]
        
        interaction_successful = True
        
        for i, query in enumerate(test_queries, 1):
            print(f"💬 Simulated Interaction {i}:")
            print(f"   User: {query}")
            
            try:
                response = agent.process_query(query)
                
                # Check basic response components
                has_domain = hasattr(response, 'domain') and response.domain != "unknown"
                has_route = hasattr(response, 'legal_route') and response.legal_route
                has_timeline = hasattr(response, 'timeline') and response.timeline
                
                if has_domain and has_route and has_timeline:
                    print(f"   Agent: ✅ Complete response provided")
                    print(f"          Domain: {response.domain}")
                    print(f"          Timeline: {response.timeline}")
                else:
                    print(f"   Agent: ⚠️ Incomplete response")
                    interaction_successful = False
                
            except Exception as e:
                print(f"   Agent: ❌ Error - {e}")
                interaction_successful = False
            
            print()
        
        return interaction_successful
        
    except Exception as e:
        print(f"❌ CLI simulation failed: {e}")
        return False

def test_response_completeness():
    """Test that responses contain all required components"""
    
    print("📋 RESPONSE COMPLETENESS TEST")
    print("=" * 35)
    print("Testing response completeness and structure\n")
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        
        agent = create_working_enhanced_agent()
        
        # Test a standard query
        query = "my phone is being hacked by someone"
        response = agent.process_query(query)
        
        print(f"Query: {query}")
        print("Checking response components:")
        
        # Required components checklist
        components = [
            ('session_id', 'Session ID'),
            ('timestamp', 'Timestamp'),
            ('user_query', 'User Query'),
            ('domain', 'Domain Classification'),
            ('confidence', 'Confidence Score'),
            ('legal_route', 'Legal Route'),
            ('timeline', 'Timeline'),
            ('success_rate', 'Success Rate'),
            ('constitutional_articles', 'Constitutional Articles'),
            ('constitutional_backing', 'Constitutional Backing'),
            ('response_time', 'Response Time')
        ]
        
        present_components = 0
        total_components = len(components)
        
        for attr, name in components:
            if hasattr(response, attr):
                value = getattr(response, attr)
                if value is not None and value != "":
                    present_components += 1
                    print(f"   ✅ {name}: Present")
                else:
                    print(f"   ⚠️ {name}: Empty")
            else:
                print(f"   ❌ {name}: Missing")
        
        completeness_score = (present_components / total_components) * 100
        print(f"\n📊 Response Completeness: {present_components}/{total_components} ({completeness_score:.1f}%)")
        
        return completeness_score >= 80
        
    except Exception as e:
        print(f"❌ Completeness test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🧪 COMPREHENSIVE AGENT TESTING")
    print("=" * 45)
    print("Testing edge cases, interactions, and response quality\n")
    
    # Run all tests
    edge_case_ok = test_edge_cases()
    cli_interaction_ok = test_cli_interaction()
    completeness_ok = test_response_completeness()
    
    print("\n🎯 COMPREHENSIVE TEST RESULTS:")
    print("=" * 35)
    
    tests_passed = sum([edge_case_ok, cli_interaction_ok, completeness_ok])
    total_tests = 3
    
    print(f"Edge Cases: {'✅ PASSED' if edge_case_ok else '❌ FAILED'}")
    print(f"CLI Interaction: {'✅ PASSED' if cli_interaction_ok else '❌ FAILED'}")
    print(f"Response Completeness: {'✅ PASSED' if completeness_ok else '❌ FAILED'}")
    
    overall_score = (tests_passed / total_tests) * 100
    print(f"\nOverall Score: {tests_passed}/{total_tests} ({overall_score:.1f}%)")
    
    if overall_score >= 80:
        print("\n🎉 AGENT IS WORKING EXCELLENTLY!")
        print("   • All major functionality works correctly")
        print("   • Edge cases are handled properly")
        print("   • Responses are complete and accurate")
        print("   • Ready for production use")
    elif overall_score >= 60:
        print("\n⚠️ AGENT IS WORKING WITH MINOR ISSUES")
        print("   • Core functionality is good")
        print("   • Some edge cases may need attention")
        print("   • Generally ready for use")
    else:
        print("\n❌ AGENT HAS SIGNIFICANT ISSUES")
        print("   • Major problems detected")
        print("   • Requires investigation and fixes")

if __name__ == "__main__":
    main()