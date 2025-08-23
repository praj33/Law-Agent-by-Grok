"""
Conversation Loop - Task 2 Implementation
========================================

This module handles multi-turn legal conversations (3-6 turns) with evolution tracking.
Implements the conversation_loop.py requirement for Task 2.

Features:
- Multi-turn dialogue management
- Learning detection (acknowledgment, clarification, dissatisfaction)
- Adaptive responses based on conversation context
- Context preservation across turns
- Evolution tracking for conversation improvement

Author: Legal Agent Team
Version: 3.0.0 (Task 2 - Conversation Loop)
Date: 2025-08-15
"""

import json
import datetime
import uuid
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

# Import base components
try:
    from legal_agent import LegalAgent, LegalQueryInput, LegalAgentResponse
    LEGAL_AGENT_AVAILABLE = True
except ImportError:
    LEGAL_AGENT_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Single conversation turn data"""
    turn_number: int
    user_input: str
    agent_response: Any  # LegalAgentResponse
    feedback: Optional[str] = None
    satisfaction_level: Optional[float] = None
    learning_events: List[Dict[str, Any]] = None
    timestamp: str = None

    def __post_init__(self):
        if self.learning_events is None:
            self.learning_events = []
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()


@dataclass
class ConversationSession:
    """Complete conversation session"""
    session_id: str
    start_time: str
    turns: List[ConversationTurn]
    total_turns: int = 0
    conversation_state: str = "active"  # active, satisfied, dissatisfied, ended
    learning_progress: Dict[str, float] = None
    context_evolution: Dict[str, Any] = None

    def __post_init__(self):
        if self.learning_progress is None:
            self.learning_progress = {
                'confidence_evolution': [],
                'satisfaction_trend': [],
                'learning_rate': 0.1
            }
        if self.context_evolution is None:
            self.context_evolution = {
                'domain_shifts': [],
                'strategy_changes': [],
                'improvement_indicators': []
            }


class ConversationLoop:
    """
    Multi-turn conversation handler with learning capabilities.
    
    This is the main conversation_loop.py module required for Task 2.
    Manages 3-6 turn conversations with adaptive learning.
    """

    def __init__(self, 
                 min_turns: int = 3,
                 max_turns: int = 6,
                 conversation_file: str = "conversation_history.json"):
        """Initialize conversation loop"""
        
        self.min_turns = min_turns
        self.max_turns = max_turns
        self.conversation_file = conversation_file
        
        # Active conversations
        self.active_conversations: Dict[str, ConversationSession] = {}
        
        # Conversation patterns and learning
        self.conversation_patterns = {
            'acknowledgment': ['thank you', 'helpful', 'good', 'thanks', 'useful', 'clear'],
            'clarification': ['what', 'how', 'explain', 'clarify', 'more details', 'elaborate'],
            'dissatisfaction': ['wrong', 'not helpful', 'bad', 'useless', 'unclear', 'confusing'],
            'satisfaction': ['satisfied', 'enough', 'complete', 'done', 'good enough']
        }
        
        # Learning statistics
        self.learning_stats = {
            'total_conversations': 0,
            'completed_conversations': 0,
            'average_turns': 0.0,
            'satisfaction_rate': 0.0,
            'learning_events': 0
        }
        
        # Load existing conversation history
        self.load_conversation_history()
        
        logger.info(f"Conversation loop initialized: {self.min_turns}-{self.max_turns} turns")

    def start_conversation(self, 
                          initial_query: str,
                          agent: Any,
                          session_id: Optional[str] = None) -> str:
        """
        Start a new conversation session.
        
        Args:
            initial_query: User's initial legal query
            agent: Legal agent instance
            session_id: Optional session ID (generated if not provided)
            
        Returns:
            session_id: Unique session identifier
        """
        
        if not session_id:
            session_id = self._generate_session_id()
        
        # Create conversation session
        session = ConversationSession(
            session_id=session_id,
            start_time=datetime.datetime.now().isoformat(),
            turns=[]
        )
        
        # Process initial query
        query_input = LegalQueryInput(
            user_input=initial_query,
            session_id=session_id
        )
        
        if hasattr(agent, 'process_query_with_learning'):
            # Use adaptive agent method
            response = agent.process_query_with_learning(query_input)
        else:
            # Use standard agent method  
            response = agent.process_query(query_input)
        
        # Create first turn
        first_turn = ConversationTurn(
            turn_number=1,
            user_input=initial_query,
            agent_response=response
        )
        
        session.turns.append(first_turn)
        session.total_turns = 1
        
        # Store session
        self.active_conversations[session_id] = session
        
        # Update statistics
        self.learning_stats['total_conversations'] += 1
        
        logger.info(f"Started conversation {session_id} with initial query")
        
        return session_id

    def continue_conversation(self,
                            session_id: str,
                            user_input: str,
                            agent: Any,
                            feedback_on_previous: Optional[str] = None) -> Tuple[Any, bool]:
        """
        Continue an existing conversation.
        
        Args:
            session_id: Session identifier
            user_input: User's next input
            agent: Legal agent instance
            feedback_on_previous: Optional feedback on previous response
            
        Returns:
            Tuple of (agent_response, should_end_conversation)
        """
        
        if session_id not in self.active_conversations:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_conversations[session_id]
        
        # Check if conversation should continue
        if session.total_turns >= self.max_turns:
            logger.info(f"Conversation {session_id} reached max turns, ending")
            self.end_conversation(session_id)
            return None, True
        
        # Process feedback on previous turn if provided
        if feedback_on_previous and session.turns:
            self._process_turn_feedback(session, feedback_on_previous)
        
        # Determine conversation intent
        conversation_intent = self._analyze_conversation_intent(user_input, session)
        
        # Check for satisfaction and early termination
        if self._should_end_conversation(conversation_intent, session):
            logger.info(f"Conversation {session_id} ending due to satisfaction")
            self.end_conversation(session_id)
            return session.turns[-1].agent_response, True
        
        # Process new query with adaptive context
        query_input = LegalQueryInput(
            user_input=user_input,
            session_id=session_id,
            feedback=feedback_on_previous
        )
        
        # Apply conversation context to agent processing
        if hasattr(agent, 'process_query_with_learning'):
            # Use adaptive agent method
            response = agent.process_query_with_learning(query_input)
        else:
            # Use standard agent method
            response = agent.process_query(query_input)
        
        # Create new turn
        new_turn = ConversationTurn(
            turn_number=session.total_turns + 1,
            user_input=user_input,
            agent_response=response,
            feedback=feedback_on_previous
        )
        
        # Analyze and record learning events
        learning_events = self._detect_learning_events(session, new_turn, conversation_intent)
        new_turn.learning_events = learning_events
        
        # Update session
        session.turns.append(new_turn)
        session.total_turns += 1
        
        # Update learning progress
        self._update_learning_progress(session, new_turn, conversation_intent)
        
        # Determine if conversation should end
        should_end = self._should_end_conversation(conversation_intent, session)
        
        if should_end:
            self.end_conversation(session_id)
        
        logger.info(f"Continued conversation {session_id}, turn {session.total_turns}")
        
        return response, should_end

    def end_conversation(self, session_id: str):
        """End a conversation and save to history"""
        
        if session_id not in self.active_conversations:
            return
        
        session = self.active_conversations[session_id]
        session.conversation_state = "ended"
        
        # Calculate final statistics
        self._calculate_conversation_statistics(session)
        
        # Save to history
        self.save_conversation_history()
        
        # Update global statistics
        self.learning_stats['completed_conversations'] += 1
        self._update_global_statistics()
        
        # Remove from active conversations
        del self.active_conversations[session_id]
        
        logger.info(f"Ended conversation {session_id} after {session.total_turns} turns")

    def _analyze_conversation_intent(self, user_input: str, session: ConversationSession) -> str:
        """Analyze the intent behind user's input"""
        
        user_input_lower = user_input.lower()
        
        # Check for different intent patterns
        for intent, patterns in self.conversation_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                return intent
        
        # Check for new query vs follow-up
        if len(session.turns) > 0:
            # Simple heuristic: if input is a question, it's likely clarification
            if any(word in user_input_lower for word in ['what', 'how', 'when', 'where', 'why', '?']):
                return 'clarification'
            # If it's a statement expressing satisfaction/dissatisfaction
            elif any(word in user_input_lower for word in ['thank', 'good', 'bad', 'wrong']):
                return 'acknowledgment' if any(word in user_input_lower for word in ['thank', 'good']) else 'dissatisfaction'
        
        # Default to new query
        return 'new_query'

    def _should_end_conversation(self, intent: str, session: ConversationSession) -> bool:
        """Determine if conversation should end"""
        
        # Always require minimum turns
        if session.total_turns < self.min_turns:
            return False
        
        # End on satisfaction
        if intent == 'satisfaction':
            return True
        
        # End if user seems satisfied (multiple acknowledgments)
        recent_intents = []
        for turn in session.turns[-2:]:  # Last 2 turns
            if turn.learning_events:
                for event in turn.learning_events:
                    if 'intent' in event:
                        recent_intents.append(event['intent'])
        
        if recent_intents.count('acknowledgment') >= 2:
            return True
        
        # End at max turns
        if session.total_turns >= self.max_turns:
            return True
        
        return False

    def _process_with_conversation_context(self, 
                                         query_input: LegalQueryInput, 
                                         agent: Any,
                                         session: ConversationSession) -> Any:
        """Process query with conversation context"""
        
        # Apply learning from conversation history
        if hasattr(agent, 'process_query_with_learning'):
            # Use adaptive agent if available
            return agent.process_query_with_learning(query_input)
        else:
            # Use standard agent
            return agent.process_query(query_input)

    def _detect_learning_events(self, 
                               session: ConversationSession,
                               current_turn: ConversationTurn,
                               intent: str) -> List[Dict[str, Any]]:
        """Detect and record learning events"""
        
        learning_events = []
        
        # Previous turn context
        previous_turn = session.turns[-1] if len(session.turns) > 1 else None
        
        # Intent-based learning events
        if intent == 'acknowledgment':
            learning_events.append({
                'type': 'positive_feedback',
                'intent': intent,
                'confidence_impact': +0.15,
                'description': 'User acknowledged helpfulness'
            })
        elif intent == 'dissatisfaction':
            learning_events.append({
                'type': 'negative_feedback',
                'intent': intent,
                'confidence_impact': -0.10,
                'description': 'User expressed dissatisfaction'
            })
        elif intent == 'clarification':
            learning_events.append({
                'type': 'clarification_request',
                'intent': intent,
                'confidence_impact': +0.05,
                'description': 'User engaged for more details'
            })
        
        # Domain consistency learning
        if previous_turn:
            current_domain = getattr(current_turn.agent_response, 'domain', 'unknown')
            previous_domain = getattr(previous_turn.agent_response, 'domain', 'unknown')
            
            if current_domain != previous_domain:
                learning_events.append({
                    'type': 'domain_shift',
                    'intent': intent,
                    'from_domain': previous_domain,
                    'to_domain': current_domain,
                    'description': f'Domain changed from {previous_domain} to {current_domain}'
                })
        
        # Confidence evolution tracking
        if previous_turn:
            current_confidence = getattr(current_turn.agent_response, 'confidence', 0.0)
            previous_confidence = getattr(previous_turn.agent_response, 'confidence', 0.0)
            
            confidence_change = current_confidence - previous_confidence
            if abs(confidence_change) > 0.05:  # Significant change
                learning_events.append({
                    'type': 'confidence_evolution',
                    'intent': intent,
                    'confidence_change': confidence_change,
                    'description': f'Confidence changed by {confidence_change:+.3f}'
                })
        
        return learning_events

    def _update_learning_progress(self, 
                                session: ConversationSession,
                                current_turn: ConversationTurn,
                                intent: str):
        """Update learning progress for the session"""
        
        # Update confidence evolution
        current_confidence = getattr(current_turn.agent_response, 'confidence', 0.0)
        session.learning_progress['confidence_evolution'].append(current_confidence)
        
        # Update satisfaction trend
        satisfaction_score = self._calculate_satisfaction_score(intent)
        session.learning_progress['satisfaction_trend'].append(satisfaction_score)
        
        # Update context evolution
        if current_turn.learning_events:
            for event in current_turn.learning_events:
                if event['type'] == 'domain_shift':
                    session.context_evolution['domain_shifts'].append(event)
                elif abs(event.get('confidence_impact', 0)) > 0.1:
                    session.context_evolution['improvement_indicators'].append(event)
        
        # Adaptive learning rate adjustment
        if len(session.learning_progress['satisfaction_trend']) >= 3:
            recent_satisfaction = session.learning_progress['satisfaction_trend'][-3:]
            if all(score >= 0.5 for score in recent_satisfaction):
                # Reduce learning rate if consistently satisfied
                session.learning_progress['learning_rate'] *= 0.9
            elif all(score < 0.3 for score in recent_satisfaction):
                # Increase learning rate if consistently dissatisfied
                session.learning_progress['learning_rate'] *= 1.1
        
        # Update global learning statistics
        self.learning_stats['learning_events'] += len(current_turn.learning_events)

    def _process_turn_feedback(self, session: ConversationSession, feedback: str):
        """Process feedback on previous turn"""
        
        if not session.turns:
            return
        
        last_turn = session.turns[-1]
        last_turn.feedback = feedback
        
        # Calculate satisfaction level
        satisfaction = self._calculate_satisfaction_score(
            self._analyze_conversation_intent(feedback, session)
        )
        last_turn.satisfaction_level = satisfaction

    def _calculate_satisfaction_score(self, intent: str) -> float:
        """Calculate satisfaction score from intent"""
        
        satisfaction_mapping = {
            'acknowledgment': 0.8,
            'satisfaction': 1.0,
            'clarification': 0.6,
            'dissatisfaction': 0.2,
            'new_query': 0.5
        }
        
        return satisfaction_mapping.get(intent, 0.5)

    def _calculate_conversation_statistics(self, session: ConversationSession):
        """Calculate final statistics for completed conversation"""
        
        if not session.turns:
            return
        
        # Calculate average satisfaction
        satisfactions = []
        for turn in session.turns:
            if turn.satisfaction_level is not None:
                satisfactions.append(turn.satisfaction_level)
        
        if satisfactions:
            avg_satisfaction = sum(satisfactions) / len(satisfactions)
            session.conversation_state = "satisfied" if avg_satisfaction >= 0.6 else "dissatisfied"

    def _update_global_statistics(self):
        """Update global learning statistics"""
        
        if self.learning_stats['completed_conversations'] > 0:
            # Calculate average turns from completed conversations
            total_turns = 0
            satisfied_count = 0
            
            # This would ideally load from conversation history
            # For now, use active conversation data
            for session in self.active_conversations.values():
                total_turns += session.total_turns
                if session.conversation_state == "satisfied":
                    satisfied_count += 1
            
            if self.learning_stats['completed_conversations'] > 0:
                self.learning_stats['average_turns'] = total_turns / self.learning_stats['completed_conversations']
                self.learning_stats['satisfaction_rate'] = satisfied_count / self.learning_stats['completed_conversations']

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"conv_{timestamp}_{unique_id}"

    def get_conversation_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a conversation"""
        
        if session_id not in self.active_conversations:
            return None
        
        session = self.active_conversations[session_id]
        
        return {
            'session_id': session_id,
            'turns': session.total_turns,
            'state': session.conversation_state,
            'learning_events': sum(len(turn.learning_events) for turn in session.turns),
            'confidence_trend': session.learning_progress['confidence_evolution'],
            'satisfaction_trend': session.learning_progress['satisfaction_trend']
        }

    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get overall learning statistics"""
        
        return {
            **self.learning_stats,
            'active_conversations': len(self.active_conversations),
            'conversation_settings': {
                'min_turns': self.min_turns,
                'max_turns': self.max_turns
            }
        }

    def save_conversation_history(self):
        """Save conversation history to file"""
        
        try:
            # Convert active conversations to serializable format
            history_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'statistics': self.learning_stats,
                'active_conversations': {}
            }
            
            for session_id, session in self.active_conversations.items():
                # Convert session to dictionary
                session_dict = asdict(session)
                
                # Convert agent responses to serializable format
                for turn_dict in session_dict['turns']:
                    if hasattr(turn_dict['agent_response'], '__dict__'):
                        turn_dict['agent_response'] = {
                            'domain': getattr(turn_dict['agent_response'], 'domain', 'unknown'),
                            'confidence': getattr(turn_dict['agent_response'], 'confidence', 0.0),
                            'legal_route': getattr(turn_dict['agent_response'], 'legal_route', ''),
                            'timeline': getattr(turn_dict['agent_response'], 'timeline', '')
                        }
                
                history_data['active_conversations'][session_id] = session_dict
            
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved conversation history with {len(self.active_conversations)} sessions")
            
        except Exception as e:
            logger.error(f"Error saving conversation history: {e}")

    def load_conversation_history(self):
        """Load conversation history from file"""
        
        try:
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            # Load statistics
            if 'statistics' in history_data:
                self.learning_stats.update(history_data['statistics'])
            
            logger.info("Loaded conversation history")
            
        except FileNotFoundError:
            logger.info("No existing conversation history found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading conversation history: {e}")


