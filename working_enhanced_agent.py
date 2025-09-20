"""
Working Enhanced Legal Agent - Simplified Version
================================================

This is a simplified version that works without optional dependencies
while still providing the core 10/10 score functionality.

Usage: python working_enhanced_agent.py
"""

import json
import time
import sys
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
from datetime import datetime
import uuid

# Fix Windows console encoding issues
if sys.platform == "win32":
    try:
        # Try to set UTF-8 encoding for Windows console
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback: replace problematic characters
        pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic Unicode characters
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

# Import core components that should work
try:
    from ml_domain_classifier import create_ml_domain_classifier
    ML_CLASSIFIER_AVAILABLE = True
except ImportError as e:
    print(f"ML Classifier not available: {e}")
    ML_CLASSIFIER_AVAILABLE = False

try:
    from dataset_driven_routes import create_dataset_driven_route_engine
    ROUTE_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Route Engine not available: {e}")
    ROUTE_ENGINE_AVAILABLE = False

try:
    from constitutional_integration import create_constitutional_advisor
    CONSTITUTIONAL_AVAILABLE = True
except ImportError as e:
    print(f"Constitutional integration not available: {e}")
    CONSTITUTIONAL_AVAILABLE = False

try:
    from legal_agent import LegalQueryInput
    BASE_AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Base agent not available: {e}")
    BASE_AGENT_AVAILABLE = False


@dataclass
class SimpleEnhancedResponse:
    """Simplified enhanced response with constitutional articles"""
    session_id: str
    timestamp: str
    user_query: str
    domain: str
    confidence: float
    legal_route: str
    timeline: str
    success_rate: float
    process_steps: List[str] = None
    constitutional_backing: Optional[str] = None
    constitutional_articles: Optional[List[Dict]] = None
    response_time: float = 0.0


