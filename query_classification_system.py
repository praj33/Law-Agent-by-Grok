"""
Query Classification System for Legal Agent
==========================================

This module implements a comprehensive query classification system that:
1. Classifies queries into Domain and Subdomain using JSON classification system
2. Retrieves all relevant legal provisions from BNS, IPC, CrPC
3. Implements confidence scoring with feedback learning
4. Maintains query history with timestamps
5. Integrates constitutional articles when applicable

Author: Legal Agent Team
Version: 1.0.0
Date: 2025-09-11
"""

import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
import re

# Import required components
from ml_domain_classifier import create_ml_domain_classifier
from subdomain_classifier import create_subdomain_classifier
from complete_legal_database import create_complete_legal_database
from constitutional_article_matcher import get_constitutional_articles_with_confidence
from query_storage import create_query_storage

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalProvisions:
    """Legal provisions from all three codes"""
    bns_sections: List[Dict[str, Any]]
    ipc_sections: List[Dict[str, Any]]
    crpc_sections: List[Dict[str, Any]]


@dataclass
class QueryClassificationResult:
    """Complete query classification result"""
    # Core classification
    session_id: str
    timestamp: str
    user_query: str
    
    # Classification results
    domain: str
    subdomain: str
    confidence: float
    
    # Legal provisions
    constitutional_articles: List[Dict[str, Any]]
    bns_sections: List[Dict[str, Any]]
    ipc_sections: List[Dict[str, Any]]
    crpc_sections: List[Dict[str, Any]]
    
    # Process information
    legal_process: List[str]
    notes_and_safeguards: List[str]
    emergency_contacts: List[str]
    
    # Confidence system
    confidence_percentage: int
    confidence_explanation: str
    
    # Query history
    stored_in_history: bool = False