def create_conversation_loop(min_turns: int = 3, max_turns: int = 6) -> ConversationLoop:
    """Factory function to create conversation loop"""
    return ConversationLoop(min_turns=min_turns, max_turns=max_turns)


# Test the conversation loop
if __name__ == "__main__":
    print("🔄 CONVERSATION LOOP TEST")
    print("=" * 50)
    
    try:
        from legal_agent import create_legal_agent
        
        conversation_loop = create_conversation_loop()
        agent = create_legal_agent()
        
        # Start test conversation
        session_id = conversation_loop.start_conversation(
            "my landlord is not returning my security deposit",
            agent
        )
        
        print(f"Started conversation: {session_id}")
        
        # Continue conversation
        response1, should_end1 = conversation_loop.continue_conversation(
            session_id,
            "what legal action can I take",
            agent,
            feedback_on_previous="helpful"
        )
        
        print(f"Turn 2 completed, should_end: {should_end1}")
        
        # Final turn
        response2, should_end2 = conversation_loop.continue_conversation(
            session_id,
            "thank you for the advice",
            agent,
            feedback_on_previous="very helpful"
        )
        
        print(f"Turn 3 completed, should_end: {should_end2}")
        
        # Get conversation status
        status = conversation_loop.get_conversation_status(session_id)
        print(f"Conversation status: {status}")
        
        # Get learning statistics
        stats = conversation_loop.get_learning_statistics()
        print(f"Learning stats: {stats}")
        
        print("✅ Conversation loop test completed successfully!")
        
    except ImportError as e:
        print(f"❌ Test requires legal_agent module: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")