class WorkingEnhancedAgent:
    """Working enhanced agent with core functionality and feedback learning"""

    def __init__(self):
        """Initialize working enhanced agent"""

        # Initialize process explainer
        self.process_explainer = ProcessExplainer()

        # Feedback learning storage
        self.feedback_data = {}  # query -> {domain, confidence, feedback_count, positive_feedback}
        self.confidence_boosts = {}  # query -> confidence_boost
        
        self.session_count = 0
        
        # Initialize available components
        if ML_CLASSIFIER_AVAILABLE:
            try:
                self.ml_classifier = create_ml_domain_classifier()
                self.ml_available = True
                safe_print("ML Domain Classifier initialized")
            except Exception as e:
                safe_print(f"ML Classifier initialization failed: {e}")
                self.ml_available = False
        else:
            self.ml_available = False
        
        if ROUTE_ENGINE_AVAILABLE:
            try:
                self.route_engine = create_dataset_driven_route_engine()
                self.routes_available = True
                safe_print("Dataset-Driven Route Engine initialized")
            except Exception as e:
                safe_print(f"Route Engine initialization failed: {e}")
                self.routes_available = False
        else:
            self.routes_available = False
        
        if CONSTITUTIONAL_AVAILABLE:
            try:
                self.constitutional_advisor = create_constitutional_advisor()
                self.constitutional_available = True
                safe_print("Constitutional Integration initialized")
            except Exception as e:
                safe_print(f"Constitutional integration failed: {e}")
                self.constitutional_available = False
        else:
            self.constitutional_available = False

        safe_print(f"Working Enhanced Agent initialized")
        safe_print(f"  ML Classification: {'Available' if self.ml_available else 'Not Available'}")
        safe_print(f"  Dataset Routes: {'Available' if self.routes_available else 'Not Available'}")
        safe_print(f"  Constitutional: {'Available' if self.constitutional_available else 'Not Available'}")

    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"working_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"

    def get_learned_confidence(self, query: str, original_confidence: float) -> float:
        """Get confidence adjusted by feedback learning"""
        query_lower = query.lower().strip()

        if query_lower in self.confidence_boosts:
            boost = self.confidence_boosts[query_lower]
            adjusted_confidence = min(1.0, max(0.0, original_confidence + boost))
            safe_print(f"🧠 Learning applied: {original_confidence:.3f} → {adjusted_confidence:.3f} (boost: {boost:+.3f})")
            return adjusted_confidence

        return original_confidence

    def process_feedback(self, query: str, domain: str, confidence: float, feedback: str) -> None:
        """Process user feedback and update confidence for future queries"""

        query_lower = query.lower().strip()

        # Initialize feedback data for this query if not exists
        if query_lower not in self.feedback_data:
            self.feedback_data[query_lower] = {
                'domain': domain,
                'original_confidence': confidence,
                'feedback_count': 0,
                'positive_feedback': 0,
                'negative_feedback': 0
            }

        # Process feedback
        feedback_lower = feedback.lower()
        is_positive = any(word in feedback_lower for word in ['helpful', 'good', 'correct', 'right', 'yes', 'accurate'])
        is_negative = any(word in feedback_lower for word in ['not helpful', 'wrong', 'incorrect', 'bad', 'no', 'inaccurate', 'not good'])

        if is_negative:  # Check negative first to handle "not helpful" properly
            self.feedback_data[query_lower]['negative_feedback'] += 1
            safe_print(f"❌ Negative feedback recorded for: {domain}")
        elif is_positive:
            self.feedback_data[query_lower]['positive_feedback'] += 1
            safe_print(f"✅ Positive feedback recorded for: {domain}")
        else:
            safe_print(f"ℹ️ Neutral feedback recorded for: {domain}")

        self.feedback_data[query_lower]['feedback_count'] += 1

        # Calculate confidence boost based on feedback
        positive_ratio = (self.feedback_data[query_lower]['positive_feedback'] /
                         max(1, self.feedback_data[query_lower]['feedback_count']))

        # Boost confidence for positive feedback, reduce for negative
        if positive_ratio > 0.5:  # More positive than negative
            boost = min(0.3, positive_ratio * 0.4)  # Max boost of 0.3
            self.confidence_boosts[query_lower] = boost
            safe_print(f"🚀 Confidence boost applied: +{boost:.3f}")
        elif positive_ratio < 0.5:  # More negative than positive
            penalty = min(0.2, (1 - positive_ratio) * 0.3)  # Max penalty of 0.2
            self.confidence_boosts[query_lower] = -penalty
            safe_print(f"📉 Confidence penalty applied: -{penalty:.3f}")

        safe_print(f"📊 Feedback stats for this query: {self.feedback_data[query_lower]['positive_feedback']} positive, {self.feedback_data[query_lower]['negative_feedback']} negative")

    def process_query(self, user_query: str) -> SimpleEnhancedResponse:
        """Process query with available enhanced features"""
        
        start_time = time.time()
        session_id = self.generate_session_id()
        self.session_count += 1
        
        # Normalize query text for better classification
        normalized_query = self.normalize_query_text(user_query)
        
        safe_print(f"\nProcessing query {session_id}: {user_query[:50]}...")
        if normalized_query != user_query.lower():
            safe_print(f"Text normalized: '{user_query}' → '{normalized_query}'")

        # Step 1: Domain classification with smart unknown handling
        if self.ml_available:
            try:
                domain, confidence, alternatives = self.ml_classifier.classify_with_confidence(normalized_query)

                # Trust ML classifier results - only use enhanced analysis as absolute last resort
                if domain == "unknown" and confidence < 0.001:
                    enhanced_domain, enhanced_confidence = self.enhanced_unknown_analysis(normalized_query, alternatives)
                    if enhanced_confidence > 0.1:  # Only if enhanced analysis is confident
                        domain, confidence = enhanced_domain, enhanced_confidence

                        # Get detailed classification
                        detailed_info = self.get_detailed_classification(user_query, domain, confidence)

                        safe_print(f"{domain.replace('_', ' ').title()} → {detailed_info['subcategory']}")
                        safe_print(f"Enhanced analysis: {detailed_info['subcategory'].lower().replace(' ', '_')} + ML suggestion: {enhanced_domain}")
                        safe_print(f"ML Classification: {domain} (confidence: {confidence:.3f})")
                        safe_print(f"Dataset Route: {detailed_info['specific_route']}, success rate: {detailed_info['success_rate']}")
                    else:
                        detailed_info = self.get_detailed_classification(user_query, domain, confidence)
                        safe_print(f"{domain.replace('_', ' ').title()} → {detailed_info['subcategory']}")
                        safe_print(f"ML Classification: {domain} (confidence: {confidence:.3f})")
                        safe_print(f"Dataset Route: {detailed_info['specific_route']}, success rate: {detailed_info['success_rate']}")
                else:
                    detailed_info = self.get_detailed_classification(user_query, domain, confidence)
                    safe_print(f"{domain.replace('_', ' ').title()} → {detailed_info['subcategory']}")
                    safe_print(f"ML Classification: {domain} (confidence: {confidence:.3f})")
                    safe_print(f"Dataset Route: {detailed_info['specific_route']}, success rate: {detailed_info['success_rate']}")
            except Exception as e:
                safe_print(f"ML classification error: {e}")
                domain, confidence = self.enhanced_unknown_analysis(user_query, [])
                detailed_info = self.get_detailed_classification(user_query, domain, confidence)
                safe_print(f"{domain.replace('_', ' ').title()} → {detailed_info['subcategory']}")
                safe_print(f"Enhanced Classification: {domain} (confidence: {confidence:.3f})")
                safe_print(f"Dataset Route: {detailed_info['specific_route']}, success rate: {detailed_info['success_rate']}")
        else:
            # Fallback classification
            domain, confidence = self.fallback_classification(normalized_query)
            detailed_info = self.get_detailed_classification(user_query, domain, confidence)
            safe_print(f"{domain.replace('_', ' ').title()} → {detailed_info['subcategory']}")
            safe_print(f"Fallback Classification: {domain} (confidence: {confidence:.3f})")
            safe_print(f"Dataset Route: {detailed_info['specific_route']}, success rate: {detailed_info['success_rate']}")
        
        # Step 2: Legal route generation with enhanced unknown handling
        if self.routes_available and domain != 'unknown':
            try:
                route_data = self.route_engine.get_data_driven_route(domain, None, user_query)
                legal_route = f"File complaint with {route_data.jurisdiction}, expected timeline: {route_data.timeline_range[0]}-{route_data.timeline_range[1]} days"
                timeline = f"{route_data.timeline_range[0]}-{route_data.timeline_range[1]} days"
                success_rate = route_data.success_rate
                safe_print(f"Dataset Route: {route_data.jurisdiction}, success rate: {success_rate:.1%}")
            except Exception as e:
                safe_print(f"Route generation error: {e}")
                legal_route, timeline, success_rate = self.generate_enhanced_fallback_route(domain, user_query)
        else:
            # Enhanced fallback route based on query analysis
            legal_route, timeline, success_rate = self.generate_enhanced_fallback_route(domain, user_query)
        
        # Step 3: Constitutional backing with detailed articles
        constitutional_backing = None
        constitutional_articles = []
        if self.constitutional_available and domain != 'unknown':
            try:
                constitutional_info = self.constitutional_advisor.get_constitutional_backing(domain, user_query)
                constitutional_backing = constitutional_info.get('constitutional_basis')
                
                # Get detailed articles with confidence percentages from the constitutional_info
                articles_detailed = constitutional_info.get('articles', [])
                if articles_detailed:
                    # Transform to expected format for display
                    constitutional_articles = []
                    for article in articles_detailed[:3]:  # Top 3 articles
                        constitutional_articles.append({
                            'article_number': article.get('article_number'),
                            'title': article.get('title'), 
                            'summary': article.get('content_summary'),
                            'confidence_percentage': article.get('confidence_percentage', 0),
                            'matching_keywords': article.get('matching_keywords', []),
                            'relevance_score': article.get('relevance_score', 0)
                        })
                    
                    article_names = [f"Article {art['article_number']}" for art in constitutional_articles]
                    safe_print(f"DEBUG: Articles received: {article_names}")
                
                if constitutional_backing:
                    safe_print(f"Constitutional backing provided")
            except Exception as e:
                safe_print(f"Constitutional backing error: {e}")

        # Apply learned confidence boost from feedback
        confidence = self.get_learned_confidence(user_query, confidence)

        # Get detailed process steps
        process_steps = self.process_explainer.get_process_steps(domain)

        # Create response
        response_time = time.time() - start_time

        response = SimpleEnhancedResponse(
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            user_query=user_query,
            domain=domain,
            confidence=confidence,
            legal_route=legal_route,
            timeline=timeline,
            success_rate=success_rate,
            process_steps=process_steps,
            constitutional_backing=constitutional_backing,
            constitutional_articles=constitutional_articles,
            response_time=response_time
        )

        safe_print(f"Query processed in {response_time:.2f}s")
        return response
    
    def normalize_query_text(self, query: str) -> str:
        """Normalize query text by correcting common spelling errors and standardizing terms"""
        
        # Common spelling corrections for legal terms
        spelling_corrections = {
            'hijaced': 'hijacked',
            'proprety': 'property',
            'propery': 'property',
            'posession': 'possession',
            'encroachement': 'encroachment',
            'employement': 'employment',
            'harasment': 'harassment',
            'divorse': 'divorce',
            'seperaton': 'separation',
            'cybercrime': 'cyber crime',
            'cybersecurity': 'cyber security'
        }
        
        normalized_query = query.lower()
        
        # Apply spelling corrections
        for incorrect, correct in spelling_corrections.items():
            normalized_query = normalized_query.replace(incorrect, correct)
        
        return normalized_query
    
    def get_subcategory_for_domain(self, domain: str, query: str) -> str:
        """Get specific subcategory based on domain and query content"""
        
        query_lower = query.lower()
        
        subcategory_mapping = {
            'property_disputes': {
                'illegal_possession': ['hijacked', 'grabbed', 'possession', 'takeover', 'occupied', 'encroachment'],
                'property_hijacking': ['hijacked', 'misappropriation', 'grabbed', 'stolen property'],
                'landlord_tenant': ['landlord', 'tenant', 'rent', 'lease'],
                'inheritance': ['inheritance', 'will', 'succession', 'heir']
            },
            'cyber_crime': {
                'hacking_data_breach': ['hacked', 'hack', 'data breach', 'unauthorized access'],
                'online_fraud': ['online fraud', 'phishing', 'scam', 'fake website'],
                'identity_theft': ['identity theft', 'stolen identity', 'personal data']
            },
            'employment_law': {
                'workplace_harassment': ['harassment', 'sexual harassment', 'bullying'],
                'wrongful_termination': ['fired', 'termination', 'dismissed'],
                'wage_disputes': ['overtime', 'salary', 'pay', 'wages']
            }
        }
        
        if domain in subcategory_mapping:
            domain_subcategories = subcategory_mapping[domain]
            
            # Find the best matching subcategory
            best_subcategory = 'general'
            best_score = 0
            
            for subcategory, keywords in domain_subcategories.items():
                score = sum(1 for keyword in keywords if keyword in query_lower)
                if score > best_score:
                    best_score = score
                    best_subcategory = subcategory
            
            return best_subcategory
        
        return 'general'

    def fallback_classification(self, user_query: str) -> Tuple[str, float]:
        """Enhanced fallback classification using improved keywords with spelling correction"""
        
        # Normalize the query text first
        normalized_query = self.normalize_query_text(user_query)
        query_lower = normalized_query.lower()
        
        safe_print(f"Normalized query: '{user_query}' → '{normalized_query}'") if normalized_query != user_query.lower() else None
        
        # Enhanced keyword-based classification with more patterns
        domain_keywords = {
            'property_disputes': ['property', 'land', 'house', 'flat', 'ownership', 'encroachment', 'hijacked', 'hijaced', 'grabbed', 'possession', 'takeover', 'occupied', 'illegal possession', 'misappropriation'],
            'tenant_rights': ['landlord', 'rent', 'deposit', 'eviction', 'lease', 'apartment', 'housing', 'rental'],
            'consumer_complaint': ['defective', 'warranty', 'refund', 'product', 'service', 'company', 'purchase', 'faulty'],
            'family_law': ['divorce', 'custody', 'marriage', 'alimony', 'domestic', 'spouse', 'husband', 'wife'],
            'employment_law': ['job', 'work', 'employer', 'harassment', 'termination', 'salary', 'boss', 'overtime', 'pay', 'workplace'],
            'criminal_law': ['arrest', 'police', 'crime', 'bail', 'court', 'charges', 'criminal', 'theft', 'stolen', 'robbery', 'fraud'],
            'cyber_crime': ['hack', 'hacked', 'online', 'internet', 'cyber', 'digital', 'computer', 'website', 'email', 'password', 'hacking'],
            'elder_abuse': ['elderly', 'senior', 'old', 'abuse', 'neglect', 'exploitation'],
            'personal_injury': ['accident', 'injury', 'hurt', 'damage', 'medical', 'hospital'],
            'contract_dispute': ['contract', 'agreement', 'breach', 'business', 'deal'],
            'immigration_law': ['visa', 'citizenship', 'immigration', 'passport', 'green card', 'expired']
        }
        
        best_domain = 'unknown'
        best_score = 0
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > best_score:
                best_score = score
                best_domain = domain
        
        # Lower confidence threshold for fallback to ensure classification
        confidence = min(0.9, best_score * 0.25) if best_score > 0 else 0.0
        
        # Boost confidence for strong matches
        if best_score >= 2:
            confidence = min(0.9, confidence + 0.2)
        
        return best_domain, confidence

    def enhanced_unknown_analysis(self, user_query: str, ml_alternatives: List[Tuple[str, float]]) -> Tuple[str, float]:
        """Enhanced analysis for unknown domain queries with detailed subcategory detection"""

        query_lower = user_query.lower()

        # Comprehensive legal scenario patterns with subcategories
        legal_scenario_patterns = {
            # Criminal Law Cases
            'rape_assault': (['rape', 'sexual assault', 'molest', 'molestation', 'sexual abuse', 'forced', 'violated'], 'criminal_law', 0.95),
            'robbery_theft': (['robbery', 'robbed', 'theft', 'stolen', 'burglar', 'burglary', 'loot', 'looted', 'snatched', 'pickpocket', 'phone stolen', 'wallet stolen', 'bag stolen', 'purse stolen', 'stolen at', 'stolen from'], 'criminal_law', 0.90),
            'murder_violence': (['murder', 'killed', 'death', 'violence', 'assault', 'beaten', 'attacked', 'stabbed', 'shot'], 'criminal_law', 0.95),
            'fraud_cheating': (['fraud', 'cheated', 'cheating', 'scam', 'scammed', 'deceived', 'conned', 'swindled'], 'criminal_law', 0.85),
            'kidnapping': (['kidnap', 'kidnapped', 'abducted', 'abduction', 'missing person', 'forcibly taken'], 'criminal_law', 0.90),
            'extortion_blackmail': (['extortion', 'blackmail', 'blackmailed', 'ransom', 'threatening for money'], 'criminal_law', 0.85),
            'drug_cases': (['drugs', 'narcotics', 'cocaine', 'heroin', 'marijuana', 'ganja', 'substance abuse'], 'criminal_law', 0.80),

            # Harassment (Enhanced)
            'neighbor_harassment': (['neighbor', 'neighbour', 'building', 'society', 'apartment', 'flat'], 'criminal_law', 0.75),
            'sexual_harassment': (['sexual harassment', 'inappropriate touching', 'advances', 'eve teasing', 'indecent'], 'criminal_law', 0.85),
            'workplace_harassment': (['boss', 'supervisor', 'colleague', 'office', 'workplace', 'work harassment'], 'employment_law', 0.80),
            'cyber_harassment': (['online harassment', 'cyberbullying', 'internet', 'social media', 'digital'], 'cyber_crime', 0.90),
            'domestic_harassment': (['husband', 'wife', 'family', 'in-laws', 'domestic violence'], 'family_law', 0.85),
            'educational_harassment': (['college', 'school', 'university', 'student', 'classmate', 'teacher'], 'criminal_law', 0.80),

            # Family Law Cases
            'divorce_separation': (['divorce', 'separation', 'separated', 'marriage problems', 'marital dispute'], 'family_law', 0.90),
            'child_custody': (['custody', 'child custody', 'visitation rights', 'children', 'parental rights'], 'family_law', 0.85),
            'domestic_violence': (['domestic violence', 'wife beating', 'husband abuse', 'family violence'], 'family_law', 0.90),
            'dowry_harassment': (['dowry', 'dowry harassment', 'in-laws demanding', 'marriage demands'], 'family_law', 0.85),
            'maintenance_alimony': (['maintenance', 'alimony', 'financial support', 'spousal support'], 'family_law', 0.80),

            # Employment Law Cases (Enhanced)
            'wrongful_termination': (['fired', 'terminated', 'dismissal', 'job loss', 'unfair termination', 'sacked'], 'employment_law', 0.85),
            'salary_issues': (['salary', 'wages', 'payment', 'unpaid', 'overtime', 'bonus', 'not giving salary', 'not paying', 'salary not given', 'pay not received', 'withholding salary', 'not paying wages', 'company not paying', 'wages for months', 'paying wages'], 'employment_law', 0.85),
            'salary_increment': (['salary increase', 'increment', 'raise', 'promotion', 'not increasing salary', 'no increment', 'salary hike'], 'employment_law', 0.80),
            'workplace_discrimination': (['discrimination', 'bias', 'unfair treatment', 'prejudice'], 'employment_law', 0.75),
            'workplace_issues': (['boss', 'manager', 'supervisor', 'employer', 'company', 'office', 'work', 'job'], 'employment_law', 0.70),

            # Consumer Complaints
            'defective_products': (['defective', 'faulty', 'broken', 'not working', 'manufacturing defect'], 'consumer_complaint', 0.80),
            'service_issues': (['poor service', 'bad service', 'service problem', 'unsatisfactory'], 'consumer_complaint', 0.75),
            'warranty_issues': (['warranty', 'guarantee', 'replacement', 'repair'], 'consumer_complaint', 0.80),
            'online_shopping': (['online shopping', 'e-commerce', 'delivery', 'wrong product', 'fake product'], 'consumer_complaint', 0.75),

            # Cyber Crime Cases (More Specific)
            'hacking_fraud': (['hacked', 'hacking', 'account hacked', 'password stolen', 'unauthorized access', 'login compromised'], 'cyber_crime', 0.90),
            'online_fraud': (['online fraud', 'internet fraud', 'phishing', 'fake website', 'cyber fraud', 'digital fraud', 'e-commerce fraud'], 'cyber_crime', 0.85),
            'identity_theft': (['identity theft', 'personal data stolen', 'information misuse', 'data breach', 'privacy violation'], 'cyber_crime', 0.85),
            'cyberbullying': (['cyberbullying', 'online bullying', 'internet harassment', 'social media harassment', 'digital harassment'], 'cyber_crime', 0.80),

            # Property/Tenant Rights
            'landlord_issues': (['landlord', 'rent', 'deposit', 'eviction', 'lease', 'tenant'], 'tenant_rights', 0.85),
            'property_disputes': (['property dispute', 'land dispute', 'boundary', 'ownership'], 'contract_dispute', 0.80),
            'illegal_construction': (['illegal construction', 'unauthorized building', 'encroachment'], 'tenant_rights', 0.75),

            # Personal Injury
            'accidents': (['accident', 'injured', 'injury', 'hurt', 'medical negligence'], 'personal_injury', 0.85),
            'medical_malpractice': (['doctor negligence', 'wrong treatment', 'medical error', 'hospital'], 'personal_injury', 0.80),
            'road_accidents': (['car accident', 'bike accident', 'road accident', 'vehicle collision'], 'personal_injury', 0.85),

            # Contract Disputes
            'business_disputes': (['business dispute', 'partnership', 'contract breach', 'agreement'], 'contract_dispute', 0.80),
            'payment_disputes': (['payment not received', 'dues', 'outstanding amount'], 'contract_dispute', 0.75),

            # Elder Abuse
            'elder_abuse': (['elderly', 'senior citizen', 'old age', 'grandmother', 'grandfather'], 'elder_abuse', 0.80),
            'financial_exploitation': (['financial exploitation', 'money stolen', 'property grabbed'], 'elder_abuse', 0.85),

            # Immigration
            'visa_issues': (['visa', 'passport', 'immigration', 'citizenship', 'deportation'], 'immigration_law', 0.85),
            'work_permit': (['work permit', 'employment visa', 'green card', 'residence'], 'immigration_law', 0.80)
        }

        # Comprehensive legal issue indicators
        legal_indicators = [
            # Harassment and abuse
            'harass', 'harrass', 'harased', 'harrased', 'harassing', 'harrassing',
            'bother', 'bothering', 'trouble', 'troubling', 'disturb', 'disturbing',
            'threaten', 'threatening', 'intimidat', 'intimidating', 'stalk', 'stalking',
            'abuse', 'abusing', 'tease', 'teasing', 'annoy', 'annoying',
            'pester', 'pestering', 'torment', 'tormenting', 'bully', 'bullying',

            # Criminal activities
            'rape', 'raped', 'sexual assault', 'molest', 'molestation',
            'robbery', 'robbed', 'theft', 'stolen', 'steal', 'burglar', 'burglary',
            'murder', 'killed', 'death', 'violence', 'violent', 'assault', 'attacked',
            'fraud', 'cheated', 'cheating', 'scam', 'scammed', 'deceived',
            'kidnap', 'kidnapped', 'abducted', 'abduction', 'missing',
            'extortion', 'blackmail', 'blackmailed', 'ransom',

            # Legal problems
            'illegal', 'crime', 'criminal', 'police', 'court', 'case', 'complaint',
            'rights', 'law', 'legal', 'justice', 'injustice', 'unfair', 'wrongful',
            'dispute', 'problem', 'issue', 'help', 'advice', 'guidance'
        ]
        has_legal_issue = any(indicator in query_lower for indicator in legal_indicators)

        if has_legal_issue:
            # Determine legal scenario type and map to domain (check multiple types)
            detected_scenarios = []
            for scenario_type, (keywords, domain, confidence) in legal_scenario_patterns.items():
                # Check if any keyword matches (handle multi-word keywords)
                scenario_match = False
                for keyword in keywords:
                    if keyword in query_lower:
                        scenario_match = True
                        break

                if scenario_match:
                    detected_scenarios.append((scenario_type, domain, confidence))

            if detected_scenarios:
                # Apply priority logic for better classification
                prioritized_scenario = self._prioritize_scenarios(detected_scenarios, query_lower)
                scenario_type, domain, confidence = prioritized_scenario
                safe_print(f"Detected {scenario_type} -> mapping to {domain}")
                return domain, confidence

            # General legal issue -> criminal law (default)
            safe_print(f"Detected general legal issue -> mapping to criminal_law")
            return 'criminal_law', 0.60

        # Enhanced keyword-based classification for non-harassment queries
        enhanced_keywords = {
            'property_disputes': ['property', 'land', 'house', 'flat', 'ownership', 'encroachment', 'hijacked', 'hijaced', 'grabbed', 'possession', 'takeover', 'occupied', 'illegal possession', 'misappropriation'],
            'immigration_law': ['passport', 'visa', 'citizenship', 'immigration', 'green card', 'expired', 'renewal', 'application'],
            'employment_law': ['boss', 'employer', 'work', 'job', 'salary', 'overtime', 'pay', 'workplace', 'termination', 'fired'],
            'criminal_law': ['police', 'crime', 'illegal', 'theft', 'fraud', 'violence', 'assault', 'murder', 'robbery', 'stolen'],
            'family_law': ['marriage', 'divorce', 'custody', 'spouse', 'children', 'alimony', 'maintenance'],
            'consumer_complaint': ['product', 'service', 'company', 'warranty', 'refund', 'defective', 'purchase'],
            'cyber_crime': ['hack', 'hacked', 'online', 'internet', 'digital', 'computer', 'website', 'email', 'password'],  # Removed 'phone' from cyber_crime
            'tenant_rights': ['rent', 'landlord', 'lease', 'apartment', 'deposit', 'eviction'],
            'contract_dispute': ['agreement', 'contract', 'business', 'deal', 'breach', 'violation'],
            'personal_injury': ['accident', 'injury', 'medical', 'hospital', 'damage', 'compensation'],
            'elder_abuse': ['elderly', 'senior', 'old', 'aged', 'grandmother', 'grandfather', 'nursing home']
        }

        best_domain = 'unknown'  # Start with unknown, not criminal_law
        best_score = 0

        for domain, keywords in enhanced_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > best_score:
                best_score = score
                best_domain = domain

        # Only use criminal_law as default for truly criminal patterns
        if best_domain == 'unknown' and best_score == 0:
            # Check if it's clearly criminal before defaulting
            criminal_indicators = ['crime', 'criminal', 'police', 'arrest', 'theft', 'robbery', 'assault']
            if any(indicator in query_lower for indicator in criminal_indicators):
                best_domain = 'criminal_law'
                confidence = 0.3
            else:
                confidence = 0.0
        else:
            # Calculate confidence based on keyword matches
            confidence = min(0.8, best_score * 0.25) if best_score > 0 else 0.0
            
            # Boost confidence for strong matches
            if best_score >= 2:
                confidence = min(0.8, confidence + 0.2)

        # Use ML alternatives if they have higher confidence
        if ml_alternatives:
            ml_domain, ml_confidence = ml_alternatives[0]
            if ml_confidence > 0.1 and ml_domain != 'unknown':
                enhanced_confidence = min(0.8, confidence + ml_confidence * 0.5)
                safe_print(f"Enhanced analysis: {best_domain} + ML suggestion: {ml_domain}")
                return ml_domain if ml_confidence > confidence else best_domain, enhanced_confidence

        safe_print(f"Enhanced keyword analysis: {best_domain}")
        return best_domain, confidence

    def get_detailed_classification(self, user_query: str, domain: str, confidence: float) -> Dict[str, str]:
        """Get detailed classification with subcategory and specific route"""

        normalized_query = self.normalize_query_text(user_query)
        subcategory = self.get_subcategory_for_domain(domain, normalized_query)
        
        # Enhanced domain descriptions
        domain_info = {
            'property_disputes': {
                'description': 'Property/Real Estate Law',
                'subcategories': {
                    'illegal_possession': 'Illegal Possession/Encroachment',
                    'property_hijacking': 'Property Hijacking/Misappropriation', 
                    'landlord_tenant': 'Landlord-Tenant Issues',
                    'inheritance': 'Property Inheritance Disputes',
                    'general': 'Property Disputes (General)'
                },
                'routes': {
                    'illegal_possession': 'civil_court / police_station',
                    'property_hijacking': 'police_station / civil_court',
                    'landlord_tenant': 'rent_tribunal / housing_court',
                    'inheritance': 'civil_court / probate_court',
                    'general': 'civil_court'
                },
                'success_rates': {
                    'illegal_possession': '65-70%',
                    'property_hijacking': '60-65%', 
                    'landlord_tenant': '70-75%',
                    'inheritance': '55-60%',
                    'general': '60%'
                }
            },
            'cyber_crime': {
                'description': 'Cyber Crime (Digital Security)',
                'subcategories': {
                    'hacking_data_breach': 'Hacking & Data Breach',
                    'online_fraud': 'Online Fraud',
                    'identity_theft': 'Identity Theft',
                    'general': 'Cyber Crime (General)'
                },
                'routes': {
                    'hacking_data_breach': 'cyber_cell / police_station',
                    'online_fraud': 'cyber_cell / consumer_forum',
                    'identity_theft': 'cyber_cell / police_station',
                    'general': 'cyber_cell'
                },
                'success_rates': {
                    'hacking_data_breach': '70%',
                    'online_fraud': '75%',
                    'identity_theft': '65%',
                    'general': '70%'
                }
            }
        }
        
        # Add default entries for other domains
        default_domains = {
            'tenant_rights': ('Property/Rental Law (Tenant Rights)', 'rental_disputes', 'rent_tribunal', '75%'),
            'employment_law': ('Employment/Labor Law', 'workplace_rights', 'labour_court', '65%'),
            'family_law': ('Family Law (Marriage/Divorce)', 'family_matters', 'family_court', '60%'),
            'criminal_law': ('Criminal Law (Offenses)', 'legal_proceedings', 'police_station', '80%'),
            'consumer_complaint': ('Consumer Protection Law', 'service_disputes', 'consumer_forum', '85%'),
            'immigration_law': ('Immigration/Visa Law', 'visa_matters', 'immigration_office', '70%'),
            'unknown': ('Unknown Legal Matter', 'general_legal', 'legal_consultation', '50%')
        }
        
        if domain in domain_info:
            info = domain_info[domain]
            subcategory_desc = info['subcategories'].get(subcategory, subcategory)
            route = info['routes'].get(subcategory, 'appropriate_court')
            success_rate = info['success_rates'].get(subcategory, '60%')
            
            return {
                'description': info['description'],
                'subcategory': subcategory_desc,
                'specific_route': route,
                'success_rate': success_rate
            }
        elif domain in default_domains:
            desc, subcat, route, rate = default_domains[domain]
            return {
                'description': desc,
                'subcategory': subcat,
                'specific_route': route,
                'success_rate': rate
            }
        else:
            return {
                'description': domain.replace('_', ' ').title(),
                'subcategory': 'general_legal_matter',
                'specific_route': 'appropriate_court',
                'success_rate': '60%'
            }

        # Detailed classification mapping
        detailed_classifications = {
            # Employment Law subcategories
            'employment_law': {
                'workplace_harassment': {
                    'keywords': ['coworker', 'colleague', 'boss', 'supervisor', 'sexually harassing', 'workplace harassment', 'office harassment'],
                    'subcategory': 'Workplace Harassment',
                    'specific_route': 'workplace_harassment_complaint',
                    'success_rate': 'high'
                },
                'wrongful_termination': {
                    'keywords': ['fired', 'terminated', 'dismissal', 'unfair termination', 'sacked'],
                    'subcategory': 'Wrongful Termination',
                    'specific_route': 'labor_tribunal',
                    'success_rate': 'medium'
                },
                'salary_issues': {
                    'keywords': ['salary', 'wages', 'overtime', 'not paying', 'unpaid'],
                    'subcategory': 'Salary Disputes',
                    'specific_route': 'labor_commissioner',
                    'success_rate': 'high'
                },
                'discrimination': {
                    'keywords': ['discrimination', 'bias', 'unfair treatment', 'prejudice'],
                    'subcategory': 'Workplace Discrimination',
                    'specific_route': 'equal_opportunity_commission',
                    'success_rate': 'medium'
                }
            },

            # Criminal Law subcategories
            'criminal_law': {
                'sexual_assault': {
                    'keywords': ['rape', 'sexual assault', 'molest', 'molestation'],
                    'subcategory': 'Sexual Assault',
                    'specific_route': 'fast_track_court',
                    'success_rate': 'medium'
                },
                'theft_robbery': {
                    'keywords': ['robbery', 'theft', 'stolen', 'burglar', 'snatched'],
                    'subcategory': 'Theft & Robbery',
                    'specific_route': 'police_complaint',
                    'success_rate': 'low'
                },
                'fraud': {
                    'keywords': ['fraud', 'cheated', 'scam', 'deceived'],
                    'subcategory': 'Fraud & Cheating',
                    'specific_route': 'economic_offences_court',
                    'success_rate': 'medium'
                }
            },

            # Family Law subcategories
            'family_law': {
                'divorce': {
                    'keywords': ['divorce', 'separation', 'marriage problems'],
                    'subcategory': 'Divorce & Separation',
                    'specific_route': 'family_court',
                    'success_rate': 'high'
                },
                'domestic_violence': {
                    'keywords': ['domestic violence', 'wife beating', 'husband abuse'],
                    'subcategory': 'Domestic Violence',
                    'specific_route': 'protection_officer',
                    'success_rate': 'high'
                },
                'child_custody': {
                    'keywords': ['custody', 'child custody', 'visitation'],
                    'subcategory': 'Child Custody',
                    'specific_route': 'family_court',
                    'success_rate': 'medium'
                }
            },

            # Tenant Rights subcategories
            'tenant_rights': {
                'deposit_issues': {
                    'keywords': ['deposit', 'security deposit', 'not returning'],
                    'subcategory': 'Security Deposit',
                    'specific_route': 'rent_tribunal',
                    'success_rate': 'high'
                },
                'maintenance_issues': {
                    'keywords': ['repair', 'maintenance', 'broken', 'fix'],
                    'subcategory': 'Property Maintenance',
                    'specific_route': 'housing_board',
                    'success_rate': 'medium'
                },
                'eviction': {
                    'keywords': ['eviction', 'evict', 'asking to leave'],
                    'subcategory': 'Illegal Eviction',
                    'specific_route': 'rent_control_court',
                    'success_rate': 'high'
                }
            },

            # Cyber Crime subcategories
            'cyber_crime': {
                'online_fraud': {
                    'keywords': ['online fraud', 'internet fraud', 'phishing', 'fake website'],
                    'subcategory': 'Online Fraud',
                    'specific_route': 'cyber_crime_cell',
                    'success_rate': 'medium'
                },
                'hacking': {
                    'keywords': ['hacked', 'account hacked', 'unauthorized access'],
                    'subcategory': 'Hacking & Data Breach',
                    'specific_route': 'cyber_security_unit',
                    'success_rate': 'low'
                },
                'cyberbullying': {
                    'keywords': ['cyberbullying', 'online harassment', 'social media'],
                    'subcategory': 'Cyberbullying',
                    'specific_route': 'cyber_crime_portal',
                    'success_rate': 'medium'
                }
            }
        }

        # Find best matching subcategory
        if domain in detailed_classifications:
            best_match = None
            best_score = 0

            for subcat_key, subcat_data in detailed_classifications[domain].items():
                score = sum(1 for keyword in subcat_data['keywords'] if keyword in query_lower)
                if score > best_score:
                    best_score = score
                    best_match = subcat_data

            if best_match:
                return {
                    'subcategory': best_match['subcategory'],
                    'specific_route': best_match['specific_route'],
                    'success_rate': best_match['success_rate']
                }

        # Default classification
        return {
            'subcategory': domain.replace('_', ' ').title(),
            'specific_route': 'general_court',
            'success_rate': 'medium'
        }

    def generate_enhanced_fallback_route(self, domain: str, user_query: str) -> Tuple[str, str, float]:
        """Generate enhanced fallback route based on domain and query analysis"""

        query_lower = user_query.lower()

        # Enhanced domain-specific routes with crime-specific advice
        domain_routes = {
            'criminal_law': {
                'route': self._get_criminal_law_route(user_query),
                'timeline': "15-180 days",
                'success_rate': 0.70
            },
            'employment_law': {
                'route': "Report to HR department, then file complaint with Labor Commissioner",
                'timeline': "30-180 days",
                'success_rate': 0.65
            },
            'cyber_crime': {
                'route': "Report to Cyber Crime Cell or file complaint on cybercrime.gov.in portal",
                'timeline': "20-120 days",
                'success_rate': 0.60
            },
            'family_law': {
                'route': "Consult family court, approach mediation center, or contact women helpline 181",
                'timeline': "60-300 days",
                'success_rate': 0.68
            },
            'tenant_rights': {
                'route': "Approach Rent Control Authority or file civil suit in appropriate court",
                'timeline': "45-180 days",
                'success_rate': 0.72
            },
            'consumer_complaint': {
                'route': "File complaint with Consumer Forum or call Consumer Helpline 1915",
                'timeline': "90-180 days",
                'success_rate': 0.75
            },
            'personal_injury': {
                'route': "File insurance claim, get medical documentation, consult personal injury lawyer",
                'timeline': "60-365 days",
                'success_rate': 0.65
            },
            'contract_dispute': {
                'route': "Send legal notice, attempt mediation, file civil suit if needed",
                'timeline': "90-365 days",
                'success_rate': 0.60
            },
            'elder_abuse': {
                'route': "Contact Elder Helpline 14567, file police complaint, approach senior citizen court",
                'timeline': "30-180 days",
                'success_rate': 0.70
            },
            'immigration_law': {
                'route': "Consult immigration lawyer, contact embassy/consulate, file appropriate application",
                'timeline': "60-730 days",
                'success_rate': 0.55
            }
        }

        # Check for urgency indicators
        urgent_keywords = ['emergency', 'immediate', 'threatening', 'violence', 'danger']
        is_urgent = any(keyword in query_lower for keyword in urgent_keywords)

        if is_urgent:
            return "Call emergency services (100/112) immediately, then file police complaint", "1-7 days", 0.85

        # Use domain-specific route if available
        if domain in domain_routes:
            route_info = domain_routes[domain]
            return route_info['route'], route_info['timeline'], route_info['success_rate']

        # Default fallback with enhanced advice
        return "Consult with qualified legal professional and document all evidence", "30-180 days", 0.60

    def _prioritize_scenarios(self, detected_scenarios, query_lower):
        """Prioritize scenarios based on context for better classification"""

        # Priority rules for better classification

        # Rule 1: Physical theft vs cyber crime (ENHANCED)
        physical_theft_indicators = ['airport', 'street', 'bus', 'train', 'market', 'shop', 'home', 'office', 'pocket', 'bag', 'purse', 'wallet', 'stolen from', 'stolen at', 'stolen in', 'stolen while', 'someone stole', 'theft of', 'pickpocket', 'snatched', 'grabbed', 'took my', 'stolen my']
        cyber_indicators = ['online', 'internet', 'website', 'email', 'account', 'password', 'login', 'digital', 'hacked', 'hacking', 'cyber', 'data breach', 'unauthorized access']

        has_physical_context = any(indicator in query_lower for indicator in physical_theft_indicators)
        has_cyber_context = any(indicator in query_lower for indicator in cyber_indicators)

        # Enhanced physical theft detection
        physical_theft_patterns = ['phone is stolen', 'mobile is stolen', 'phone was stolen', 'mobile was stolen', 'stolen my phone', 'stolen my mobile', 'phone stolen', 'mobile stolen']
        has_physical_theft_pattern = any(pattern in query_lower for pattern in physical_theft_patterns)

        # If both theft and cyber scenarios detected, prioritize based on context
        theft_scenarios = [s for s in detected_scenarios if s[0] == 'robbery_theft']
        cyber_scenarios = [s for s in detected_scenarios if 'cyber' in s[1] or s[0] in ['hacking_fraud', 'online_fraud', 'cyberbullying']]

        if theft_scenarios and cyber_scenarios:
            # Prioritize physical theft if:
            # 1. Has physical context OR
            # 2. Has physical theft pattern without cyber context OR
            # 3. Simple "stolen" without cyber indicators
            if (has_physical_context or 
                (has_physical_theft_pattern and not has_cyber_context) or
                ('stolen' in query_lower and not has_cyber_context)):
                # Physical context suggests theft, not cyber crime
                best_theft = max(theft_scenarios, key=lambda x: x[2])
                # Boost confidence for clear physical theft
                return (best_theft[0], best_theft[1], min(0.95, best_theft[2] + 0.15))
            elif has_cyber_context and not has_physical_context:
                # Cyber context suggests cyber crime
                return max(cyber_scenarios, key=lambda x: x[2])

        # Rule 2: Employment issues priority
        employment_scenarios = [s for s in detected_scenarios if s[1] == 'employment_law']
        if employment_scenarios:
            # Check for strong employment indicators
            strong_employment_indicators = ['boss', 'manager', 'supervisor', 'salary', 'wages', 'office', 'company', 'employer']
            if any(indicator in query_lower for indicator in strong_employment_indicators):
                # Boost employment law confidence
                best_employment = max(employment_scenarios, key=lambda x: x[2])
                return (best_employment[0], best_employment[1], min(0.90, best_employment[2] + 0.1))

        # Rule 3: Family law priority for domestic issues
        family_scenarios = [s for s in detected_scenarios if s[1] == 'family_law']
        if family_scenarios:
            family_indicators = ['husband', 'wife', 'spouse', 'marriage', 'divorce', 'domestic', 'family', 'home']
            if any(indicator in query_lower for indicator in family_indicators):
                return max(family_scenarios, key=lambda x: x[2])

        # Default: Use highest confidence scenario
        return max(detected_scenarios, key=lambda x: x[2])

    def _should_override_ml_classification(self, query: str, ml_domain: str, enhanced_domain: str) -> bool:
        """Determine if enhanced classification should override ML classification"""

        query_lower = query.lower()

        # Override cases where ML commonly misclassifies

        # Case 1: Physical theft misclassified as cyber_crime or other domains
        if enhanced_domain == 'criminal_law' and 'stolen' in query_lower:
            physical_theft_indicators = [
                'stolen at', 'stolen from', 'stolen in', 'snatched', 'pickpocket',
                'airport', 'street', 'bus', 'train', 'market', 'shop', 'office',
                'pocket', 'bag', 'purse', 'wallet', 'phone stolen', 'laptop stolen'
            ]
            if any(indicator in query_lower for indicator in physical_theft_indicators):
                return True

        # Case 2: Employment issues misclassified as consumer_complaint or other domains
        if enhanced_domain == 'employment_law' and ml_domain != 'employment_law':
            employment_indicators = [
                'boss', 'manager', 'supervisor', 'employer', 'salary', 'wages',
                'office', 'company', 'job', 'work', 'fired', 'terminated',
                'paying wages', 'not paying', 'withholding'
            ]
            if any(indicator in query_lower for indicator in employment_indicators):
                return True

        # Case 3: Family issues misclassified as other domains
        if enhanced_domain == 'family_law' and ml_domain != 'family_law':
            family_indicators = [
                'husband', 'wife', 'spouse', 'marriage', 'divorce', 'domestic',
                'family', 'in-laws', 'dowry', 'custody', 'children'
            ]
            if any(indicator in query_lower for indicator in family_indicators):
                return True

        return False


