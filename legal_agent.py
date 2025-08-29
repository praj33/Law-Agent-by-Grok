"""
Legal Agent - Integrated Master Class
=====================================

This module provides a comprehensive legal assistant agent that integrates:
- Domain classification using TF-IDF vectorization
- Legal route recommendation engine
- Process step explanation
- Legal glossary term identification
- Feedback collection and learning system

Author: Legal Agent Team
Version: 1.0.0
Date: 2025-07-22
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import json
import datetime
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Import data integration module
try:
    from data_integration import CrimeDataAnalyzer, EnhancedLegalRouteEngine, create_enhanced_legal_system
    DATA_INTEGRATION_AVAILABLE = True
except ImportError:
    DATA_INTEGRATION_AVAILABLE = False

try:
    from constitutional_integration import ConstitutionalAdvisor, create_constitutional_advisor
    CONSTITUTIONAL_INTEGRATION_AVAILABLE = True
except ImportError:
    CONSTITUTIONAL_INTEGRATION_AVAILABLE = False
    print("Warning: Data integration module not available. Running in basic mode.")


@dataclass
class LegalQueryInput:
    """Input structure for legal queries"""
    user_input: str
    feedback: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class LegalAgentResponse:
    """Complete response structure from the legal agent"""
    domain: str
    confidence: float
    legal_route: str
    timeline: str
    outcome: str
    process_steps: List[str]
    glossary: Dict[str, str]
    session_id: str
    timestamp: str
    raw_query: str
    location_insights: Optional[Dict[str, Any]] = None
    data_driven_advice: Optional[str] = None
    risk_assessment: Optional[str] = None
    constitutional_backing: Optional[str] = None
    constitutional_articles: Optional[List[Dict]] = None
    legal_acts: Optional[List[Dict[str, Any]]] = None  # Add legal acts field

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert response to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


class DomainClassifier:
    """Handles legal domain classification using TF-IDF similarity"""
    
    def __init__(self):
        self.domain_data = pd.DataFrame({
            'domain': [
                'tenant rights', 
                'consumer complaint', 
                'family law',
                'employment law',
                'contract dispute',
                'personal injury',
                'criminal law',
                'immigration law',
                'elder abuse',
                'cyber crime'
            ],
            'example_query': [
                'my landlord is not returning deposit security rent eviction notice',
                'i received a faulty product defective warranty refund return consumer complaint filing defective goods service',
                'i want a divorce from my husband custody child support alimony',
                'my employer fired me wrongfully terminated harassment discrimination',
                'breach of contract agreement violation terms conditions',
                'car accident injury compensation medical bills insurance claim',
                'arrested charged crime criminal defense lawyer bail',
                'visa application green card citizenship immigration status',
                'elderly abuse senior citizen harassment neglect financial exploitation',
                'online fraud cyber crime hacking identity theft digital scam phone hacked malware computer virus cyberbullying social media stalking email compromise data breach mobile security'
            ]
        })
        
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        self.X = self.vectorizer.fit_transform(self.domain_data['example_query'])
        self.confidence_threshold = 0.12  # Lowered for better coverage
    
    def classify(self, user_query: str) -> Tuple[str, float]:
        """
        Classify user query into legal domain

        Args:
            user_query: Raw user input

        Returns:
            Tuple of (domain, confidence_score)
        """
        cleaned_query = self._clean_query(user_query)
        user_vec = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(user_vec, self.X)

        best_match_idx = similarities.argmax()
        confidence = float(similarities[0][best_match_idx])

        if confidence < self.confidence_threshold:
            return "unknown", confidence

        domain = self.domain_data['domain'].iloc[best_match_idx]
        return domain, confidence

    def extract_location(self, user_query: str) -> Optional[str]:
        """Extract location information from user query"""
        # Common Indian state/city patterns
        location_patterns = [
            r'\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\bfrom\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\bat\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b(Delhi|Mumbai|Kolkata|Chennai|Bangalore|Hyderabad|Pune|Ahmedabad)\b',
            r'\b([A-Z][a-z]+\s+Pradesh|[A-Z][a-z]+\s+Nadu)\b'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, user_query, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None
    
    def _clean_query(self, query: str) -> str:
        """Clean and preprocess user query"""
        return query.strip().lower()
    
    def add_training_example(self, domain: str, example_query: str):
        """Add new training example to improve classification"""
        new_row = pd.DataFrame({
            'domain': [domain],
            'example_query': [example_query]
        })
        self.domain_data = pd.concat([self.domain_data, new_row], ignore_index=True)
        # Retrain the vectorizer
        self.X = self.vectorizer.fit_transform(self.domain_data['example_query'])


class LegalRouteEngine:
    """Provides legal route recommendations based on domain"""
    
    def __init__(self):
        self.route_mapping = {
            'tenant rights': {
                'summary': 'Send legal notice to landlord and approach rent tribunal or housing court.',
                'timeline': '2-3 months',
                'outcome': 'Deposit refund, rent reduction, or lease termination.',
                'urgency': 'medium',
                'cost_estimate': '$200-$800'
            },
            'consumer complaint': {
                'summary': 'File complaint in consumer forum or small claims court.',
                'timeline': '3-6 months',
                'outcome': 'Replacement, refund, or compensation for damages.',
                'urgency': 'low',
                'cost_estimate': '$50-$300'
            },
            'family law': {
                'summary': 'File divorce petition in family court with proper documentation.',
                'timeline': '6 months to 2 years',
                'outcome': 'Legal separation, child custody arrangement, alimony if applicable.',
                'urgency': 'high',
                'cost_estimate': '$1,500-$5,000'
            },
            'employment law': {
                'summary': 'File complaint with EEOC or state labor department.',
                'timeline': '3-12 months',
                'outcome': 'Compensation, reinstatement, or policy changes.',
                'urgency': 'high',
                'cost_estimate': '$500-$3,000'
            },
            'contract dispute': {
                'summary': 'Attempt mediation first, then consider litigation.',
                'timeline': '2-8 months',
                'outcome': 'Contract enforcement, damages, or settlement.',
                'urgency': 'medium',
                'cost_estimate': '$800-$4,000'
            },
            'personal injury': {
                'summary': 'Document injuries, gather evidence, file insurance claim.',
                'timeline': '6 months to 3 years',
                'outcome': 'Medical expenses coverage, pain and suffering compensation.',
                'urgency': 'high',
                'cost_estimate': '$1,000-$10,000+'
            },
            'criminal law': {
                'summary': 'Hire criminal defense attorney immediately.',
                'timeline': '3 months to 2 years',
                'outcome': 'Reduced charges, plea bargain, or case dismissal.',
                'urgency': 'critical',
                'cost_estimate': '$2,000-$15,000+'
            },
            'immigration law': {
                'summary': 'Consult immigration attorney and file appropriate applications.',
                'timeline': '6 months to 5 years',
                'outcome': 'Visa approval, status adjustment, or citizenship.',
                'urgency': 'high',
                'cost_estimate': '$1,500-$8,000'
            },
            'elder abuse': {
                'summary': 'File complaint under Maintenance and Welfare of Parents and Senior Citizens Act, 2007.',
                'timeline': '2-6 months',
                'outcome': 'Protection order, maintenance, or criminal prosecution.',
                'urgency': 'high',
                'cost_estimate': '$300-$2,000'
            },
            'cyber crime': {
                'summary': 'Report to Cyber Crime Cell and file complaint under IT Act, 2000.',
                'timeline': '1-8 months',
                'outcome': 'Investigation, recovery of funds, or prosecution.',
                'urgency': 'high',
                'cost_estimate': '$200-$1,500'
            },
            'unknown': {
                'summary': 'No specific legal route identified. Consult with a general practice attorney.',
                'timeline': 'N/A',
                'outcome': 'Professional legal assessment needed.',
                'urgency': 'medium',
                'cost_estimate': '$200-$500 (consultation)'
            }
        }
    
    def get_route(self, domain: str) -> Dict[str, str]:
        """Get legal route information for a domain"""
        return self.route_mapping.get(domain, self.route_mapping['unknown'])
    
    def add_route(self, domain: str, route_info: Dict[str, str]):
        """Add new legal route for a domain"""
        self.route_mapping[domain] = route_info


class ProcessExplainer:
    """Explains step-by-step legal processes for different domains"""

    def __init__(self):
        self.process_mapping = {
            'tenant rights': [
                "1. Document the issue (photos, receipts, communications)",
                "2. Review your lease agreement and local tenant laws",
                "3. Send written notice to landlord (certified mail)",
                "4. Wait for landlord response (typically 30 days)",
                "5. File complaint with local rent tribunal/housing court",
                "6. Attend mediation session if required",
                "7. Present evidence at hearing",
                "8. Receive tribunal decision and enforcement"
            ],
            'consumer complaint': [
                "1. Gather all receipts, warranties, and documentation",
                "2. Contact the business directly to resolve the issue",
                "3. File complaint with Better Business Bureau",
                "4. Submit complaint to consumer protection agency",
                "5. File case in small claims court if necessary",
                "6. Prepare evidence and witness statements",
                "7. Attend court hearing and present case",
                "8. Collect judgment if successful"
            ],
            'family law': [
                "1. Consult with a family law attorney",
                "2. Gather financial documents and records",
                "3. File divorce petition with family court",
                "4. Serve papers to spouse through proper channels",
                "5. Attend mandatory mediation sessions",
                "6. Negotiate custody and asset division",
                "7. Attend court hearings as scheduled",
                "8. Finalize divorce decree and arrangements"
            ],
            'employment law': [
                "1. Document all incidents (dates, witnesses, evidence)",
                "2. Review employee handbook and company policies",
                "3. File internal complaint with HR department",
                "4. File complaint with EEOC or state agency",
                "5. Participate in investigation process",
                "6. Consider mediation or settlement discussions",
                "7. File lawsuit if administrative remedies fail",
                "8. Proceed through litigation process"
            ],
            'contract dispute': [
                "1. Review contract terms and identify breach",
                "2. Gather evidence of performance and damages",
                "3. Send formal demand letter to other party",
                "4. Attempt good faith negotiations",
                "5. Consider alternative dispute resolution (mediation)",
                "6. File lawsuit if settlement not reached",
                "7. Engage in discovery process",
                "8. Proceed to trial or arbitration"
            ],
            'personal injury': [
                "1. Seek immediate medical attention",
                "2. Document the accident scene and injuries",
                "3. Report incident to relevant authorities",
                "4. Notify insurance companies",
                "5. Consult with personal injury attorney",
                "6. File insurance claims and gather medical records",
                "7. Negotiate settlement with insurance companies",
                "8. File lawsuit if fair settlement not offered"
            ],
            'criminal law': [
                "1. Exercise right to remain silent",
                "2. Request attorney immediately",
                "3. Do not discuss case with anyone except attorney",
                "4. Attend arraignment and enter plea",
                "5. Participate in discovery process",
                "6. Consider plea bargain negotiations",
                "7. Prepare for trial if necessary",
                "8. Appeal if convicted and grounds exist"
            ],
            'immigration law': [
                "1. Determine eligibility for desired immigration benefit",
                "2. Gather required documentation and evidence",
                "3. Complete and file appropriate forms",
                "4. Pay required fees and submit application",
                "5. Attend biometrics appointment if required",
                "6. Participate in interview process",
                "7. Respond to any requests for additional evidence",
                "8. Receive decision and take appropriate next steps"
            ],
            'elder abuse': [
                "1. Document all incidents of abuse or neglect",
                "2. Ensure immediate safety of the senior citizen",
                "3. Report to local police if criminal activity involved",
                "4. File complaint with Senior Citizens Tribunal",
                "5. Gather medical records and witness statements",
                "6. Apply for protection order if necessary",
                "7. Attend tribunal hearings and present evidence",
                "8. Follow up on tribunal orders and enforcement"
            ],
            'cyber crime': [
                "1. Preserve all digital evidence (screenshots, emails, messages)",
                "2. Report immediately to local Cyber Crime Cell",
                "3. File FIR at nearest police station",
                "4. Submit complaint on National Cyber Crime Portal",
                "5. Freeze affected bank accounts if financial fraud",
                "6. Cooperate with investigation agencies",
                "7. Provide additional evidence as requested",
                "8. Follow up on case progress and recovery"
            ],
            'unknown': [
                "1. Identify the specific legal issue involved",
                "2. Research applicable laws and regulations",
                "3. Consult with appropriate legal professional",
                "4. Follow attorney's guidance for next steps"
            ]
        }

    def get_process_steps(self, domain: str) -> List[str]:
        """Get process steps for a legal domain"""
        return self.process_mapping.get(domain, self.process_mapping['unknown'])

    def add_process(self, domain: str, steps: List[str]):
        """Add new process steps for a domain"""
        self.process_mapping[domain] = steps


class GlossaryEngine:
    """Identifies and explains legal terms found in queries and responses"""

    def __init__(self):
        self.glossary_db = {
            'legal notice': 'A formal written communication from one party to another regarding legal matters.',
            'tribunal': 'A special court or judicial body that handles particular types of legal matters.',
            'alimony': 'Financial support paid by one spouse to another after divorce or separation.',
            'consumer forum': 'A specialized court that handles cases related to consumer complaints and disputes.',
            'petition': 'A formal written request submitted to a court asking for specific legal action.',
            'mediation': 'A form of alternative dispute resolution where a neutral third party helps resolve conflicts.',
            'arbitration': 'A method of dispute resolution where an arbitrator makes a binding decision.',
            'discovery': 'The pre-trial process where parties exchange information and evidence.',
            'plaintiff': 'The person who brings a legal action or lawsuit against another party.',
            'defendant': 'The person or entity being sued or accused in a legal proceeding.',
            'settlement': 'An agreement between parties to resolve a dispute without going to trial.',
            'damages': 'Monetary compensation awarded to a party who has suffered loss or injury.',
            'injunction': 'A court order requiring someone to do or stop doing a specific action.',
            'liability': 'Legal responsibility for one\'s actions or omissions that cause harm to others.',
            'negligence': 'Failure to exercise reasonable care, resulting in damage or injury to another.',
            'breach of contract': 'Failure to perform any duty or obligation specified in a contract.',
            'statute of limitations': 'The time limit within which a legal action must be filed.',
            'jurisdiction': 'The authority of a court to hear and decide a particular type of case.',
            'subpoena': 'A legal document requiring someone to appear in court or produce documents.',
            'deposition': 'Sworn testimony taken outside of court during the discovery process.',
            'affidavit': 'A written statement made under oath and signed before a notary public.',
            'power of attorney': 'A legal document giving someone authority to act on another\'s behalf.',
            'custody': 'Legal responsibility for the care and control of a child or dependent.',
            'garnishment': 'A legal process to collect debt by taking money from wages or bank accounts.',
            'lien': 'A legal claim against property to secure payment of a debt or obligation.',
            'probate': 'The legal process of administering a deceased person\'s estate.',
            'tort': 'A civil wrong that causes harm to another person, excluding breach of contract.',
            'felony': 'A serious crime typically punishable by imprisonment for more than one year.',
            'misdemeanor': 'A less serious crime typically punishable by fine or short-term imprisonment.',
            'bail': 'Money paid to secure the release of an accused person pending trial.',
            'plea bargain': 'An agreement where a defendant pleads guilty to a lesser charge.',
            'appeal': 'A request to a higher court to review and change a lower court\'s decision.',
            'warrant': 'A legal document authorizing police to make an arrest or conduct a search.',
            'eviction': 'The legal process of removing a tenant from rental property.',
            'foreclosure': 'The legal process by which a lender takes possession of mortgaged property.',
            'bankruptcy': 'A legal proceeding for individuals or businesses unable to pay their debts.',
            'class action': 'A lawsuit filed by one or more people on behalf of a larger group.',
            'contingency fee': 'A fee arrangement where the lawyer is paid only if the case is won.'
        }

    def find_terms(self, text: str) -> Dict[str, str]:
        """
        Find legal terms in text and return their definitions

        Args:
            text: Text to search for legal terms

        Returns:
            Dictionary of found terms and their definitions
        """
        found_terms = {}
        text_lower = text.lower()

        for term, definition in self.glossary_db.items():
            if term in text_lower:
                found_terms[term] = definition

        return found_terms

    def add_term(self, term: str, definition: str):
        """Add new term to glossary"""
        self.glossary_db[term.lower()] = definition

    def get_all_terms(self) -> Dict[str, str]:
        """Get all terms in glossary"""
        return self.glossary_db.copy()


class FeedbackSystem:
    """Collects and processes user feedback for continuous improvement"""

    def __init__(self, feedback_file: str = 'feedback.csv'):
        self.feedback_file = feedback_file
        self._ensure_feedback_file_exists()

    def _ensure_feedback_file_exists(self):
        """Create feedback file if it doesn't exist"""
        feedback_path = Path(self.feedback_file)
        if not feedback_path.exists():
            with open(self.feedback_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'query', 'domain', 'feedback', 'session_id'])

    def collect_feedback(self, query: str, domain: str, feedback: str, session_id: str = None):
        """
        Collect and store user feedback

        Args:
            query: User's original query
            domain: Classified legal domain
            feedback: User's feedback (helpful, not helpful, etc.)
            session_id: Unique session identifier
        """
        timestamp = datetime.datetime.now().isoformat()

        with open(self.feedback_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, query, domain, feedback, session_id])

    def get_feedback_stats(self) -> Dict[str, Any]:
        """
        Calculate feedback statistics

        Returns:
            Dictionary with feedback statistics
        """
        try:
            df = pd.read_csv(self.feedback_file)

            # Basic stats
            total_feedback = len(df)
            domains = df['domain'].value_counts().to_dict()
            feedback_types = df['feedback'].value_counts().to_dict()

            # Calculate positive feedback percentage
            positive_feedback = df[df['feedback'].str.contains('helpful|good|yes', case=False, na=False)]
            positive_percentage = len(positive_feedback) / total_feedback * 100 if total_feedback > 0 else 0

            # Domain-specific feedback
            domain_feedback = {}
            for domain in domains.keys():
                domain_df = df[df['domain'] == domain]
                domain_positive = domain_df[domain_df['feedback'].str.contains('helpful|good|yes', case=False, na=False)]
                domain_percentage = len(domain_positive) / len(domain_df) * 100 if len(domain_df) > 0 else 0
                domain_feedback[domain] = {
                    'total': len(domain_df),
                    'positive_percentage': domain_percentage
                }

            return {
                'total_feedback': total_feedback,
                'domains': domains,
                'feedback_types': feedback_types,
                'positive_percentage': positive_percentage,
                'domain_feedback': domain_feedback,
                'recent_feedback': df.tail(10).to_dict('records')
            }
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return {
                'total_feedback': 0,
                'domains': {},
                'feedback_types': {},
                'positive_percentage': 0,
                'domain_feedback': {},
                'recent_feedback': []
            }

    def export_feedback(self, output_file: str = 'feedback_export.json'):
        """Export feedback data to JSON file"""
        try:
            df = pd.read_csv(self.feedback_file)
            feedback_data = df.to_dict('records')

            with open(output_file, 'w') as f:
                json.dump(feedback_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error exporting feedback: {e}")
            return False


class LegalAgent:
    """
    Integrated legal agent that combines all components:
    - Domain classification
    - Legal route recommendation
    - Process explanation
    - Glossary term identification
    - Feedback collection
    - Data-driven insights (when available)
    """

    def __init__(self, feedback_file: str = 'feedback.csv', enable_data_integration: bool = True):
        """Initialize the legal agent with all components"""
        self.domain_classifier = DomainClassifier()
        self.route_engine = LegalRouteEngine()
        self.process_explainer = ProcessExplainer()
        self.glossary_engine = GlossaryEngine()
        self.feedback_system = FeedbackSystem(feedback_file)

        # Initialize data integration if available
        self.data_integration_enabled = False
        self.crime_analyzer = None
        self.enhanced_route_engine = None

        if enable_data_integration and DATA_INTEGRATION_AVAILABLE:
            try:
                self.crime_analyzer, self.enhanced_route_engine = create_enhanced_legal_system()
                self.data_integration_enabled = True
                print("Data integration enabled with crime statistics")
            except Exception as e:
                print(f"Data integration failed: {e}")

        # Initialize constitutional integration
        self.constitutional_integration_enabled = False
        self.constitutional_advisor = None

        if CONSTITUTIONAL_INTEGRATION_AVAILABLE:
            try:
                self.constitutional_advisor = create_constitutional_advisor()
                self.constitutional_integration_enabled = True
                print("Legal agent with constitutional integration enabled")
            except Exception as e:
                print(f"Constitutional integration failed: {e}")
                self.data_integration_enabled = False

    def process_query(self, query_input: LegalQueryInput) -> LegalAgentResponse:
        """
        Process a legal query and generate a comprehensive response

        Args:
            query_input: LegalQueryInput object with user query and optional feedback

        Returns:
            LegalAgentResponse with all response components
        """
        # Generate session ID and timestamp if not provided
        session_id = query_input.session_id or self._generate_session_id()
        timestamp = query_input.timestamp or datetime.datetime.now().isoformat()

        # Extract location from query
        location = self.domain_classifier.extract_location(query_input.user_input)

        # Classify domain
        domain, confidence = self.domain_classifier.classify(query_input.user_input)

        # Get legal route (enhanced if data integration available)
        if self.data_integration_enabled and domain in ['elder abuse', 'criminal law']:
            route = self.enhanced_route_engine.get_enhanced_route(domain, location, query_input.user_input)
        else:
            route = self.route_engine.get_route(domain)

        # Get process steps
        process_steps = self.process_explainer.get_process_steps(domain)

        # Find glossary terms
        combined_text = query_input.user_input + ' ' + route['summary']
        glossary = self.glossary_engine.find_terms(combined_text)

        # Get location-based insights if available
        location_insights = None
        data_driven_advice = None
        risk_assessment = None

        if self.data_integration_enabled and location:
            if 'senior' in query_input.user_input.lower() or 'elder' in query_input.user_input.lower():
                location_insights = self.crime_analyzer.get_location_based_advice(location, 'senior_citizen_abuse')
                if location_insights.get('location_found'):
                    data_driven_advice = location_insights['advice']
                    risk_assessment = location_insights['risk_level']

        # Get constitutional backing with enhanced legal acts if available
        constitutional_backing = None
        constitutional_articles = None
        legal_acts = None

        if self.constitutional_integration_enabled and domain != 'unknown':
            try:
                constitutional_info = self.constitutional_advisor.get_constitutional_backing(domain, query_input.user_input)
                constitutional_backing = constitutional_info['constitutional_basis']

                # Process enhanced constitutional articles and legal acts
                detailed = constitutional_info.get('articles')
                if detailed:
                    constitutional_articles = [
                        {
                            'article_number': a.get('article_number'),
                            'title': a.get('title'),
                            'summary': a.get('content_summary'),
                            'relevance_type': a.get('relevance_type', 'RELEVANT'),
                            'is_primary': a.get('is_primary', False)
                        }
                        for a in detailed[:4]  # Limit to top 4 articles
                    ]
                else:
                    # Fallback to basic relevant articles (no misleading confidence)
                    constitutional_articles = [
                        {
                            'article_number': article.article_number,
                            'title': article.clean_title,
                            'summary': article.summary,
                            'relevance_type': 'RELEVANT'
                        }
                        for article in constitutional_info.get('relevant_articles', [])[:3]
                    ]
                
                # Extract legal acts if available (NEW FEATURE)
                if 'legal_acts' in constitutional_info:
                    legal_acts = constitutional_info['legal_acts']
                    
            except Exception as e:
                print(f"⚠️ Constitutional backing failed: {e}")

        # Store feedback if provided
        if query_input.feedback:
            self.feedback_system.collect_feedback(
                query_input.user_input,
                domain,
                query_input.feedback,
                session_id
            )

        # Create response with enhanced legal backing
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
            risk_assessment=risk_assessment,
            constitutional_backing=constitutional_backing,
            constitutional_articles=constitutional_articles,
            legal_acts=legal_acts  # Add legal acts to response
        )

        return response

    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = np.random.randint(1000, 9999)
        return f"session_{timestamp}_{random_suffix}"

    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        return self.feedback_system.get_feedback_stats()

    def add_training_example(self, domain: str, example_query: str):
        """Add training example to improve classification"""
        self.domain_classifier.add_training_example(domain, example_query)

    def add_glossary_term(self, term: str, definition: str):
        """Add new term to glossary"""
        self.glossary_engine.add_term(term, definition)

    def add_legal_route(self, domain: str, route_info: Dict[str, str]):
        """Add new legal route for a domain"""
        self.route_engine.add_route(domain, route_info)

    def add_process_steps(self, domain: str, steps: List[str]):
        """Add new process steps for a domain"""
        self.process_explainer.add_process(domain, steps)