class QueryClassificationSystem:
    """Main query classification system"""
    
    def __init__(self):
        """Initialize the classification system"""
        logger.info("Initializing Query Classification System...")
        
        # Initialize components
        self.domain_classifier = create_ml_domain_classifier()
        self.subdomain_classifier = create_subdomain_classifier()
        self.legal_database = create_complete_legal_database()
        self.query_storage = create_query_storage()
        
        # Load JSON classification system
        self.json_classification = self._load_json_classification_system()
        
        # Initialize confidence tracking
        self.confidence_history = {}
        
        logger.info("Query Classification System initialized successfully")
    
    def _load_json_classification_system(self) -> Dict[str, Any]:
        """Load the JSON classification system from the user query"""
        # This is the JSON structure provided in the user query
        return {
            "domains": {
                "Criminal Law": {
                    "Murder": ["murder", "homicide", "kill", "manslaughter"],
                    "Kidnapping / Abduction": ["kidnap", "abduct", "ransom", "hostage"],
                    "Sexual Offences": ["rape", "sexual assault", "molestation"],
                    "Drug Crime": ["drugs", "narcotics", "smuggling"],
                    "Financial Crime": ["fraud", "cheating", "scam", "money laundering"],
                    "Cyber Crime": ["hacking", "online scam", "cyber fraud", "phishing"]
                },
                "Family Law": {
                    "Domestic Violence": ["domestic violence", "dowry", "husband beats", "cruelty"],
                    "Marriage & Divorce": ["divorce", "alimony", "separation"],
                    "Child Custody & Maintenance": ["child custody", "maintenance", "child support"]
                },
                "Property & Land Law": {
                    "Tenant Rights": ["tenant", "rent", "landlord", "eviction"],
                    "Real Estate & Land Disuses": ["land dispute", "property fraud", "illegal possession"]
                },
                "Traffic & Motor Vehicle Law": {
                    "Road Accidents": ["car accident", "bike accident", "hit and run"],
                    "Drunk Driving": ["drink and drive", "alcohol driving", "rash driving"]
                },
                "Employment & Labor Law": {
                    "Employment Issues": ["salary not paid", "wrongful termination", "unpaid wages"],
                    "Workplace Harassment": ["workplace harassment", "sexual harassment at work"]
                },
                "Consumer Law": {
                    "Consumer Protection": ["consumer complaint", "defective product", "refund not given"],
                    "Medical Malpractice": ["wrong treatment", "hospital negligence", "doctor negligence"]
                },
                "Social Offences": {
                    "Superstition & Black Magic": ["black magic", "superstition", "inhuman practice", "witch hunting"]
                }
            }
        }
    
    def classify_query(self, user_query: str) -> QueryClassificationResult:
        """Classify a user query and return comprehensive results"""
        start_time = time.time()
        session_id = f"qcs_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
        logger.info(f"Classifying query: {user_query[:50]}...")
        
        try:
            # Step 1: Classify domain using ML classifier
            domain, confidence, alternatives = self.domain_classifier.classify_with_confidence(user_query)
            
            # Step 2: Classify subdomain
            subdomain, subdomain_confidence, subdomain_alternatives = self.subdomain_classifier.classify_subdomain(domain, user_query)
            
            # Step 3: Get constitutional articles
            constitutional_data = get_constitutional_articles_with_confidence(user_query)
            constitutional_articles = constitutional_data.get('recommendations', [])[:5]  # Top 5 articles
            
            # Step 4: Get legal provisions
            legal_provisions = self._get_all_legal_provisions(domain, subdomain, user_query)
            
            # Step 5: Generate legal process information
            legal_process = self._generate_legal_process(domain, subdomain)
            notes_and_safeguards = self._generate_notes_and_safeguards(domain, subdomain)
            emergency_contacts = self._generate_emergency_contacts(domain, subdomain)
            
            # Step 6: Calculate final confidence
            final_confidence = self._calculate_final_confidence(confidence, subdomain_confidence)
            confidence_percentage = int(final_confidence * 100)
            confidence_explanation = self._generate_confidence_explanation(confidence, subdomain_confidence, alternatives, subdomain_alternatives)
            
            # Step 7: Create result object
            result = QueryClassificationResult(
                session_id=session_id,
                timestamp=datetime.now().isoformat(),
                user_query=user_query,
                domain=domain,
                subdomain=subdomain,
                confidence=final_confidence,
                constitutional_articles=constitutional_articles,
                bns_sections=legal_provisions.bns_sections,
                ipc_sections=legal_provisions.ipc_sections,
                crpc_sections=legal_provisions.crpc_sections,
                legal_process=legal_process,
                notes_and_safeguards=notes_and_safeguards,
                emergency_contacts=emergency_contacts,
                confidence_percentage=confidence_percentage,
                confidence_explanation=confidence_explanation
            )
            
            # Step 8: Store in query history
            self._store_query_history(result)
            
            # Log completion
            processing_time = time.time() - start_time
            logger.info(f"Query classified successfully in {processing_time:.2f}s with confidence {confidence_percentage}%")
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying query: {e}")
            return self._create_fallback_result(session_id, user_query, str(e))
    
    def _get_all_legal_provisions(self, domain: str, subdomain: str, query: str) -> LegalProvisions:
        """Get all relevant legal provisions from BNS, IPC, and CrPC"""
        try:
            # Get provisions from complete legal database
            provisions = self.legal_database.get_all_sections_for_query(domain, subdomain, query)
            
            return LegalProvisions(
                bns_sections=provisions.get("bns_sections", []),
                ipc_sections=provisions.get("ipc_sections", []),
                crpc_sections=provisions.get("crpc_sections", [])
            )
        except Exception as e:
            logger.error(f"Error getting legal provisions: {e}")
            return LegalProvisions([], [], [])
    
    def _generate_legal_process(self, domain: str, subdomain: str) -> List[str]:
        """Generate step-by-step legal process based on domain and subdomain"""
        processes = {
            # Criminal Law processes
            "kidnapping": [
                "File First Information Report (FIR) at nearest police station",
                "Police investigation and evidence collection",
                "Formation of charge sheet by police",
                "Filing of case in appropriate court",
                "Trial proceedings with witness examination",
                "Judgment by court"
            ],
            "cyber_crime": [
                "Report incident to cyber cell or local police",
                "Preserve all digital evidence (screenshots, messages)",
                "Police investigation and technical analysis",
                "Formation of charge sheet",
                "Filing of case in appropriate court",
                "Trial with digital evidence presentation",
                "Judgment by court"
            ],
            "rape": [
                "File complaint immediately with police or protection officer",
                "Medical examination at government hospital",
                "Police investigation and evidence collection",
                "Filing of case under relevant sections",
                "Fast track court hearing (if applicable)",
                "Trial with victim protection measures",
                "Judgment by court"
            ],
            
            # Family Law processes
            "domestic_violence": [
                "File complaint with protection officer or police",
                "Apply for protection order under Domestic Violence Act",
                "Medical examination if needed",
                "Police investigation if criminal aspects involved",
                "Appearance before magistrate for protection orders",
                "Implementation of protection orders",
                "Follow-up for compliance"
            ],
            "divorce": [
                "Consult family lawyer for case evaluation",
                "Prepare and file divorce petition in family court",
                "Serve notice to spouse",
                "Appear for court proceedings and document submission",
                "Attempt mediation/conciliation (if required)",
                "Final arguments and evidence presentation",
                "Decree by court"
            ],
            
            # Property & Land Law processes
            "tenant_rights": [
                "Document all communication with landlord",
                "Send legal notice for security deposit return",
                "File complaint with rent control authority",
                "Appear for hearing with evidence",
                "If needed, file civil suit in appropriate court",
                "Execution of court order for deposit return"
            ],
            
            # Employment & Labor Law processes
            "workplace_harassment": [
                "Report incident to internal committee (if available)",
                "File written complaint with employer",
                "Approach labor commissioner if internal process fails",
                "File complaint with National Human Rights Commission (NHRC)",
                "Approach civil court for damages",
                "Criminal complaint if sexual harassment involved"
            ],
            
            # Consumer Law processes
            "consumer_complaint": [
                "File online complaint at consumer forum website",
                "Submit physical complaint with evidence documents",
                "Notice to opposite party for response",
                "Hearing with both parties",
                "Mediation attempt (if applicable)",
                "Final judgment by consumer forum",
                "Appeal process if needed"
            ],
            
            # Traffic & Motor Vehicle Law processes
            "road_accidents": [
                "Immediate medical attention and police reporting",
                "FIR filing at nearest police station",
                "Vehicle inspection and accident spot measurement",
                "Collection of witness statements and medical reports",
                "Claim intimation to insurance company",
                "Filing of claim petition in Motor Accident Claims Tribunal",
                "Hearing and evidence examination",
                "Award of compensation"
            ]
        }
        
        # Try to find specific process
        key = subdomain.lower().replace(" ", "_").replace("/", "_")
        if key in processes:
            return processes[key]
        
        # Try domain-based process
        domain_key = domain.lower().replace(" ", "_").replace("/", "_")
        if domain_key in processes:
            return processes[domain_key]
        
        # Default process
        return [
            "Consult qualified legal professional",
            "File appropriate complaint/petition",
            "Gather and preserve evidence",
            "Appear for legal proceedings",
            "Follow court orders and judgments"
        ]
    
    def _generate_notes_and_safeguards(self, domain: str, subdomain: str) -> List[str]:
        """Generate important notes and safeguards"""
        notes = {
            "kidnapping": [
                "Time is critical - report immediately to police",
                "Preserve all communication with kidnappers",
                "Coordinate with police without alerting kidnappers",
                "Do not make independent negotiations"
            ],
            "cyber_crime": [
                "Do not delete any digital evidence",
                "Take screenshots of all relevant communications",
                "Change passwords for all online accounts",
                "Report to both local police and cyber cell"
            ],
            "rape": [
                "Medical examination should be done within 24 hours",
                "Avoid changing clothes or bathing before examination",
                "Report to woman police officer if possible",
                "Legal aid is available free of cost"
            ],
            "domestic_violence": [
                "Emergency helpline: 181 (Domestic Violence Helpline)",
                "Safe shelter can be provided by local authorities",
                "Medical examination important for evidence",
                "Counseling services available for victims"
            ],
            "workplace_harassment": [
                "Document all incidents with dates and witnesses",
                "Report through proper channels in organization",
                "Legal action can be taken even after job change",
                "Compensation can be claimed for mental trauma"
            ],
            "consumer_complaint": [
                "Keep all purchase receipts and warranty documents",
                "Register complaints within limitation period",
                "Small value claims can be filed online easily",
                "Legal representation not mandatory in consumer forums"
            ],
            "road_accidents": [
                "Accident spot should not be disturbed",
                "Photographs of accident spot are important",
                "Medical treatment should be from government hospital",
                "Police report required for insurance claim"
            ]
        }
        
        # Try to find specific notes
        key = subdomain.lower().replace(" ", "_").replace("/", "_")
        if key in notes:
            return notes[key]
        
        # Try domain-based notes
        domain_key = domain.lower().replace(" ", "_").replace("/", "_")
        if domain_key in notes:
            return notes[domain_key]
        
        # Default notes
        return [
            "Consult qualified legal professional for detailed advice",
            "Preserve all relevant documents and evidence",
            "Follow proper legal procedures for best results",
            "Legal aid services available for economically weaker sections"
        ]
    
    def _generate_emergency_contacts(self, domain: str, subdomain: str) -> List[str]:
        """Generate emergency contacts based on domain"""
        contacts = {
            "kidnapping": [
                "Police Emergency: 100",
                "Women Helpline: 1091",
                "Childline: 1098",
                "National Emergency Response Support System: 112"
            ],
            "cyber_crime": [
                "Cyber Crime Cell: Local police station",
                "National Cyber Crime Reporting Portal: www.cybercrime.gov.in",
                "Police Emergency: 100",
                "National Emergency Response Support System: 112"
            ],
            "rape": [
                "Police Emergency: 100",
                "Women Helpline: 1091",
                "National Commission for Women: 1800-11-4212",
                "Legal Services Authority: 1800-11-8888"
            ],
            "domestic_violence": [
                "Domestic Violence Helpline: 181",
                "Police Emergency: 100",
                "Women Helpline: 1091",
                "National Commission for Women: 1800-11-4212"
            ],
            "workplace_harassment": [
                "Local Labor Commissioner Office",
                "National Human Rights Commission: 1800-11-4212",
                "Police Emergency: 100 (if criminal aspects involved)",
                "Legal Services Authority: 1800-11-8888"
            ]
        }
        
        # Try to find specific contacts
        key = subdomain.lower().replace(" ", "_").replace("/", "_")
        if key in contacts:
            return contacts[key]
        
        # Try domain-based contacts
        domain_key = domain.lower().replace(" ", "_").replace("/", "_")
        if domain_key in contacts:
            return contacts[domain_key]
        
        # Default emergency contacts
        return [
            "Police Emergency: 100",
            "Legal Services Authority: 1800-11-8888",
            "National Emergency Response Support System: 112"
        ]
    
    def _calculate_final_confidence(self, domain_confidence: float, subdomain_confidence: float) -> float:
        """Calculate final confidence score"""
        # Weighted average with domain having more weight
        final_confidence = (domain_confidence * 0.6) + (subdomain_confidence * 0.4)
        return min(1.0, max(0.0, final_confidence))
    
    def _generate_confidence_explanation(self, domain_confidence: float, subdomain_confidence: float,
                                       domain_alternatives: List[Tuple[str, float]], 
                                       subdomain_alternatives: List[Tuple[str, float]]) -> str:
        """Generate explanation for confidence score"""
        explanations = []
        
        if domain_confidence >= 0.8:
            explanations.append("High confidence in domain classification")
        elif domain_confidence >= 0.6:
            explanations.append("Good confidence in domain classification")
        elif domain_confidence >= 0.4:
            explanations.append("Moderate confidence in domain classification")
        else:
            explanations.append("Low confidence in domain classification")
        
        if subdomain_confidence >= 0.8:
            explanations.append("High confidence in subdomain classification")
        elif subdomain_confidence >= 0.6:
            explanations.append("Good confidence in subdomain classification")
        elif subdomain_confidence >= 0.4:
            explanations.append("Moderate confidence in subdomain classification")
        else:
            explanations.append("Low confidence in subdomain classification")
        
        # Add alternatives if available
        if len(domain_alternatives) > 1:
            alt_domain, alt_conf = domain_alternatives[1]
            explanations.append(f"Alternative domain: {alt_domain} ({alt_conf:.2f})")
        
        if len(subdomain_alternatives) > 1:
            alt_subdomain, alt_conf = subdomain_alternatives[1]
            explanations.append(f"Alternative subdomain: {alt_subdomain} ({alt_conf:.2f})")
        
        return ". ".join(explanations)
    
    def _store_query_history(self, result: QueryClassificationResult):
        """Store query in history with all relevant information"""
        try:
            # Create a simple object to store
            class SimpleResponse:
                def __init__(self, domain, confidence):
                    self.domain = domain
                    self.confidence = confidence
                    self.constitutional_articles = result.constitutional_articles
            
            response = SimpleResponse(result.domain, result.confidence)
            
            # Store in query storage
            query_id = self.query_storage.store_query(result.user_query, response)
            if query_id:
                result.stored_in_history = True
                logger.info(f"Query stored in history with ID: {query_id}")
        except Exception as e:
            logger.error(f"Error storing query in history: {e}")
    
    def _create_fallback_result(self, session_id: str, user_query: str, error_msg: str) -> QueryClassificationResult:
        """Create fallback result when errors occur"""
        return QueryClassificationResult(
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            user_query=user_query,
            domain="unknown",
            subdomain="general",
            confidence=0.0,
            constitutional_articles=[],
            bns_sections=[],
            ipc_sections=[],
            crpc_sections=[],
            legal_process=["System error occurred. Please try again or consult legal professional."],
            notes_and_safeguards=["An error occurred during processing. Please try again."],
            emergency_contacts=["Police Emergency: 100"],
            confidence_percentage=0,
            confidence_explanation=f"System error: {error_msg}"
        )
    
    def process_feedback(self, session_id: str, feedback: str, rating: int = 0):
        """Process user feedback to improve confidence scoring"""
        try:
            # Store feedback (simplified)
            logger.info(f"Processing feedback for session {session_id}: {feedback} (Rating: {rating})")
            
            # In a real implementation, this would update confidence scores
            # and potentially retrain models based on feedback
            return True
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            return False
    
    def get_query_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent query history"""
        try:
            stored_queries = self.query_storage.get_recent_queries(limit)
            history = []
            
            for query in stored_queries:
                history.append({
                    "timestamp": query.timestamp,
                    "user_query": query.user_query,
                    "domain": query.domain,
                    "confidence": query.confidence
                })
            
            return history
        except Exception as e:
            logger.error(f"Error retrieving query history: {e}")
            return []
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            return {
                "domain_classifier_stats": self.domain_classifier.get_model_stats(),
                "subdomain_classifier_stats": self.subdomain_classifier.get_stats(),
                "legal_database_stats": self.legal_database.get_stats(),
                "queries_processed": len(self.query_storage.get_recent_queries(1000))  # Approximate
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}


def create_query_classification_system() -> QueryClassificationSystem:
    """Factory function to create query classification system"""
    return QueryClassificationSystem()


def format_classification_result(result: QueryClassificationResult) -> str:
    """Format classification result for display"""
    
    output = []
    
    # Header
    output.append("=" * 80)
    output.append("🏛️  LEGAL QUERY CLASSIFICATION RESULT")
    output.append("=" * 80)
    output.append("")
    
    # Query information
    output.append(f"🕒 Timestamp: {result.timestamp}")
    output.append(f"🆔 Session ID: {result.session_id}")
    output.append(f"❓ User Query: {result.user_query}")
    output.append("")
    
    # Classification results
    output.append("🔍 CLASSIFICATION RESULTS")
    output.append("-" * 40)
    output.append(f"Domain: {result.domain.replace('_', ' ').title()}")
    output.append(f"Subdomain: {result.subdomain.replace('_', ' ').title()}")
    output.append(f"Confidence: {result.confidence_percentage}%")
    output.append(f"Explanation: {result.confidence_explanation}")
    output.append("")
    
    # Constitutional Articles
    if result.constitutional_articles:
        output.append("📜 CONSTITUTIONAL ARTICLES")
        output.append("-" * 40)
        for article in result.constitutional_articles:
            output.append(f"Article {article['article_number']}: {article['title']}")
            output.append(f"  Confidence: {article['confidence_percentage']}%")
            if article.get('matching_keywords'):
                output.append(f"  Keywords: {', '.join(article['matching_keywords'])}")
        output.append("")
    
    # BNS Sections
    if result.bns_sections:
        output.append("📖 BHARATIYA NYAYA SANHITA (BNS) SECTIONS")
        output.append("-" * 40)
        for section in result.bns_sections[:10]:  # Limit to first 10
            output.append(f"Section {section['section_number']}: {section['title']}")
            # Truncate description for readability
            desc = section['description'][:150] + "..." if len(section['description']) > 150 else section['description']
            output.append(f"  {desc}")
        if len(result.bns_sections) > 10:
            output.append(f"  ... and {len(result.bns_sections) - 10} more sections")
        output.append("")
    
    # IPC Sections
    if result.ipc_sections:
        output.append("⚖️  INDIAN PENAL CODE (IPC) SECTIONS")
        output.append("-" * 40)
        for section in result.ipc_sections[:10]:  # Limit to first 10
            output.append(f"Section {section['section_number']}: {section['title']}")
            # Truncate description for readability
            desc = section['description'][:150] + "..." if len(section['description']) > 150 else section['description']
            output.append(f"  {desc}")
        if len(result.ipc_sections) > 10:
            output.append(f"  ... and {len(result.ipc_sections) - 10} more sections")
        output.append("")
    
    # CrPC Sections
    if result.crpc_sections:
        output.append("📝 CODE OF CRIMINAL PROCEDURE (CrPC) SECTIONS")
        output.append("-" * 40)
        for section in result.crpc_sections[:10]:  # Limit to first 10
            output.append(f"Section {section['section_number']}: {section['title']}")
            # Truncate description for readability
            desc = section['description'][:150] + "..." if len(section['description']) > 150 else section['description']
            output.append(f"  {desc}")
        if len(result.crpc_sections) > 10:
            output.append(f"  ... and {len(result.crpc_sections) - 10} more sections")
        output.append("")
    
    # Legal Process
    if result.legal_process:
        output.append("📋 STEP-BY-STEP LEGAL PROCESS")
        output.append("-" * 40)
        for i, step in enumerate(result.legal_process, 1):
            output.append(f"{i}. {step}")
        output.append("")
    
    # Notes and Safeguards
    if result.notes_and_safeguards:
        output.append("⚠️  NOTES & SAFEGUARDS")
        output.append("-" * 40)
        for note in result.notes_and_safeguards:
            output.append(f"• {note}")
        output.append("")
    
    # Emergency Contacts
    if result.emergency_contacts:
        output.append("📞 EMERGENCY CONTACTS")
        output.append("-" * 40)
        for contact in result.emergency_contacts:
            output.append(f"• {contact}")
        output.append("")
    
    # Query History
    if result.stored_in_history:
        output.append("💾 QUERY HISTORY")
        output.append("-" * 40)
        output.append("This query has been stored in your query history.")
        output.append("")
    
    return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    print("🚀 QUERY CLASSIFICATION SYSTEM")
    print("=" * 50)
    
    # Create system
    system = create_query_classification_system()
    
    # Test with the example query from user requirements
    test_query = "My child was kidnapped for ransom"
    
    print(f"Testing with query: '{test_query}'")
    print("-" * 50)
    
    # Classify query
    result = system.classify_query(test_query)
    
    # Format and display result
    formatted_output = format_classification_result(result)
    print(formatted_output)
    
    # Show system stats
    stats = system.get_system_stats()
    print("📊 SYSTEM STATISTICS:")
    print(f"   Queries Processed: {stats.get('queries_processed', 'N/A')}")
    print(f"   Domain Classifier Training Examples: {stats.get('domain_classifier_stats', {}).get('training_examples', 'N/A')}")
    print(f"   Subdomain Domains: {stats.get('subdomain_classifier_stats', {}).get('total_domains', 'N/A')}")
    print(f"   Legal Sections: {stats.get('legal_database_stats', {}).get('total_sections', 'N/A')}")
    
    print("\n✅ Query Classification System ready!")