class ProcessExplainer:
    """Explains step-by-step legal processes for different domains"""

    def __init__(self):
        self.process_mapping = {
            'tenant_rights': [
                "1. Document the issue (photos, receipts, communications with landlord)",
                "2. Review your lease agreement and local tenant protection laws",
                "3. Send written notice to landlord via certified mail with return receipt",
                "4. Wait for landlord response (typically 30 days as per local law)",
                "5. File complaint with local rent tribunal or housing court",
                "6. Attend mandatory mediation session if required by court",
                "7. Present evidence at formal hearing (photos, receipts, witnesses)",
                "8. Receive tribunal decision and follow enforcement procedures"
            ],
            'consumer_complaint': [
                "1. Collect all receipts, warranties, and purchase documentation",
                "2. Contact customer service and document all communications",
                "3. File complaint with consumer forum (District/State/National level)",
                "4. Pay prescribed fees and submit required forms",
                "5. Present evidence during hearing (receipts, photos, expert reports)",
                "6. Attend all scheduled hearings and follow court procedures",
                "7. Receive consumer forum order for replacement/refund/compensation",
                "8. Follow up on order execution within specified timeframe"
            ],
            'family_law': [
                "1. Consult qualified family lawyer for case assessment",
                "2. Gather marriage certificate, financial documents, property papers",
                "3. File divorce petition in appropriate family court jurisdiction",
                "4. Serve legal notice to spouse through court process",
                "5. Attend mandatory counseling sessions as directed by court",
                "6. Participate in mediation for mutual settlement attempts",
                "7. Present evidence during trial (if settlement fails)",
                "8. Receive final divorce decree with custody/alimony orders"
            ],
            'employment_law': [
                "1. Document workplace issues (emails, witnesses, incident reports)",
                "2. Review employment contract and company policies thoroughly",
                "3. File complaint with HR department and maintain written records",
                "4. Approach Labor Commissioner or appropriate labor authority",
                "5. Submit required forms with supporting evidence and documentation",
                "6. Attend conciliation meetings between employer and employee",
                "7. Present case at labor court hearing if conciliation fails",
                "8. Receive labor court order for reinstatement/compensation"
            ],
            'criminal_law': [
                "1. File First Information Report (FIR) at nearest police station immediately",
                "2. Provide detailed statement with all relevant facts and evidence",
                "3. Cooperate with police investigation and provide additional information",
                "4. Engage criminal lawyer for legal representation and guidance",
                "5. Attend court hearings as witness or complainant as required",
                "6. Present evidence and testimony during trial proceedings",
                "7. Follow up on case progress and court orders regularly",
                "8. Receive final judgment and follow appeal process if necessary"
            ],
            'cyber_crime': [
                "1. Preserve digital evidence (screenshots, emails, transaction records)",
                "2. File complaint with local Cyber Crime Cell or online portal",
                "3. Submit detailed complaint with all supporting digital evidence",
                "4. Provide access to affected accounts/devices for investigation",
                "5. Cooperate with cyber crime investigation team",
                "6. Attend hearings at designated cyber crime court",
                "7. Present technical evidence and expert testimony if required",
                "8. Follow court orders for recovery/compensation procedures"
            ],
            'personal_injury': [
                "1. Seek immediate medical attention and preserve medical records",
                "2. Document accident scene with photos and witness statements",
                "3. Report incident to police and obtain official accident report",
                "4. Notify insurance companies (yours and other party's) immediately",
                "5. Consult personal injury lawyer for case evaluation",
                "6. File insurance claims with comprehensive medical documentation",
                "7. Negotiate settlement with insurance companies through lawyer",
                "8. File civil lawsuit if fair settlement cannot be reached"
            ],
            'contract_dispute': [
                "1. Review contract terms and identify specific breach clauses",
                "2. Gather all contract-related documents and communications",
                "3. Send legal notice to defaulting party demanding performance",
                "4. Attempt negotiation and settlement through mutual discussion",
                "5. File civil suit in appropriate court for contract enforcement",
                "6. Present contract documents and evidence of breach in court",
                "7. Attend hearings and follow court procedures for resolution",
                "8. Receive court judgment for specific performance or damages"
            ],
            'elder_abuse': [
                "1. Document evidence of abuse (medical records, photos, witnesses)",
                "2. Contact Elder Helpline (14567) for immediate assistance",
                "3. File police complaint if physical/financial abuse is involved",
                "4. Approach Senior Citizen Tribunal for legal remedies",
                "5. Submit application with medical/financial evidence of abuse",
                "6. Attend tribunal hearings with supporting witnesses",
                "7. Present case for protection order or compensation",
                "8. Follow tribunal orders for elder protection and care"
            ],
            'immigration_law': [
                "1. Determine eligibility for desired immigration benefit or status",
                "2. Gather required documentation (passport, certificates, photos)",
                "3. Complete appropriate immigration forms accurately and completely",
                "4. Pay required government fees and submit application package",
                "5. Attend biometrics appointment at designated service center",
                "6. Participate in immigration interview if scheduled",
                "7. Respond promptly to any requests for additional evidence",
                "8. Receive decision and take appropriate next steps or appeals"
            ],
            'unknown': [
                "1. Consult with qualified legal professional for case assessment",
                "2. Gather all relevant documents and evidence related to issue",
                "3. Research applicable laws and legal precedents",
                "4. Determine appropriate legal forum or authority for complaint",
                "5. File formal complaint or petition with supporting documentation",
                "6. Follow prescribed legal procedures and attend required hearings",
                "7. Present case with evidence and legal arguments",
                "8. Receive legal decision and follow enforcement procedures"
            ]
        }

    def get_process_steps(self, domain: str) -> List[str]:
        """Get detailed process steps for a legal domain"""
        return self.process_mapping.get(domain, self.process_mapping['unknown'])

    def _get_criminal_law_route(self, query: str) -> str:
        """Get specific criminal law route based on crime type"""

        query_lower = query.lower()

        # Serious crimes requiring immediate action
        if any(word in query_lower for word in ['rape', 'murder', 'kidnap', 'assault', 'violence']):
            return "URGENT: Call 100 immediately, file FIR at nearest police station, seek medical help if needed"

        # Theft and robbery
        elif any(word in query_lower for word in ['robbery', 'theft', 'stolen', 'burglar']):
            return "File FIR immediately at nearest police station, provide list of stolen items with values"

        # Fraud and cheating
        elif any(word in query_lower for word in ['fraud', 'cheated', 'scam', 'deceived']):
            return "File complaint with Economic Offences Wing, gather all transaction evidence and documents"

        # Harassment cases
        elif any(word in query_lower for word in ['harass', 'threaten', 'intimidat', 'stalk']):
            return "File police complaint under IPC Section 506/509, document all incidents with evidence"

        # Cyber crimes
        elif any(word in query_lower for word in ['hacked', 'online', 'cyber', 'internet']):
            return "Report to Cyber Crime Cell, file complaint on cybercrime.gov.in, preserve digital evidence"

        # General criminal matters
        else:
            return "File police complaint (FIR) at nearest station, gather evidence, consult criminal lawyer"

    def generate_enhanced_fallback_route(self, domain: str, user_query: str) -> Tuple[str, str, float]:
        """Generate enhanced fallback route based on domain and query analysis"""

        query_lower = user_query.lower()

        # Domain-specific routes
        domain_routes = {
            'criminal_law': {
                'route': "File police complaint (FIR) at nearest station under relevant IPC sections",
                'timeline': "15-90 days",
                'success_rate': 0.70
            },
            'employment_law': {
                'route': "File complaint with labor commissioner or approach employment tribunal",
                'timeline': "60-180 days",
                'success_rate': 0.65
            },
            'cyber_crime': {
                'route': "Report to Cyber Crime Cell and file complaint on cybercrime.gov.in portal",
                'timeline': "30-120 days",
                'success_rate': 0.60
            },
            'family_law': {
                'route': "Approach family court or file petition under relevant family law provisions",
                'timeline': "90-365 days",
                'success_rate': 0.68
            },
            'consumer_complaint': {
                'route': "File complaint with consumer forum (district/state/national level)",
                'timeline': "45-180 days",
                'success_rate': 0.72
            },
            'tenant_rights': {
                'route': "File complaint with rent controller or approach civil court",
                'timeline': "60-240 days",
                'success_rate': 0.65
            }
        }

        # Check for urgency indicators
        urgency_keywords = ['emergency', 'immediate', 'urgent', 'threatening', 'violence', 'danger']
        is_urgent = any(keyword in query_lower for keyword in urgency_keywords)

        if is_urgent:
            return ("Contact emergency services (100/112) immediately, then file police complaint",
                   "Immediate-15 days", 0.80)

        # Use domain-specific route if available
        if domain in domain_routes:
            route_info = domain_routes[domain]
            return route_info['route'], route_info['timeline'], route_info['success_rate']

        # Default fallback with enhanced advice
        return ("Consult with qualified legal professional and consider filing appropriate complaint with relevant authorities",
               "30-180 days", 0.60)

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            'ml_classification': self.ml_available,
            'dataset_routes': self.routes_available,
            'constitutional_backing': self.constitutional_available,
            'queries_processed': getattr(self, 'session_count', 0)
        }