# Convenience function for quick usage
def create_legal_agent(feedback_file: str = 'feedback.csv') -> LegalAgent:
    """
    Create and return a configured LegalAgent instance

    Args:
        feedback_file: Path to feedback CSV file

    Returns:
        Configured LegalAgent instance
    """
    return LegalAgent(feedback_file)


def quick_query(user_input: str, feedback: str = None) -> Dict[str, Any]:
    """
    Quick query function for simple usage

    Args:
        user_input: User's legal query
        feedback: Optional feedback on previous response

    Returns:
        Dictionary with agent response
    """
    agent = create_legal_agent()
    query = LegalQueryInput(user_input=user_input, feedback=feedback)
    response = agent.process_query(query)
    return response.to_dict()


if __name__ == "__main__":
    # Example usage
    agent = create_legal_agent()

    # Test query
    test_query = LegalQueryInput(
        user_input="My landlord won't return my security deposit and it's been 3 months",
        feedback=None
    )

    response = agent.process_query(test_query)
    print("Legal Agent Response:")
    print("=" * 50)
    print(response.to_json())

    # Test feedback
    feedback_query = LegalQueryInput(
        user_input="Same query as before",
        feedback="This was very helpful, thank you!"
    )

    agent.process_query(feedback_query)

    # Show feedback stats
    print("\nFeedback Statistics:")
    print("=" * 50)
    stats = agent.get_feedback_stats()
    print(json.dumps(stats, indent=2))
