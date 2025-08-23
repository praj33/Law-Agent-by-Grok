"""
Reward Engine - Task 2 Implementation
====================================

This module calculates value of feedback per episode using multi-dimensional rewards.
Implements the reward_engine.py requirement for Task 2.

Features:
- Multi-dimensional reward calculation
- Reinforcement learning principles
- Adaptive learning rate adjustment
- Transparent reward tracking
- Performance-based reward weighting

Author: Legal Agent Team
Version: 3.0.0 (Task 2 - Reward Engine)
Date: 2025-08-15
"""

import json
import datetime
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)


@dataclass
class RewardComponents:
    """Individual reward component breakdown"""
    accuracy: float = 0.0
    helpfulness: float = 0.0
    clarity: float = 0.0
    timeliness: float = 0.0
    consistency: float = 0.0
    total: float = 0.0


@dataclass
class RewardEvent:
    """Single reward calculation event"""
    timestamp: str
    session_id: str
    query: str
    domain: str
    feedback_type: str
    reward_components: RewardComponents
    confidence_before: float
    confidence_after: float
    learning_rate: float
    impact_score: float


class RewardEngine:
    """
    Feedback value calculator with reinforcement scoring.
    
    This is the main reward_engine.py module required for Task 2.
    Calculates multi-dimensional rewards for agent learning.
    """

    def __init__(self, 
                 reward_weights: Optional[Dict[str, float]] = None,
                 learning_rate: float = 0.1,
                 reward_history_file: str = "reward_history.json"):
        """Initialize reward engine"""
        
        # Default reward weights (must sum to 1.0)
        self.reward_weights = reward_weights or {
            'accuracy': 0.30,      # Domain classification accuracy
            'helpfulness': 0.25,   # Route/advice helpfulness  
            'clarity': 0.20,       # Response clarity
            'timeliness': 0.15,    # Response speed
            'consistency': 0.10    # Consistency with past responses
        }
        
        # Validate weights sum to 1.0
        weight_sum = sum(self.reward_weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            logger.warning(f"Reward weights sum to {weight_sum:.3f}, should be 1.0")
            # Normalize weights
            for key in self.reward_weights:
                self.reward_weights[key] /= weight_sum
        
        self.base_learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.reward_history_file = reward_history_file
        
        # Reward calculation state
        self.reward_history: List[RewardEvent] = []
        self.recent_rewards = deque(maxlen=20)  # Last 20 rewards for trend analysis
        
        # Performance tracking
        self.performance_metrics = {
            'total_rewards_calculated': 0,
            'average_reward': 0.0,
            'reward_trend': 0.0,
            'learning_rate_adjustments': 0
        }
        
        # Feedback type mapping to base reward
        self.feedback_base_rewards = {
            'positive': 0.8,       # "helpful", "good", "thank you"
            'negative': 0.2,       # "not helpful", "wrong", "bad"
            'clarification': 0.6,  # "explain", "clarify", "more details"
            'neutral': 0.5,        # Default/ambiguous feedback
            'satisfaction': 0.9,   # "satisfied", "complete", "done"
            'dissatisfaction': 0.1 # "useless", "terrible", "waste of time"
        }
        
        # Load existing reward history
        self.load_reward_history()
        
        logger.info(f"Reward engine initialized with weights: {self.reward_weights}")

    def calculate_reward(self, 
                        feedback_data: Dict[str, Any],
                        agent_response: Any,
                        context_data: Optional[Dict[str, Any]] = None) -> Tuple[float, RewardComponents]:
        """
        Calculate multi-dimensional reward based on feedback and performance.
        
        Args:
            feedback_data: Feedback information including type, text, satisfaction
            agent_response: Agent's response being evaluated
            context_data: Additional context (response time, previous responses, etc.)
            
        Returns:
            Tuple of (total_reward, reward_components)
        """
        
        context_data = context_data or {}
        
        # Initialize reward components
        components = RewardComponents()
        
        # 1. Calculate accuracy reward (30%)
        components.accuracy = self._calculate_accuracy_reward(
            feedback_data, agent_response, context_data
        )
        
        # 2. Calculate helpfulness reward (25%)
        components.helpfulness = self._calculate_helpfulness_reward(
            feedback_data, agent_response, context_data
        )
        
        # 3. Calculate clarity reward (20%)
        components.clarity = self._calculate_clarity_reward(
            feedback_data, agent_response, context_data
        )
        
        # 4. Calculate timeliness reward (15%)
        components.timeliness = self._calculate_timeliness_reward(
            feedback_data, agent_response, context_data
        )
        
        # 5. Calculate consistency reward (10%)
        components.consistency = self._calculate_consistency_reward(
            feedback_data, agent_response, context_data
        )
        
        # Calculate weighted total reward
        components.total = (
            components.accuracy * self.reward_weights['accuracy'] +
            components.helpfulness * self.reward_weights['helpfulness'] +
            components.clarity * self.reward_weights['clarity'] +
            components.timeliness * self.reward_weights['timeliness'] +
            components.consistency * self.reward_weights['consistency']
        )
        
        # Apply learning rate and create reward event
        self._record_reward_event(feedback_data, agent_response, components, context_data)
        
        # Update performance metrics
        self._update_performance_metrics(components.total)
        
        # Adjust learning rate based on performance trends
        self._adjust_learning_rate()
        
        logger.info(f"Calculated reward: {components.total:.3f} (accuracy: {components.accuracy:.3f}, helpfulness: {components.helpfulness:.3f})")
        
        return components.total, components

    def _calculate_accuracy_reward(self, 
                                 feedback_data: Dict[str, Any],
                                 agent_response: Any,
                                 context_data: Dict[str, Any]) -> float:
        """Calculate accuracy component (30% weight)"""
        
        feedback_type = feedback_data.get('type', 'neutral')
        base_reward = self.feedback_base_rewards.get(feedback_type, 0.5)
        
        # Confidence-based adjustment
        confidence = getattr(agent_response, 'confidence', 0.5)
        confidence_bonus = 0.0
        
        if feedback_type == 'positive' and confidence > 0.7:
            confidence_bonus = 0.2  # High confidence + positive feedback
        elif feedback_type == 'negative' and confidence < 0.4:
            confidence_bonus = 0.1  # Low confidence + negative feedback (agent was cautious)
        elif feedback_type == 'negative' and confidence > 0.8:
            confidence_bonus = -0.3  # High confidence + negative feedback (overconfident)
        
        # Domain consistency check
        domain_consistency_bonus = 0.0
        previous_domain = context_data.get('previous_domain')
        current_domain = getattr(agent_response, 'domain', 'unknown')
        
        if previous_domain and current_domain == previous_domain:
            domain_consistency_bonus = 0.1
        elif previous_domain and current_domain != previous_domain and feedback_type == 'positive':
            domain_consistency_bonus = 0.15  # Good domain change
        
        accuracy_reward = base_reward + confidence_bonus + domain_consistency_bonus
        return np.clip(accuracy_reward, 0.0, 1.0)

    def _calculate_helpfulness_reward(self, 
                                    feedback_data: Dict[str, Any],
                                    agent_response: Any,
                                    context_data: Dict[str, Any]) -> float:
        """Calculate helpfulness component (25% weight)"""
        
        feedback_text = feedback_data.get('text', '').lower()
        feedback_type = feedback_data.get('type', 'neutral')
        
        base_reward = self.feedback_base_rewards.get(feedback_type, 0.5)
        
        # Text analysis for helpfulness indicators
        helpfulness_indicators = {
            'positive': ['helpful', 'useful', 'clear', 'good', 'excellent', 'perfect', 'exactly'],
            'negative': ['useless', 'unhelpful', 'confusing', 'wrong', 'bad', 'terrible'],
            'actionable': ['steps', 'process', 'action', 'do', 'contact', 'file', 'approach']
        }
        
        helpfulness_bonus = 0.0
        
        for indicator_type, words in helpfulness_indicators.items():
            matches = sum(1 for word in words if word in feedback_text)
            
            if indicator_type == 'positive' and matches > 0:
                helpfulness_bonus += matches * 0.1
            elif indicator_type == 'negative' and matches > 0:
                helpfulness_bonus -= matches * 0.15
            elif indicator_type == 'actionable' and matches > 0:
                helpfulness_bonus += matches * 0.05
        
        # Route quality assessment
        route_quality_bonus = 0.0
        legal_route = getattr(agent_response, 'legal_route', '')
        
        if legal_route and len(legal_route) > 50:  # Detailed route
            route_quality_bonus = 0.1
        
        # Timeline specificity bonus
        timeline = getattr(agent_response, 'timeline', '')
        if timeline and any(word in timeline.lower() for word in ['days', 'months', 'weeks']):
            route_quality_bonus += 0.05
        
        helpfulness_reward = base_reward + helpfulness_bonus + route_quality_bonus
        return np.clip(helpfulness_reward, 0.0, 1.0)

    def _calculate_clarity_reward(self, 
                                feedback_data: Dict[str, Any],
                                agent_response: Any,
                                context_data: Dict[str, Any]) -> float:
        """Calculate clarity component (20% weight)"""
        
        feedback_text = feedback_data.get('text', '').lower()
        feedback_type = feedback_data.get('type', 'neutral')
        
        base_reward = self.feedback_base_rewards.get(feedback_type, 0.5)
        
        # Clarity indicators in feedback
        clarity_indicators = {
            'clear': ['clear', 'understandable', 'simple', 'easy', 'straightforward'],
            'unclear': ['confusing', 'unclear', 'complicated', 'hard to understand', 'complex'],
            'explanation': ['explain', 'clarify', 'elaborate', 'more details', 'breakdown']
        }
        
        clarity_bonus = 0.0
        
        for indicator_type, words in clarity_indicators.items():
            matches = sum(1 for word in words if word in feedback_text)
            
            if indicator_type == 'clear' and matches > 0:
                clarity_bonus += matches * 0.15
            elif indicator_type == 'unclear' and matches > 0:
                clarity_bonus -= matches * 0.2
            elif indicator_type == 'explanation' and feedback_type == 'clarification':
                clarity_bonus += matches * 0.1  # Clarification requests show engagement
        
        # Response length and structure bonus
        structure_bonus = 0.0
        legal_route = getattr(agent_response, 'legal_route', '')
        
        if legal_route:
            # Well-structured responses get bonus
            if any(indicator in legal_route.lower() for indicator in ['step', 'first', 'then', 'next', 'finally']):
                structure_bonus = 0.1
            
            # Appropriate length (not too short, not too long)
            if 100 <= len(legal_route) <= 500:
                structure_bonus += 0.05
        
        clarity_reward = base_reward + clarity_bonus + structure_bonus
        return np.clip(clarity_reward, 0.0, 1.0)

    def _calculate_timeliness_reward(self, 
                                   feedback_data: Dict[str, Any],
                                   agent_response: Any,
                                   context_data: Dict[str, Any]) -> float:
        """Calculate timeliness component (15% weight)"""
        
        feedback_type = feedback_data.get('type', 'neutral')
        base_reward = self.feedback_base_rewards.get(feedback_type, 0.5)
        
        # Response time bonus/penalty
        response_time = context_data.get('response_time', 1.0)
        time_bonus = 0.0
        
        if response_time < 0.5:  # Very fast response
            time_bonus = 0.2
        elif response_time < 1.0:  # Fast response
            time_bonus = 0.1
        elif response_time > 3.0:  # Slow response
            time_bonus = -0.1
        elif response_time > 5.0:  # Very slow response
            time_bonus = -0.2
        
        # Timeline accuracy in legal advice
        timeline_bonus = 0.0
        timeline = getattr(agent_response, 'timeline', '')
        
        if timeline:
            # Specific timelines get bonus
            if any(word in timeline.lower() for word in ['days', 'months', 'weeks']):
                timeline_bonus = 0.1
            
            # Realistic timelines get additional bonus
            if any(phrase in timeline.lower() for phrase in ['2-3 months', '30-90 days', '6 months']):
                timeline_bonus += 0.05
        
        timeliness_reward = base_reward + time_bonus + timeline_bonus
        return np.clip(timeliness_reward, 0.0, 1.0)

    def _calculate_consistency_reward(self, 
                                    feedback_data: Dict[str, Any],
                                    agent_response: Any,
                                    context_data: Dict[str, Any]) -> float:
        """Calculate consistency component (10% weight)"""
        
        feedback_type = feedback_data.get('type', 'neutral')
        base_reward = self.feedback_base_rewards.get(feedback_type, 0.5)
        
        consistency_bonus = 0.0
        
        # Domain consistency
        previous_domain = context_data.get('previous_domain')
        current_domain = getattr(agent_response, 'domain', 'unknown')
        
        if previous_domain:
            if current_domain == previous_domain:
                consistency_bonus += 0.15  # Consistent domain classification
            elif feedback_type == 'positive':
                consistency_bonus += 0.1   # Domain change but positive feedback
        
        # Confidence consistency
        previous_confidence = context_data.get('previous_confidence', 0.5)
        current_confidence = getattr(agent_response, 'confidence', 0.5)
        
        # Handle None values
        if previous_confidence is None:
            previous_confidence = 0.5
        if current_confidence is None:
            current_confidence = 0.5
        
        confidence_diff = abs(current_confidence - previous_confidence)
        
        if confidence_diff < 0.1:  # Small change
            consistency_bonus += 0.05
        elif confidence_diff > 0.5:  # Large change
            if feedback_type == 'positive':
                consistency_bonus += 0.1  # Large change but positive outcome
            else:
                consistency_bonus -= 0.1  # Large change with negative outcome
        
        # Route consistency (similar legal routes for similar issues)
        route_consistency_bonus = 0.0
        previous_route = context_data.get('previous_route', '')
        current_route = getattr(agent_response, 'legal_route', '')
        
        if previous_route and current_route:
            # Simple similarity check
            common_words = set(previous_route.lower().split()) & set(current_route.lower().split())
            similarity = len(common_words) / max(len(previous_route.split()), len(current_route.split()))
            
            if similarity > 0.3:  # Some similarity
                route_consistency_bonus = 0.05
        
        consistency_reward = base_reward + consistency_bonus + route_consistency_bonus
        return np.clip(consistency_reward, 0.0, 1.0)

    def _record_reward_event(self, 
                           feedback_data: Dict[str, Any],
                           agent_response: Any,
                           components: RewardComponents,
                           context_data: Dict[str, Any]):
        """Record reward calculation event"""
        
        event = RewardEvent(
            timestamp=datetime.datetime.now().isoformat(),
            session_id=context_data.get('session_id', 'unknown'),
            query=context_data.get('query', ''),
            domain=getattr(agent_response, 'domain', 'unknown'),
            feedback_type=feedback_data.get('type', 'neutral'),
            reward_components=components,
            confidence_before=context_data.get('confidence_before', 0.0),
            confidence_after=getattr(agent_response, 'confidence', 0.0),
            learning_rate=self.current_learning_rate,
            impact_score=components.total * self.current_learning_rate
        )
        
        self.reward_history.append(event)
        self.recent_rewards.append(components.total)
        
        # Keep history manageable
        if len(self.reward_history) > 1000:
            self.reward_history = self.reward_history[-800:]  # Keep last 800 events

    def _update_performance_metrics(self, reward: float):
        """Update performance tracking metrics"""
        
        self.performance_metrics['total_rewards_calculated'] += 1
        
        # Update average reward
        total_rewards = self.performance_metrics['total_rewards_calculated']
        old_avg = self.performance_metrics['average_reward']
        self.performance_metrics['average_reward'] = (old_avg * (total_rewards - 1) + reward) / total_rewards
        
        # Calculate reward trend (last 10 vs previous 10)
        if len(self.recent_rewards) >= 20:
            recent_10 = list(self.recent_rewards)[-10:]
            previous_10 = list(self.recent_rewards)[-20:-10]
            
            recent_avg = sum(recent_10) / len(recent_10)
            previous_avg = sum(previous_10) / len(previous_10)
            
            self.performance_metrics['reward_trend'] = recent_avg - previous_avg

    def _adjust_learning_rate(self):
        """Adjust learning rate based on performance trends"""
        
        if len(self.recent_rewards) < 10:
            return
        
        # Calculate performance trend
        trend = self.performance_metrics.get('reward_trend', 0.0)
        
        # Adjust learning rate based on trend
        if trend > 0.1:  # Improving performance
            # Slightly reduce learning rate to maintain stability
            self.current_learning_rate *= 0.95
            self.performance_metrics['learning_rate_adjustments'] += 1
        elif trend < -0.1:  # Declining performance
            # Increase learning rate to adapt faster
            self.current_learning_rate *= 1.1
            self.performance_metrics['learning_rate_adjustments'] += 1
        
        # Keep learning rate within reasonable bounds
        self.current_learning_rate = np.clip(
            self.current_learning_rate, 
            self.base_learning_rate * 0.1,  # Minimum 10% of base
            self.base_learning_rate * 2.0   # Maximum 200% of base
        )

    def get_confidence_adjustment(self, reward: float) -> float:
        """Calculate confidence adjustment based on reward"""
        
        # Scale reward to confidence adjustment
        # Reward range [0, 1] -> Adjustment range [-0.3, +0.3]
        base_adjustment = (reward - 0.5) * 0.6
        
        # Apply learning rate
        adjustment = base_adjustment * self.current_learning_rate
        
        return np.clip(adjustment, -0.3, 0.3)

    def get_reward_statistics(self) -> Dict[str, Any]:
        """Get reward engine statistics"""
        
        recent_rewards_list = list(self.recent_rewards)
        
        return {
            **self.performance_metrics,
            'current_learning_rate': self.current_learning_rate,
            'base_learning_rate': self.base_learning_rate,
            'reward_weights': self.reward_weights,
            'recent_rewards': recent_rewards_list,
            'reward_history_length': len(self.reward_history),
            'recent_average': sum(recent_rewards_list) / len(recent_rewards_list) if recent_rewards_list else 0.0
        }

    def get_reward_breakdown(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get detailed breakdown of recent rewards"""
        
        recent_events = self.reward_history[-limit:] if self.reward_history else []
        
        breakdown = []
        for event in recent_events:
            breakdown.append({
                'timestamp': event.timestamp,
                'feedback_type': event.feedback_type,
                'domain': event.domain,
                'total_reward': event.reward_components.total,
                'accuracy': event.reward_components.accuracy,
                'helpfulness': event.reward_components.helpfulness,
                'clarity': event.reward_components.clarity,
                'timeliness': event.reward_components.timeliness,
                'consistency': event.reward_components.consistency,
                'confidence_change': event.confidence_after - event.confidence_before,
                'impact_score': event.impact_score
            })
        
        return breakdown

    def save_reward_history(self):
        """Save reward history to file"""
        
        try:
            # Convert reward events to serializable format
            history_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'performance_metrics': self.performance_metrics,
                'reward_weights': self.reward_weights,
                'current_learning_rate': self.current_learning_rate,
                'recent_rewards': list(self.recent_rewards),
                'reward_events': []
            }
            
            # Convert recent events (last 100)
            for event in self.reward_history[-100:]:
                event_dict = {
                    'timestamp': event.timestamp,
                    'session_id': event.session_id,
                    'query': event.query,
                    'domain': event.domain,
                    'feedback_type': event.feedback_type,
                    'reward_components': {
                        'accuracy': event.reward_components.accuracy,
                        'helpfulness': event.reward_components.helpfulness,
                        'clarity': event.reward_components.clarity,
                        'timeliness': event.reward_components.timeliness,
                        'consistency': event.reward_components.consistency,
                        'total': event.reward_components.total
                    },
                    'confidence_before': event.confidence_before,
                    'confidence_after': event.confidence_after,
                    'learning_rate': event.learning_rate,
                    'impact_score': event.impact_score
                }
                history_data['reward_events'].append(event_dict)
            
            with open(self.reward_history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved reward history with {len(history_data['reward_events'])} events")
            
        except Exception as e:
            logger.error(f"Error saving reward history: {e}")

    def load_reward_history(self):
        """Load reward history from file"""
        
        try:
            with open(self.reward_history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            # Load performance metrics
            if 'performance_metrics' in history_data:
                self.performance_metrics.update(history_data['performance_metrics'])
            
            # Load learning rate
            if 'current_learning_rate' in history_data:
                self.current_learning_rate = history_data['current_learning_rate']
            
            # Load recent rewards
            if 'recent_rewards' in history_data:
                self.recent_rewards = deque(history_data['recent_rewards'], maxlen=20)
            
            logger.info("Loaded reward history")
            
        except FileNotFoundError:
            logger.info("No existing reward history found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading reward history: {e}")


def create_reward_engine(learning_rate: float = 0.1) -> RewardEngine:
    """Factory function to create reward engine"""
    return RewardEngine(learning_rate=learning_rate)


# Test the reward engine
if __name__ == "__main__":
    print("🎁 REWARD ENGINE TEST")
    print("=" * 50)
    
    reward_engine = create_reward_engine()
    
    # Mock agent response
    class MockResponse:
        def __init__(self):
            self.domain = "tenant_rights"
            self.confidence = 0.75
            self.legal_route = "Send legal notice to landlord and approach rent tribunal if needed"
            self.timeline = "2-3 months"
    
    # Test different feedback types
    test_cases = [
        {
            'feedback_data': {'type': 'positive', 'text': 'very helpful and clear advice'},
            'context_data': {'response_time': 0.5, 'query': 'landlord deposit issue'}
        },
        {
            'feedback_data': {'type': 'negative', 'text': 'confusing and not helpful'},
            'context_data': {'response_time': 2.0, 'query': 'landlord deposit issue'}
        },
        {
            'feedback_data': {'type': 'clarification', 'text': 'can you explain the steps more clearly'},
            'context_data': {'response_time': 1.0, 'query': 'landlord deposit issue'}
        }
    ]
    
    agent_response = MockResponse()
    
    print("Testing reward calculations:")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        reward, components = reward_engine.calculate_reward(
            test_case['feedback_data'],
            agent_response,
            test_case['context_data']
        )
        
        print(f"\nTest {i}: {test_case['feedback_data']['type']} feedback")
        print(f"   Total Reward: {reward:.3f}")
        print(f"   Accuracy: {components.accuracy:.3f}")
        print(f"   Helpfulness: {components.helpfulness:.3f}")
        print(f"   Clarity: {components.clarity:.3f}")
        print(f"   Confidence Adjustment: {reward_engine.get_confidence_adjustment(reward):+.3f}")
    
    # Get statistics
    stats = reward_engine.get_reward_statistics()
    print(f"\nReward Engine Statistics:")
    print(f"   Total Rewards: {stats['total_rewards_calculated']}")
    print(f"   Average Reward: {stats['average_reward']:.3f}")
    print(f"   Current Learning Rate: {stats['current_learning_rate']:.3f}")
    print(f"   Reward Trend: {stats['reward_trend']:+.3f}")
    
    print("\n✅ Reward engine test completed successfully!")