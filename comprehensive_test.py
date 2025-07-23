"""
Comprehensive Test Script for Legal Agent System
===============================================

This script tests all functionality of the Legal Agent system including:
- Domain classification accuracy
- Legal route recommendations
- Process step explanations
- Glossary term identification
- Data integration features
- Feedback system
- Location-based insights

Usage:
    python comprehensive_test.py

Author: Legal Agent Team
Version: 2.0.0
Date: 2025-07-22
"""

import json
import time
from typing import List, Dict, Any
from legal_agent import LegalAgent, LegalQueryInput, create_legal_agent
from data_integration import CrimeDataAnalyzer


class LegalAgentTester:
    """Comprehensive testing suite for Legal Agent"""
    
    def __init__(self):
        """Initialize the tester with agent and test data"""
        print("🚀 Initializing Legal Agent Test Suite...")
        self.agent = create_legal_agent()
        self.test_results = {
            'classification_tests': [],
            'route_tests': [],
            'location_tests': [],
            'feedback_tests': [],
            'performance_tests': [],
            'data_integration_tests': []
        }
        
        # Test scenarios with expected outcomes
        self.test_scenarios = [
            {
                'query': "My landlord won't return my security deposit in Mumbai",
                'expected_domain': 'tenant rights',
                'expected_confidence_min': 0.4,
                'location': 'Mumbai',
                'test_type': 'basic_classification'
            },
            {
                'query': "My elderly mother is being abused in Delhi nursing home",
                'expected_domain': 'elder abuse',
                'expected_confidence_min': 0.3,
                'location': 'Delhi',
                'test_type': 'elder_abuse_with_location'
            },
            {
                'query': "Someone hacked my bank account and stole money",
                'expected_domain': 'cyber crime',
                'expected_confidence_min': 0.4,
                'location': None,
                'test_type': 'cyber_crime'
            },
            {
                'query': "I want to divorce my husband and get custody of children",
                'expected_domain': 'family law',
                'expected_confidence_min': 0.6,
                'location': None,
                'test_type': 'family_law'
            },
            {
                'query': "My employer fired me for filing harassment complaint in Bangalore",
                'expected_domain': 'employment law',
                'expected_confidence_min': 0.5,
                'location': 'Bangalore',
                'test_type': 'employment_with_location'
            },
            {
                'query': "I was hit by a car and need compensation for medical bills",
                'expected_domain': 'personal injury',
                'expected_confidence_min': 0.5,
                'location': None,
                'test_type': 'personal_injury'
            },
            {
                'query': "How do I patent my new invention?",
                'expected_domain': 'unknown',
                'expected_confidence_min': 0.0,
                'location': None,
                'test_type': 'unknown_domain'
            },
            {
                'query': "Senior citizen harassment case in Maharashtra",
                'expected_domain': 'elder abuse',
                'expected_confidence_min': 0.3,
                'location': 'Maharashtra',
                'test_type': 'data_integration_test'
            }
        ]
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites"""
        print("\n" + "="*60)
        print("🧪 RUNNING COMPREHENSIVE LEGAL AGENT TESTS")
        print("="*60)
        
        # Run test suites
        self.test_domain_classification()
        self.test_legal_routes()
        self.test_location_extraction()
        self.test_data_integration()
        self.test_feedback_system()
        self.test_performance()
        
        # Generate final report
        return self.generate_test_report()
    
    def test_domain_classification(self):
        """Test domain classification accuracy"""
        print("\n📊 Testing Domain Classification...")
        
        correct_classifications = 0
        total_tests = len(self.test_scenarios)
        
        for i, scenario in enumerate(self.test_scenarios):
            query_input = LegalQueryInput(user_input=scenario['query'])
            response = self.agent.process_query(query_input)
            
            # Check classification accuracy
            is_correct = response.domain == scenario['expected_domain']
            confidence_ok = response.confidence >= scenario['expected_confidence_min']
            
            if is_correct:
                correct_classifications += 1
            
            test_result = {
                'test_id': i + 1,
                'query': scenario['query'],
                'expected_domain': scenario['expected_domain'],
                'actual_domain': response.domain,
                'confidence': response.confidence,
                'classification_correct': is_correct,
                'confidence_adequate': confidence_ok,
                'overall_pass': is_correct and confidence_ok
            }
            
            self.test_results['classification_tests'].append(test_result)
            
            status = "✅ PASS" if test_result['overall_pass'] else "❌ FAIL"
            print(f"  Test {i+1}: {status} - {scenario['expected_domain']} "
                  f"(Got: {response.domain}, Conf: {response.confidence:.2f})")
        
        accuracy = (correct_classifications / total_tests) * 100
        print(f"\n📈 Classification Accuracy: {accuracy:.1f}% ({correct_classifications}/{total_tests})")
    
    def test_legal_routes(self):
        """Test legal route recommendations"""
        print("\n🛣️  Testing Legal Route Recommendations...")
        
        route_tests_passed = 0
        
        for i, scenario in enumerate(self.test_scenarios):
            query_input = LegalQueryInput(user_input=scenario['query'])
            response = self.agent.process_query(query_input)
            
            # Check if route is provided and relevant
            has_route = bool(response.legal_route and len(response.legal_route) > 10)
            has_timeline = bool(response.timeline and response.timeline != 'N/A')
            has_outcome = bool(response.outcome and len(response.outcome) > 5)
            has_steps = bool(response.process_steps and len(response.process_steps) > 0)
            
            route_quality = has_route and has_timeline and has_outcome and has_steps
            
            if route_quality:
                route_tests_passed += 1
            
            test_result = {
                'test_id': i + 1,
                'domain': response.domain,
                'has_route': has_route,
                'has_timeline': has_timeline,
                'has_outcome': has_outcome,
                'has_steps': has_steps,
                'route_quality': route_quality,
                'step_count': len(response.process_steps)
            }
            
            self.test_results['route_tests'].append(test_result)
            
            status = "✅ PASS" if route_quality else "❌ FAIL"
            print(f"  Test {i+1}: {status} - {response.domain} "
                  f"({len(response.process_steps)} steps)")
        
        route_accuracy = (route_tests_passed / len(self.test_scenarios)) * 100
        print(f"\n📈 Route Quality: {route_accuracy:.1f}% ({route_tests_passed}/{len(self.test_scenarios)})")
    
    def test_location_extraction(self):
        """Test location extraction from queries"""
        print("\n🌍 Testing Location Extraction...")
        
        location_tests_passed = 0
        location_scenarios = [s for s in self.test_scenarios if s['location']]
        
        for i, scenario in enumerate(location_scenarios):
            extracted_location = self.agent.domain_classifier.extract_location(scenario['query'])
            
            location_correct = (extracted_location and 
                              scenario['location'].lower() in extracted_location.lower())
            
            if location_correct:
                location_tests_passed += 1
            
            test_result = {
                'test_id': i + 1,
                'query': scenario['query'],
                'expected_location': scenario['location'],
                'extracted_location': extracted_location,
                'location_correct': location_correct
            }
            
            self.test_results['location_tests'].append(test_result)
            
            status = "✅ PASS" if location_correct else "❌ FAIL"
            print(f"  Test {i+1}: {status} - Expected: {scenario['location']}, "
                  f"Got: {extracted_location}")
        
        if location_scenarios:
            location_accuracy = (location_tests_passed / len(location_scenarios)) * 100
            print(f"\n📈 Location Extraction: {location_accuracy:.1f}% "
                  f"({location_tests_passed}/{len(location_scenarios)})")
    
    def test_data_integration(self):
        """Test data integration features"""
        print("\n📊 Testing Data Integration...")
        
        if not self.agent.data_integration_enabled:
            print("  ⚠️ Data integration not available - skipping tests")
            return
        
        # Test crime data analysis
        crime_analyzer = self.agent.crime_analyzer
        
        # Test 1: High-risk states identification
        high_risk_states = crime_analyzer.get_high_risk_states(50.0)
        test_1_pass = len(high_risk_states) > 0
        
        # Test 2: Location-specific advice
        delhi_advice = crime_analyzer.get_location_based_advice("Delhi", "senior_citizen_abuse")
        test_2_pass = delhi_advice.get('location_found', False)
        
        # Test 3: Crime trends analysis
        trends = crime_analyzer.analyze_crime_trends()
        test_3_pass = 'total_crimes' in trends and '2022' in trends['total_crimes']
        
        # Test 4: Enhanced response with location data
        elder_query = LegalQueryInput(user_input="My elderly father is being abused in Delhi")
        response = self.agent.process_query(elder_query)
        test_4_pass = response.data_driven_advice is not None
        
        data_tests = [test_1_pass, test_2_pass, test_3_pass, test_4_pass]
        data_tests_passed = sum(data_tests)
        
        self.test_results['data_integration_tests'] = {
            'high_risk_identification': test_1_pass,
            'location_advice': test_2_pass,
            'trends_analysis': test_3_pass,
            'enhanced_response': test_4_pass,
            'total_passed': data_tests_passed,
            'total_tests': len(data_tests)
        }
        
        print(f"  High-risk states: {'✅ PASS' if test_1_pass else '❌ FAIL'}")
        print(f"  Location advice: {'✅ PASS' if test_2_pass else '❌ FAIL'}")
        print(f"  Trends analysis: {'✅ PASS' if test_3_pass else '❌ FAIL'}")
        print(f"  Enhanced response: {'✅ PASS' if test_4_pass else '❌ FAIL'}")
        
        data_accuracy = (data_tests_passed / len(data_tests)) * 100
        print(f"\n📈 Data Integration: {data_accuracy:.1f}% ({data_tests_passed}/{len(data_tests)})")
    
    def test_feedback_system(self):
        """Test feedback collection and analysis"""
        print("\n💬 Testing Feedback System...")
        
        # Test feedback collection
        feedback_query = LegalQueryInput(
            user_input="Test feedback query",
            feedback="This was very helpful!"
        )
        
        response = self.agent.process_query(feedback_query)
        
        # Test feedback statistics
        stats = self.agent.get_feedback_stats()
        
        feedback_tests = {
            'feedback_collected': stats['total_feedback'] > 0,
            'stats_generated': 'domains' in stats,
            'session_tracking': bool(response.session_id)
        }
        
        self.test_results['feedback_tests'] = feedback_tests
        
        for test_name, result in feedback_tests.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name.replace('_', ' ').title()}: {status}")
    
    def test_performance(self):
        """Test system performance"""
        print("\n⚡ Testing Performance...")
        
        # Test response time
        start_time = time.time()
        query = LegalQueryInput(user_input="Performance test query")
        response = self.agent.process_query(query)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        performance_tests = {
            'response_time_ok': response_time < 2.0,  # Should respond within 2 seconds
            'response_complete': all([
                response.domain,
                response.legal_route,
                response.timeline,
                response.outcome,
                response.process_steps,
                response.session_id
            ])
        }
        
        self.test_results['performance_tests'] = {
            'response_time_seconds': response_time,
            'response_time_ok': performance_tests['response_time_ok'],
            'response_complete': performance_tests['response_complete']
        }
        
        print(f"  Response time: {response_time:.2f}s {'✅ PASS' if performance_tests['response_time_ok'] else '❌ FAIL'}")
        print(f"  Response complete: {'✅ PASS' if performance_tests['response_complete'] else '❌ FAIL'}")
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("📋 FINAL TEST REPORT")
        print("="*60)
        
        # Calculate overall scores
        classification_score = sum(1 for t in self.test_results['classification_tests'] if t['overall_pass'])
        classification_total = len(self.test_results['classification_tests'])
        
        route_score = sum(1 for t in self.test_results['route_tests'] if t['route_quality'])
        route_total = len(self.test_results['route_tests'])
        
        location_score = sum(1 for t in self.test_results['location_tests'] if t['location_correct'])
        location_total = len(self.test_results['location_tests'])
        
        # Overall system score
        total_tests = classification_total + route_total + location_total
        total_passed = classification_score + route_score + location_score
        overall_score = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'overall_score': overall_score,
            'classification_accuracy': (classification_score / classification_total * 100) if classification_total > 0 else 0,
            'route_quality': (route_score / route_total * 100) if route_total > 0 else 0,
            'location_accuracy': (location_score / location_total * 100) if location_total > 0 else 0,
            'data_integration_enabled': self.agent.data_integration_enabled,
            'detailed_results': self.test_results
        }
        
        print(f"🎯 Overall Score: {overall_score:.1f}%")
        print(f"📊 Classification: {report['classification_accuracy']:.1f}%")
        print(f"🛣️  Route Quality: {report['route_quality']:.1f}%")
        print(f"🌍 Location Extraction: {report['location_accuracy']:.1f}%")
        print(f"📊 Data Integration: {'✅ Enabled' if self.agent.data_integration_enabled else '❌ Disabled'}")
        
        # Save detailed report
        with open('test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: test_report.json")
        
        return report


def main():
    """Main function to run comprehensive tests"""
    tester = LegalAgentTester()
    report = tester.run_all_tests()
    
    print("\n🎉 Testing completed!")
    print(f"📊 Overall system performance: {report['overall_score']:.1f}%")
    
    if report['overall_score'] >= 80:
        print("✅ System is ready for production!")
    elif report['overall_score'] >= 60:
        print("⚠️ System needs minor improvements before production.")
    else:
        print("❌ System needs significant improvements before production.")


if __name__ == "__main__":
    main()