def create_working_enhanced_agent() -> WorkingEnhancedAgent:
    """Factory function to create working enhanced agent"""
    return WorkingEnhancedAgent()


def interactive_cli():
    """Interactive CLI for working enhanced agent"""
    
    safe_print("WORKING ENHANCED LEGAL AGENT")
    safe_print("=" * 50)
    safe_print("Simplified version with core 10/10 score functionality")
    safe_print("Type 'quit' to exit, 'status' for system status")
    safe_print("=" * 50)
    
    agent = create_working_enhanced_agent()
    
    while True:
        try:
            user_input = input("\nYour legal question: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'status':
                status = agent.get_system_status()
                safe_print(f"\nSystem Status:")
                for component, available in status.items():
                    safe_print(f"  {component}: {'Available' if available else 'Not Available'}")
                continue
            elif not user_input:
                continue
            
            # Process query
            response = agent.process_query(user_input)
            
            # Display response
            safe_print(f"\nEnhanced Legal Response:")
            safe_print(f"  Domain: {response.domain.title()} (Confidence: {response.confidence:.3f})")
            safe_print(f"  Legal Route: {response.legal_route}")
            safe_print(f"  Timeline: {response.timeline}")
            safe_print(f"  Success Rate: {response.success_rate:.1%}")

            # Constitutional backing - RESTORED
            if response.constitutional_backing:
                safe_print(f"  Constitutional Backing: {response.constitutional_backing[:100]}...")

            safe_print(f"  Response Time: {response.response_time:.2f}s")
            
        except KeyboardInterrupt:
            safe_print(f"\nGoodbye!")
            break
        except Exception as e:
            safe_print(f"Error: {e}")


# Test the working enhanced agent
if __name__ == "__main__":
    safe_print("WORKING ENHANCED LEGAL AGENT TEST")
    safe_print("=" * 50)

    agent = create_working_enhanced_agent()

    # Test queries
    test_queries = [
        "My landlord won't return my security deposit",
        "I bought a defective phone and want refund",
        "My elderly father is being abused",
        "I was wrongfully terminated from work"
    ]

    safe_print(f"\nTesting with sample queries:")
    safe_print("-" * 30)

    for query in test_queries:
        response = agent.process_query(query)
        safe_print(f"\nQuery: \"{query}\"")
        safe_print(f"Result: {response.domain} (confidence: {response.confidence:.3f})")
        safe_print(f"Timeline: {response.timeline}")

    # Start interactive CLI
    safe_print(f"\nStarting interactive CLI...")
    interactive_cli()
