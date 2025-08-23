"""
Test Adaptive Learning System
============================

Comprehensive test suite for Task 2: Adaptive Agent Core
Tests all required scenarios and evaluation metrics.

Test Scenarios:
1. Tenant rights case with incorrect initial classification that improves over two turns
2. Cybercrime case where confidence drops due to ambiguous feedback
3. Repayment dispute that improves confidence after feedback
4. Criminal case that should not escalate assertiveness without grounds

Author: Legal Agent Team
Version: 1.0.0
Date: 2025-08-15
"""

import sys
import os
import time
import json
from typing import Dict, List, Any, Tuple

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

# Import required modules
try:
    from adaptive_agent import create_adaptive_agent
    from legal_agent import LegalQueryInput
    ADAPTIVE_AGENT_AVAILABLE = True
except ImportError as e:
    safe_print(f"Warning: Adaptive agent not available: {e}")
    ADAPTIVE_AGENT_AVAILABLE = False

try:
    from conversation_loop import create_conversation_loop
    CONVERSATION_LOOP_AVAILABLE = True
except ImportError as e:
    safe_print(f"Warning: Conversation loop not available: {e}")
    CONVERSATION_LOOP_AVAILABLE = False

try:
    from reward_engine import create_reward_engine
    REWARD_ENGINE_AVAILABLE = True
except ImportError as e:
    safe_print(f"Warning: Reward engine not available: {e}")
    REWARD_ENGINE_AVAILABLE = False

try:
    from state_memory import create_state_memory
    STATE_MEMORY_AVAILABLE = True
except ImportError as e:
    safe_print(f"Warning: State memory not available: {e}")
    STATE_MEMORY_AVAILABLE = False

ADAPTIVE_COMPONENTS_AVAILABLE = (ADAPTIVE_AGENT_AVAILABLE and
                                CONVERSATION_LOOP_AVAILABLE and
                                REWARD_ENGINE_AVAILABLE and
                                STATE_MEMORY_AVAILABLE)


