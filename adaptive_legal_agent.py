"""
Adaptive Legal Agent - Self-Training Version
===========================================

This enhanced version learns from user feedback and adapts its responses.
Features:
- Feedback-based learning
- Dynamic confidence adjustment
- Response improvement over time
- Negative feedback handling

Author: Legal Agent Team
Version: 2.1.0 (Self-Training)
Date: 2025-07-22
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import pickle
import os

from legal_agent import (
    LegalQueryInput, LegalAgentResponse, DomainClassifier, 
    LegalRouteEngine, ProcessExplainer, GlossaryEngine, FeedbackSystem
)

try:
    from data_integration import CrimeDataAnalyzer, EnhancedLegalRouteEngine, create_enhanced_legal_system
    from enhanced_data_integration import EnhancedCrimeDataAnalyzer, create_enhanced_legal_system as create_enhanced_system
    DATA_INTEGRATION_AVAILABLE = True
    ENHANCED_DATA_INTEGRATION_AVAILABLE = True
except ImportError:
    DATA_INTEGRATION_AVAILABLE = False
    ENHANCED_DATA_INTEGRATION_AVAILABLE = False


class AdaptiveDomainClassifier(DomainClassifier):
    """Enhanced classifier that learns from feedback"""
    
    def __init__(self):
        super().__init__()
        self.feedback_weights = defaultdict(float)  # Query -> weight adjustment
        self.negative_feedback_queries = []  # Queries with negative feedback
        self.positive_feedback_queries = []  # Queries with positive feedback
        self.confidence_adjustments = defaultdict(float)  # Domain -> confidence adjustment
        
        # Load previous learning if available
        self.load_learning_data()
    
    def classify_with_learning(self, user_query: str, previous_feedback: Optional[str] = None) -> Tuple[str, float]:
        """Enhanced classification that considers feedback history"""
        
        # Get base classification
        domain, confidence = self.classify(user_query)
        
        # Apply learning adjustments
        adjusted_confidence = self.apply_feedback_learning(user_query, domain, confidence)
        
        # Check if this query had negative feedback before
        if self.has_negative_feedback_history(user_query):
            # Try alternative classification
            alternative_domain, alternative_confidence = self.get_alternative_classification(user_query)
            
            if alternative_confidence > adjusted_confidence:
                print(f"🧠 Learning: Switching from {domain} to {alternative_domain} based on feedback history")
                return alternative_domain, alternative_confidence
        
        return domain, adjusted_confidence
    
    def apply_feedback_learning(self, query: str, domain: str, base_confidence: float) -> float:
        """Apply learned adjustments from feedback"""
        
        # Domain-level confidence adjustment
        domain_adjustment = self.confidence_adjustments.get(domain, 0.0)
        
        # Query-specific adjustment
        query_adjustment = self.feedback_weights.get(query.lower().strip(), 0.0)
        
        # Calculate adjusted confidence
        adjusted_confidence = base_confidence + domain_adjustment + query_adjustment
        
        # Keep within valid range [0, 1]
        adjusted_confidence = max(0.0, min(1.0, adjusted_confidence))
        
        return adjusted_confidence
    
    def get_alternative_classification(self, user_query: str) -> Tuple[str, float]:
        """Get alternative classification for queries with negative feedback"""
        
        cleaned_query = self._clean_query(user_query)
        user_vec = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(user_vec, self.X)
        
        # Get top 3 matches instead of just the best
        top_indices = similarities[0].argsort()[-3:][::-1]
        
        for idx in top_indices[1:]:  # Skip the first (original) match
            alternative_domain = self.domain_data['domain'].iloc[idx]
            alternative_confidence = float(similarities[0][idx])
            
            # Boost confidence for alternative if original had negative feedback
            if alternative_confidence > 0.1:  # Minimum threshold
                boosted_confidence = min(1.0, alternative_confidence * 1.5)
                return alternative_domain, boosted_confidence
        
        # Fallback to unknown with moderate confidence
        return "unknown", 0.3
    
    def has_negative_feedback_history(self, query: str) -> bool:
        """Check if query has negative feedback history"""
        query_normalized = query.lower().strip()
        return any(query_normalized in neg_query.lower() for neg_query in self.negative_feedback_queries)
    
    def learn_from_feedback(self, query: str, domain: str, feedback: str, confidence: float):
        """Learn from user feedback and adjust future responses"""
        
        query_normalized = query.lower().strip()
        is_positive = self.is_positive_feedback(feedback)
        
        print(f"🧠 Learning from feedback: '{feedback}' for {domain} query")
        
        if is_positive:
            # Positive feedback - reinforce this classification
            self.positive_feedback_queries.append(query_normalized)
            self.confidence_adjustments[domain] += 0.05  # Boost domain confidence
            self.feedback_weights[query_normalized] += 0.1  # Boost query confidence
            
            print(f"✅ Reinforced {domain} classification (confidence boost: +0.05)")
            
        else:
            # Negative feedback - penalize this classification
            self.negative_feedback_queries.append(query_normalized)
            self.confidence_adjustments[domain] -= 0.05  # Reduce domain confidence
            self.feedback_weights[query_normalized] -= 0.1  # Reduce query confidence
            
            # Add training example for better classification
            self.add_negative_example(query, domain)
            
            print(f"❌ Penalized {domain} classification (confidence reduction: -0.05)")
            print(f"🔄 Added negative training example")
        
        # Save learning data
        self.save_learning_data()
    
    def is_positive_feedback(self, feedback: str) -> bool:
        """Determine if feedback is positive"""
        positive_keywords = ['helpful', 'good', 'great', 'excellent', 'useful', 'correct', 'yes', 'perfect']
        negative_keywords = ['not helpful', 'bad', 'wrong', 'useless', 'incorrect', 'no', 'terrible']
        
        feedback_lower = feedback.lower()
        
        # Check for explicit negative phrases first
        if any(neg in feedback_lower for neg in negative_keywords):
            return False
        
        # Check for positive keywords
        if any(pos in feedback_lower for pos in positive_keywords):
            return True
        
        # Default to negative if unclear
        return False
    
    def add_negative_example(self, query: str, wrong_domain: str):
        """Add negative training example to improve future classification"""
        
        # Find the most likely correct domain based on similarity to other domains
        cleaned_query = self._clean_query(query)
        user_vec = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(user_vec, self.X)
        
        # Get alternative domains (excluding the wrong one)
        domain_scores = []
        for i, domain in enumerate(self.domain_data['domain']):
            if domain != wrong_domain:
                domain_scores.append((domain, similarities[0][i]))
        
        # Sort by similarity and pick the best alternative
        domain_scores.sort(key=lambda x: x[1], reverse=True)
        
        if domain_scores and domain_scores[0][1] > 0.1:
            likely_correct_domain = domain_scores[0][0]
            
            # Add this as a training example
            self.add_training_example(likely_correct_domain, query)
            print(f"🎯 Added training example: '{query}' → {likely_correct_domain}")
    
    def save_learning_data(self):
        """Save learning data to file"""
        learning_data = {
            'feedback_weights': dict(self.feedback_weights),
            'confidence_adjustments': dict(self.confidence_adjustments),
            'negative_feedback_queries': self.negative_feedback_queries,
            'positive_feedback_queries': self.positive_feedback_queries
        }
        
        try:
            with open('learning_data.json', 'w') as f:
                json.dump(learning_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save learning data: {e}")
    
    def load_learning_data(self):
        """Load previous learning data"""
        try:
            if os.path.exists('learning_data.json'):
                with open('learning_data.json', 'r') as f:
                    learning_data = json.load(f)
                
                self.feedback_weights = defaultdict(float, learning_data.get('feedback_weights', {}))
                self.confidence_adjustments = defaultdict(float, learning_data.get('confidence_adjustments', {}))
                self.negative_feedback_queries = learning_data.get('negative_feedback_queries', [])
                self.positive_feedback_queries = learning_data.get('positive_feedback_queries', [])
                
                print(f"🧠 Loaded learning data: {len(self.negative_feedback_queries)} negative, {len(self.positive_feedback_queries)} positive examples")
        except Exception as e:
            print(f"Warning: Could not load learning data: {e}")


class AdaptiveLegalAgent:
    """Self-training legal agent that learns from feedback"""
    
    def __init__(self, feedback_file: str = 'feedback.csv', enable_data_integration: bool = True):
        """Initialize the adaptive legal agent"""
        
        # Use adaptive classifier instead of basic one
        self.domain_classifier = AdaptiveDomainClassifier()
        self.route_engine = LegalRouteEngine()
        self.process_explainer = ProcessExplainer()
        self.glossary_engine = GlossaryEngine()
        self.feedback_system = FeedbackSystem(feedback_file)
        
        # Enhanced data integration
        self.data_integration_enabled = False
        self.enhanced_data_integration_enabled = False
        self.crime_analyzer = None
        self.enhanced_crime_analyzer = None
        self.enhanced_route_engine = None

        if enable_data_integration:
            # Try enhanced data integration first (with all 3 JSON files)
            if ENHANCED_DATA_INTEGRATION_AVAILABLE:
                try:
                    self.enhanced_crime_analyzer = create_enhanced_system()
                    self.enhanced_data_integration_enabled = True
                    print("✅ Adaptive agent with ENHANCED data integration enabled (3 datasets)")
                except Exception as e:
                    print(f"⚠️ Enhanced data integration failed: {e}")

            # Fallback to basic data integration
            if not self.enhanced_data_integration_enabled and DATA_INTEGRATION_AVAILABLE:
                try:
                    self.crime_analyzer, self.enhanced_route_engine = create_enhanced_legal_system()
                    self.data_integration_enabled = True
                    print("✅ Adaptive agent with basic data integration enabled")
                except Exception as e:
                    print(f"⚠️ Basic data integration failed: {e}")
        
        # Learning statistics
        self.learning_stats = {
            'total_feedback_processed': 0,
            'positive_feedback_count': 0,
            'negative_feedback_count': 0,
            'classifications_improved': 0
        }
    
    def process_query_with_learning(self, query_input: LegalQueryInput) -> LegalAgentResponse:
        """Process query with adaptive learning"""
        
        # Generate session ID and timestamp
        session_id = query_input.session_id or self._generate_session_id()
        timestamp = query_input.timestamp or datetime.datetime.now().isoformat()
        
        # Extract location
        location = self.domain_classifier.extract_location(query_input.user_input)
        
        # Use adaptive classification
        domain, confidence = self.domain_classifier.classify_with_learning(
            query_input.user_input, 
            query_input.feedback
        )
        
        # Process feedback BEFORE generating response (for learning)
        if query_input.feedback:
            self.process_feedback_learning(query_input.user_input, domain, query_input.feedback, confidence)
        
        # Get legal route (enhanced if available)
        if self.data_integration_enabled and domain in ['elder abuse', 'criminal law']:
            route = self.enhanced_route_engine.get_enhanced_route(domain, location, query_input.user_input)
        else:
            route = self.route_engine.get_route(domain)
        
        # Get process steps
        process_steps = self.process_explainer.get_process_steps(domain)
        
        # Find glossary terms
        combined_text = query_input.user_input + ' ' + route['summary']
        glossary = self.glossary_engine.find_terms(combined_text)
        
        # Get enhanced location insights
        location_insights = None
        data_driven_advice = None
        risk_assessment = None

        if location and ('senior' in query_input.user_input.lower() or 'elder' in query_input.user_input.lower()):
            if self.enhanced_data_integration_enabled:
                # Use enhanced data integration (3 datasets)
                location_insights = self.enhanced_crime_analyzer.get_comprehensive_location_advice(location, 'senior_citizen_abuse')
                if location_insights.get('location_found'):
                    data_driven_advice = location_insights['advice']
                    risk_assessment = location_insights['risk_level']
            elif self.data_integration_enabled:
                # Fallback to basic data integration
                location_insights = self.crime_analyzer.get_location_based_advice(location, 'senior_citizen_abuse')
                if location_insights.get('location_found'):
                    data_driven_advice = location_insights['advice']
                    risk_assessment = location_insights['risk_level']
        
        # Store feedback
        if query_input.feedback:
            self.feedback_system.collect_feedback(
                query_input.user_input,
                domain,
                query_input.feedback,
                session_id
            )
        
        # Create response
        response = LegalAgentResponse(
            domain=domain,
            confidence=confidence,
            legal_route=route['summary'],
            timeline=route['timeline'],
            outcome=route['outcome'],
            process_steps=process_steps,
            glossary=glossary,
            session_id=session_id,
            timestamp=timestamp,
            raw_query=query_input.user_input,
            location_insights=location_insights,
            data_driven_advice=data_driven_advice,
            risk_assessment=risk_assessment
        )
        
        return response
    
    def process_feedback_learning(self, query: str, domain: str, feedback: str, confidence: float):
        """Process feedback for learning"""
        
        # Let the classifier learn from this feedback
        self.domain_classifier.learn_from_feedback(query, domain, feedback, confidence)
        
        # Update learning statistics
        self.learning_stats['total_feedback_processed'] += 1
        
        if self.domain_classifier.is_positive_feedback(feedback):
            self.learning_stats['positive_feedback_count'] += 1
        else:
            self.learning_stats['negative_feedback_count'] += 1
            self.learning_stats['classifications_improved'] += 1
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            **self.learning_stats,
            'learning_data_size': len(self.domain_classifier.negative_feedback_queries) + len(self.domain_classifier.positive_feedback_queries),
            'confidence_adjustments': dict(self.domain_classifier.confidence_adjustments),
            'domains_with_adjustments': len(self.domain_classifier.confidence_adjustments)
        }
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = np.random.randint(1000, 9999)
        return f"adaptive_session_{timestamp}_{random_suffix}"


# Factory function
def create_adaptive_legal_agent(feedback_file: str = 'feedback.csv') -> AdaptiveLegalAgent:
    """Create adaptive legal agent"""
    return AdaptiveLegalAgent(feedback_file)


if __name__ == "__main__":
    # Demo adaptive learning
    print("🧠 ADAPTIVE LEGAL AGENT - SELF-TRAINING DEMO")
    print("=" * 50)
    
    agent = create_adaptive_legal_agent()
    
    # Test query
    print("\n1. Initial Query:")
    query1 = LegalQueryInput(user_input="My landlord won't return deposit")
    response1 = agent.process_query_with_learning(query1)
    print(f"Domain: {response1.domain}, Confidence: {response1.confidence:.2f}")
    
    # Negative feedback
    print("\n2. Negative Feedback:")
    query2 = LegalQueryInput(
        user_input="My landlord won't return deposit",
        feedback="not helpful, this is wrong domain"
    )
    response2 = agent.process_query_with_learning(query2)
    print(f"After negative feedback - Domain: {response2.domain}, Confidence: {response2.confidence:.2f}")
    
    # Same query again - should be different
    print("\n3. Same Query After Learning:")
    query3 = LegalQueryInput(user_input="My landlord won't return deposit")
    response3 = agent.process_query_with_learning(query3)
    print(f"After learning - Domain: {response3.domain}, Confidence: {response3.confidence:.2f}")
    
    # Learning stats
    print("\n4. Learning Statistics:")
    stats = agent.get_learning_stats()
    print(json.dumps(stats, indent=2))