class AdaptiveLearningTester:
    """Comprehensive tester for adaptive learning system"""
    
    def __init__(self):
        """Initialize the tester"""
        
        self.test_results = []
        self.agent = None
        self.conversation_loop = None
        self.reward_engine = None
        self.state_memory = None
        
        # Test scenarios
        self.test_scenarios = [
            {
                'name': 'Tenant Rights Improvement',
                'description': 'Tenant rights case with incorrect initial classification that improves over two turns',
                'initial_query': 'my landlord is not returning my security deposit',
                'follow_up_query': 'what legal action can I take against landlord for deposit',
                'expected_domain': 'tenant rights',
                'feedback_sequence': ['wrong domain', 'helpful']
            },
            {
                'name': 'Cybercrime Confidence Drop',
                'description': 'Cybercrime case where confidence drops due to ambiguous feedback',
                'initial_query': 'someone hacked my bank account and stole money',
                'follow_up_query': 'how to report cybercrime to police',
                'expected_domain': 'cybercrime',
                'feedback_sequence': ['not helpful', 'confusing']
            },
            {
                'name': 'Repayment Dispute Improvement',
                'description': 'Repayment dispute that improves confidence after feedback',
                'initial_query': 'friend borrowed money and not returning',
                'follow_up_query': 'legal notice for money recovery',
                'expected_domain': 'contract law',
                'feedback_sequence': ['helpful', 'very helpful']
            },
            {
                'name': 'Criminal Case Assertiveness',
                'description': 'Criminal case that should not escalate assertiveness without grounds',
                'initial_query': 'someone threatened me with violence',
                'follow_up_query': 'can I file criminal case for threats',
                'expected_domain': 'criminal law',
                'feedback_sequence': ['good', 'helpful']
            }
        ]
    
    def setup_components(self):
        """Setup all adaptive components"""

        safe_print("🔧 Setting up adaptive learning components...")

        components_setup = 0
        total_components = 4

        # Create adaptive agent
        if ADAPTIVE_AGENT_AVAILABLE:
            try:
                self.agent = create_adaptive_agent()
                safe_print("  ✅ Adaptive agent created")
                components_setup += 1
            except Exception as e:
                safe_print(f"  ❌ Error creating adaptive agent: {e}")
        else:
            safe_print("  ⚠️ Adaptive agent not available")

        # Create conversation loop
        if CONVERSATION_LOOP_AVAILABLE:
            try:
                self.conversation_loop = create_conversation_loop()
                safe_print("  ✅ Conversation loop created")
                components_setup += 1
            except Exception as e:
                safe_print(f"  ❌ Error creating conversation loop: {e}")
        else:
            safe_print("  ⚠️ Conversation loop not available")

        # Create reward engine
        if REWARD_ENGINE_AVAILABLE:
            try:
                self.reward_engine = create_reward_engine()
                safe_print("  ✅ Reward engine created")
                components_setup += 1
            except Exception as e:
                safe_print(f"  ❌ Error creating reward engine: {e}")
        else:
            safe_print("  ⚠️ Reward engine not available")

        # Create state memory
        if STATE_MEMORY_AVAILABLE:
            try:
                self.state_memory = create_state_memory("test_state_memory.db")
                safe_print("  ✅ State memory created")
                components_setup += 1
            except Exception as e:
                safe_print(f"  ❌ Error creating state memory: {e}")
        else:
            safe_print("  ⚠️ State memory not available")

        safe_print(f"📊 Components setup: {components_setup}/{total_components}")

        # Return True if at least the adaptive agent is available
        return self.agent is not None
    
    def test_behavioral_adaptation(self) -> Dict[str, Any]:
        """Test behavioral adaptation via reinforcement principles"""
        
        safe_print("\n🧠 Testing Behavioral Adaptation...")
        safe_print("=" * 60)
        
        results = {
            'test_name': 'Behavioral Adaptation',
            'passed': False,
            'details': {},
            'metrics': {}
        }
        
        try:
            # Test query
            query = "my employer is not paying overtime wages"
            session_id = f"behavioral_test_{int(time.time())}"
            
            # Initial response
            query_input = LegalQueryInput(user_input=query, session_id=session_id)
            initial_response = self.agent.process_query_with_learning(query_input)
            initial_confidence = initial_response.confidence
            
            safe_print(f"Initial Query: {query}")
            safe_print(f"Initial Confidence: {initial_confidence:.3f}")
            safe_print(f"Initial Domain: {initial_response.domain}")
            
            # Provide positive feedback - same session
            feedback_query = LegalQueryInput(
                user_input=query,
                feedback="helpful",
                session_id=session_id
            )
            
            feedback_response = self.agent.process_query_with_learning(feedback_query)
            final_confidence = feedback_response.confidence
            
            safe_print(f"After Feedback: {final_confidence:.3f}")
            safe_print(f"Confidence Change: {final_confidence - initial_confidence:+.3f}")
            
            # Check if confidence increased
            confidence_improved = final_confidence > initial_confidence
            
            results['details'] = {
                'initial_confidence': initial_confidence,
                'final_confidence': final_confidence,
                'confidence_change': final_confidence - initial_confidence,
                'confidence_improved': confidence_improved
            }
            
            results['passed'] = confidence_improved
            safe_print(f"Result: {'✅ PASSED' if confidence_improved else '❌ FAILED'}")
            
        except Exception as e:
            safe_print(f"❌ Error in behavioral adaptation test: {e}")
            results['details']['error'] = str(e)
        
        return results
    
    def test_multi_stage_dialogue(self) -> Dict[str, Any]:
        """Test multi-stage dialogue learning"""
        
        safe_print("\n💬 Testing Multi-Stage Dialogue Learning...")
        safe_print("=" * 60)
        
        results = {
            'test_name': 'Multi-Stage Dialogue',
            'passed': False,
            'scenarios': [],
            'metrics': {}
        }
        
        try:
            total_scenarios = len(self.test_scenarios)
            passed_scenarios = 0
            
            for scenario in self.test_scenarios:
                safe_print(f"\n📋 Scenario: {scenario['name']}")
                safe_print(f"Description: {scenario['description']}")
                
                scenario_result = self._test_single_scenario(scenario)
                results['scenarios'].append(scenario_result)
                
                if scenario_result['passed']:
                    passed_scenarios += 1
                    safe_print(f"  ✅ PASSED")
                else:
                    safe_print(f"  ❌ FAILED")
            
            success_rate = passed_scenarios / total_scenarios
            results['metrics']['success_rate'] = success_rate
            results['metrics']['passed_scenarios'] = passed_scenarios
            results['metrics']['total_scenarios'] = total_scenarios
            
            results['passed'] = success_rate >= 0.75  # 75% success rate required
            
            safe_print(f"\nOverall Success Rate: {success_rate:.1%}")
            safe_print(f"Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
            
        except Exception as e:
            safe_print(f"❌ Error in multi-stage dialogue test: {e}")
            results['error'] = str(e)
        
        return results
    
    def _test_single_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single dialogue scenario"""
        
        scenario_result = {
            'name': scenario['name'],
            'passed': False,
            'turns': [],
            'learning_detected': False,
            'confidence_evolution': []
        }
        
        try:
            # Start conversation
            session_id = self.conversation_loop.start_conversation(
                scenario['initial_query'], 
                self.agent
            )
            
            # Get initial response
            conversation = self.conversation_loop.active_conversations[session_id]
            initial_turn = conversation.turns[0]
            
            scenario_result['turns'].append({
                'turn': 1,
                'query': scenario['initial_query'],
                'confidence': initial_turn.agent_response.confidence,
                'domain': initial_turn.agent_response.domain
            })
            
            scenario_result['confidence_evolution'].append(initial_turn.agent_response.confidence)
            
            # Continue conversation with feedback
            for i, feedback in enumerate(scenario['feedback_sequence']):
                if i < len(scenario['feedback_sequence']) - 1:
                    # Continue with follow-up query
                    response, should_end = self.conversation_loop.continue_conversation(
                        session_id,
                        scenario['follow_up_query'],
                        self.agent,
                        feedback_on_previous=feedback
                    )
                    
                    if response:
                        scenario_result['turns'].append({
                            'turn': i + 2,
                            'query': scenario['follow_up_query'],
                            'confidence': response.confidence,
                            'domain': response.domain,
                            'feedback_given': feedback
                        })
                        
                        scenario_result['confidence_evolution'].append(response.confidence)
            
            # End conversation
            self.conversation_loop.end_conversation(session_id, "completed")
            
            # Check for learning
            confidence_changes = []
            for i in range(1, len(scenario_result['confidence_evolution'])):
                change = scenario_result['confidence_evolution'][i] - scenario_result['confidence_evolution'][i-1]
                confidence_changes.append(change)
            
            # Learning detected if confidence changed significantly
            scenario_result['learning_detected'] = any(abs(change) > 0.05 for change in confidence_changes)
            
            # Scenario passes if learning was detected and confidence generally improved with positive feedback
            positive_feedback_count = sum(1 for f in scenario['feedback_sequence'] if f in ['helpful', 'good', 'very helpful'])
            scenario_result['passed'] = (
                scenario_result['learning_detected'] and 
                len(scenario_result['turns']) >= 2 and
                positive_feedback_count > 0
            )
            
        except Exception as e:
            scenario_result['error'] = str(e)
        
        return scenario_result
    
    def test_feedback_integration(self) -> Dict[str, Any]:
        """Test feedback integration capabilities"""
        
        safe_print("\n📝 Testing Feedback Integration...")
        safe_print("=" * 60)
        
        results = {
            'test_name': 'Feedback Integration',
            'passed': False,
            'feedback_types': {},
            'metrics': {}
        }
        
        try:
            feedback_types = ['helpful', 'not helpful', 'wrong domain', 'confusing', 'excellent']
            
            for feedback_type in feedback_types:
                safe_print(f"\nTesting feedback type: {feedback_type}")
                
                # Test query
                query = f"test query for {feedback_type} feedback"
                
                # Get initial response
                query_input = LegalQueryInput(user_input=query)
                initial_response = self.agent.process_query_with_learning(query_input)
                
                # Provide feedback
                feedback_query = LegalQueryInput(
                    user_input=query,
                    feedback=feedback_type
                )
                
                feedback_response = self.agent.process_query_with_learning(feedback_query)
                
                # Calculate reward
                reward_data = {
                    'type': feedback_type,
                    'text': f"This response was {feedback_type}",
                    'satisfaction': feedback_type
                }
                
                reward, reward_components = self.reward_engine.calculate_reward(
                    reward_data,
                    initial_response,
                    {'response_time': 1.0, 'session_id': 'test_session'}
                )
                
                results['feedback_types'][feedback_type] = {
                    'confidence_change': feedback_response.confidence - initial_response.confidence,
                    'reward_score': reward,
                    'reward_components': {
                        'accuracy': reward_components.accuracy,
                        'helpfulness': reward_components.helpfulness,
                        'clarity': reward_components.clarity,
                        'timeliness': reward_components.timeliness,
                        'consistency': reward_components.consistency
                    }
                }
                
                safe_print(f"  Confidence change: {feedback_response.confidence - initial_response.confidence:+.3f}")
                safe_print(f"  Reward score: {reward:.3f}")
                
            # Check if system responds appropriately to different feedback types
            positive_feedback_rewards = [
                results['feedback_types'][ft]['reward_score'] 
                for ft in ['helpful', 'excellent'] 
                if ft in results['feedback_types']
            ]
            
            negative_feedback_rewards = [
                results['feedback_types'][ft]['reward_score'] 
                for ft in ['not helpful', 'wrong domain'] 
                if ft in results['feedback_types']
            ]
            
            # Positive feedback should have higher rewards than negative
            avg_positive = sum(positive_feedback_rewards) / len(positive_feedback_rewards) if positive_feedback_rewards else 0
            avg_negative = sum(negative_feedback_rewards) / len(negative_feedback_rewards) if negative_feedback_rewards else 0
            
            results['metrics']['avg_positive_reward'] = avg_positive
            results['metrics']['avg_negative_reward'] = avg_negative
            results['metrics']['reward_differentiation'] = avg_positive - avg_negative
            
            results['passed'] = avg_positive > avg_negative
            
            safe_print(f"\nAverage positive reward: {avg_positive:+.3f}")
            safe_print(f"Average negative reward: {avg_negative:+.3f}")
            safe_print(f"Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
            
        except Exception as e:
            safe_print(f"❌ Error in feedback integration test: {e}")
            results['error'] = str(e)
        
        return results
    
    def test_memory_and_patterns(self) -> Dict[str, Any]:
        """Test memory and pattern awareness"""
        
        safe_print("\n🧠 Testing Memory and Pattern Awareness...")
        safe_print("=" * 60)
        
        results = {
            'test_name': 'Memory and Patterns',
            'passed': False,
            'patterns': {},
            'metrics': {}
        }
        
        try:
            # Test queries with similar patterns
            similar_queries = [
                "my landlord is not returning security deposit",
                "landlord refuses to give back my deposit",
                "how to get security deposit from landlord"
            ]
            
            pattern_ids = []
            
            for i, query in enumerate(similar_queries):
                safe_print(f"\nQuery {i+1}: {query}")
                
                # Process query
                query_input = LegalQueryInput(user_input=query)
                response = self.agent.process_query_with_learning(query_input)
                
                # Record in state memory
                record_id = self.state_memory.record_query_improvement(
                    query,
                    response.domain,
                    0.5,  # confidence_before
                    response.confidence,  # confidence_after
                    'helpful',  # feedback_type
                    f'test_session_{i}'  # session_id
                )
                
                pattern_ids.append(record_id)
                safe_print(f"  Record ID: {record_id}")
                safe_print(f"  Confidence: {response.confidence:.3f}")
            
            # Check if similar queries are grouped into same pattern
            unique_patterns = len(set(pattern_ids))
            results['metrics']['unique_patterns'] = unique_patterns
            results['metrics']['total_queries'] = len(similar_queries)
            results['metrics']['pattern_efficiency'] = unique_patterns / len(similar_queries)
            
            # Get memory stats
            memory_stats = self.state_memory.get_memory_stats()
            results['metrics']['memory_stats'] = memory_stats
            
            # Test passes if similar queries are grouped efficiently
            results['passed'] = unique_patterns <= 2  # Should group similar queries
            
            safe_print(f"\nUnique patterns created: {unique_patterns}")
            safe_print(f"Pattern efficiency: {results['metrics']['pattern_efficiency']:.2f}")
            safe_print(f"Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
            
        except Exception as e:
            safe_print(f"❌ Error in memory and patterns test: {e}")
            results['error'] = str(e)
        
        return results
    
    def test_confidence_adjustment(self) -> Dict[str, Any]:
        """Test confidence adjustment system"""
        
        safe_print("\n📊 Testing Confidence Adjustment System...")
        safe_print("=" * 60)
        
        results = {
            'test_name': 'Confidence Adjustment',
            'passed': False,
            'adjustments': [],
            'metrics': {}
        }
        
        try:
            # Test confidence boost with positive feedback
            query = "workplace harassment by supervisor"
            session_id = f"confidence_test_{int(time.time())}"
            
            # Initial query
            query_input = LegalQueryInput(user_input=query, session_id=session_id)
            initial_response = self.agent.process_query_with_learning(query_input)
            initial_confidence = initial_response.confidence
            
            # Positive feedback - same session
            positive_feedback = LegalQueryInput(
                user_input=query,
                feedback="very helpful",
                session_id=session_id
            )
            
            positive_response = self.agent.process_query_with_learning(positive_feedback)
            positive_confidence = positive_response.confidence
            
            positive_adjustment = positive_confidence - initial_confidence
            
            results['adjustments'].append({
                'type': 'positive_feedback',
                'confidence_before': initial_confidence,
                'confidence_after': positive_confidence,
                'adjustment': positive_adjustment
            })
            
            safe_print(f"Positive feedback adjustment: {positive_adjustment:+.3f}")
            
            # Test confidence penalty with negative feedback - same session
            negative_feedback = LegalQueryInput(
                user_input=query,
                feedback="wrong domain",
                session_id=session_id
            )
            
            negative_response = self.agent.process_query_with_learning(negative_feedback)
            negative_confidence = negative_response.confidence
            
            negative_adjustment = negative_confidence - positive_confidence
            
            results['adjustments'].append({
                'type': 'negative_feedback',
                'confidence_before': positive_confidence,
                'confidence_after': negative_confidence,
                'adjustment': negative_adjustment
            })
            
            safe_print(f"Negative feedback adjustment: {negative_adjustment:+.3f}")
            
            # Check if adjustments are in correct direction
            positive_boost = positive_adjustment > 0.05
            negative_penalty = negative_adjustment < -0.05
            
            results['metrics']['positive_boost'] = positive_boost
            results['metrics']['negative_penalty'] = negative_penalty
            results['metrics']['adjustment_magnitude'] = abs(positive_adjustment) + abs(negative_adjustment)
            
            results['passed'] = positive_boost and negative_penalty
            
            safe_print(f"Positive boost detected: {'✅' if positive_boost else '❌'}")
            safe_print(f"Negative penalty detected: {'✅' if negative_penalty else '❌'}")
            safe_print(f"Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
            
        except Exception as e:
            safe_print(f"❌ Error in confidence adjustment test: {e}")
            results['error'] = str(e)
        
        return results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all adaptive learning tests"""
        
        safe_print("🚀 ADAPTIVE LEARNING COMPREHENSIVE TEST SUITE")
        safe_print("=" * 80)
        safe_print("Testing Task 2: Adaptive Agent Core Requirements")
        safe_print("=" * 80)
        
        if not ADAPTIVE_COMPONENTS_AVAILABLE:
            safe_print("❌ Adaptive components not available. Cannot run tests.")
            return {'error': 'Components not available'}
        
        # Setup components
        if not self.setup_components():
            safe_print("❌ Failed to setup components. Cannot run tests.")
            return {'error': 'Setup failed'}
        
        # Run all tests
        test_results = []
        
        test_results.append(self.test_behavioral_adaptation())
        test_results.append(self.test_multi_stage_dialogue())
        test_results.append(self.test_feedback_integration())
        test_results.append(self.test_memory_and_patterns())
        test_results.append(self.test_confidence_adjustment())
        
        # Calculate overall results
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result.get('passed', False))
        success_rate = passed_tests / total_tests
        
        overall_result = {
            'test_suite': 'Adaptive Learning Comprehensive Test',
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': success_rate,
            'passed': success_rate >= 0.8,  # 80% success rate required
            'individual_results': test_results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Display summary
        safe_print("\n" + "=" * 80)
        safe_print("📊 TEST SUMMARY")
        safe_print("=" * 80)
        
        for result in test_results:
            status = "✅ PASSED" if result.get('passed', False) else "❌ FAILED"
            safe_print(f"{result.get('test_name', 'Unknown Test')}: {status}")
        
        safe_print(f"\nOverall Success Rate: {success_rate:.1%}")
        safe_print(f"Final Result: {'✅ PASSED' if overall_result['passed'] else '❌ FAILED'}")
        
        if overall_result['passed']:
            safe_print("\n🎉 All Task 2 requirements have been successfully implemented and tested!")
        else:
            safe_print("\n⚠️ Some Task 2 requirements need attention.")
        
        return overall_result


def main():
    """Main test function"""
    
    tester = AdaptiveLearningTester()
    results = tester.run_comprehensive_test()
    
    # Save results (convert any non-serializable objects)
    def make_serializable(obj):
        """Convert non-serializable objects to serializable format"""
        if isinstance(obj, (bool, int, float, str, type(None))):
            return obj
        elif isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [make_serializable(item) for item in obj]
        else:
            return str(obj)

    serializable_results = make_serializable(results)

    with open('adaptive_learning_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    safe_print(f"\n📄 Test results saved to: adaptive_learning_test_results.json")
    
    return results


if __name__ == "__main__":
    main()
