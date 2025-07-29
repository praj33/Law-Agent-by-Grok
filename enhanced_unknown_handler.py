"""
Enhanced Unknown Domain Handler
==============================

Improves handling of queries that fall outside the 10 trained domains
by providing intelligent fallbacks and domain mapping suggestions.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class UnknownQueryAnalysis:
    """Analysis result for unknown domain queries"""
    suggested_domains: List[Tuple[str, float, str]]  # (domain, confidence, reason)
    harassment_type: Optional[str]
    urgency_level: str  # low, medium, high, emergency
    recommended_actions: List[str]
    constitutional_relevance: List[str]
    specialized_advice: str

class EnhancedUnknownHandler:
    """Enhanced handler for unknown domain queries"""
    
    def __init__(self):
        """Initialize enhanced unknown handler"""
        
        # Harassment-specific patterns
        self.harassment_patterns = {
            'sexual_harassment': [
                'sexual', 'inappropriate touching', 'unwanted advances', 'molest', 
                'eve teasing', 'stalking', 'obscene', 'indecent'
            ],
            'workplace_harassment': [
                'boss', 'supervisor', 'colleague', 'office', 'workplace', 'work'
            ],
            'cyber_harassment': [
                'online', 'social media', 'whatsapp', 'facebook', 'instagram', 
                'messages', 'photos', 'videos', 'internet'
            ],
            'neighbor_harassment': [
                'neighbor', 'neighbour', 'building', 'society', 'apartment', 
                'noise', 'disturbance', 'property'
            ],
            'domestic_harassment': [
                'husband', 'wife', 'family', 'in-laws', 'domestic', 'home', 'house'
            ],
            'public_harassment': [
                'street', 'public', 'transport', 'bus', 'train', 'market', 'shop'
            ]
        }
        
        # Domain mapping for harassment types
        self.harassment_domain_mapping = {
            'sexual_harassment': [
                ('criminal_law', 0.8, 'Sexual harassment is a criminal offense'),
                ('employment_law', 0.6, 'If workplace-related harassment')
            ],
            'workplace_harassment': [
                ('employment_law', 0.9, 'Workplace harassment falls under employment law'),
                ('criminal_law', 0.7, 'May involve criminal charges')
            ],
            'cyber_harassment': [
                ('cyber_crime', 0.9, 'Online harassment is cyber crime'),
                ('criminal_law', 0.6, 'May involve criminal charges')
            ],
            'neighbor_harassment': [
                ('criminal_law', 0.7, 'Harassment can be criminal offense'),
                ('tenant_rights', 0.5, 'If related to housing/property disputes')
            ],
            'domestic_harassment': [
                ('family_law', 0.9, 'Domestic issues fall under family law'),
                ('criminal_law', 0.8, 'Domestic violence is criminal offense')
            ],
            'public_harassment': [
                ('criminal_law', 0.8, 'Public harassment is criminal offense'),
                ('personal_injury', 0.4, 'If physical harm involved')
            ]
        }
        
        # Urgency indicators
        self.urgency_keywords = {
            'emergency': ['immediate danger', 'threatening', 'violence', 'assault', 'attack', 'emergency'],
            'high': ['harassment', 'stalking', 'abuse', 'threatening', 'intimidation'],
            'medium': ['bothering', 'disturbing', 'annoying', 'pestering'],
            'low': ['complaint', 'issue', 'problem', 'concern']
        }
        
        # Constitutional articles relevant to harassment
        self.constitutional_articles = {
            'harassment': [
                'Article 21 - Right to Life and Personal Liberty',
                'Article 19 - Right to Freedom of Speech and Expression',
                'Article 14 - Right to Equality',
                'Article 15 - Prohibition of Discrimination'
            ]
        }
    
    def analyze_unknown_query(self, query: str, ml_confidence: float, ml_alternatives: List[Tuple[str, float]]) -> UnknownQueryAnalysis:
        """Analyze unknown domain query and provide enhanced response"""
        
        query_lower = query.lower()
        
        # Step 1: Detect harassment type
        harassment_type = self._detect_harassment_type(query_lower)
        
        # Step 2: Determine urgency level
        urgency_level = self._assess_urgency(query_lower)
        
        # Step 3: Generate domain suggestions
        suggested_domains = self._suggest_domains(harassment_type, ml_alternatives)
        
        # Step 4: Generate recommended actions
        recommended_actions = self._generate_actions(harassment_type, urgency_level)
        
        # Step 5: Identify constitutional relevance
        constitutional_relevance = self._get_constitutional_relevance(harassment_type)
        
        # Step 6: Generate specialized advice
        specialized_advice = self._generate_specialized_advice(harassment_type, urgency_level)
        
        return UnknownQueryAnalysis(
            suggested_domains=suggested_domains,
            harassment_type=harassment_type,
            urgency_level=urgency_level,
            recommended_actions=recommended_actions,
            constitutional_relevance=constitutional_relevance,
            specialized_advice=specialized_advice
        )
    
    def _detect_harassment_type(self, query: str) -> Optional[str]:
        """Detect type of harassment from query"""
        
        for harassment_type, keywords in self.harassment_patterns.items():
            if any(keyword in query for keyword in keywords):
                return harassment_type
        
        # Check for general harassment indicators
        harassment_indicators = ['harass', 'bother', 'trouble', 'disturb', 'annoy', 'pester', 'threaten']
        if any(indicator in query for indicator in harassment_indicators):
            return 'general_harassment'
        
        return None
    
    def _assess_urgency(self, query: str) -> str:
        """Assess urgency level of the query"""
        
        for level, keywords in self.urgency_keywords.items():
            if any(keyword in query for keyword in keywords):
                return level
        
        return 'low'
    
    def _suggest_domains(self, harassment_type: Optional[str], ml_alternatives: List[Tuple[str, float]]) -> List[Tuple[str, float, str]]:
        """Suggest relevant domains based on harassment type and ML alternatives"""
        
        suggestions = []
        
        # Add harassment-specific suggestions
        if harassment_type and harassment_type in self.harassment_domain_mapping:
            for domain, confidence, reason in self.harassment_domain_mapping[harassment_type]:
                suggestions.append((domain, confidence, reason))
        
        # Add ML alternatives with explanations
        for domain, confidence in ml_alternatives[:2]:
            if domain != 'unknown':
                reason = f"ML model suggests {domain} with {confidence:.1%} confidence"
                suggestions.append((domain, confidence, reason))
        
        # Remove duplicates and sort by confidence
        seen_domains = set()
        unique_suggestions = []
        for domain, conf, reason in suggestions:
            if domain not in seen_domains:
                unique_suggestions.append((domain, conf, reason))
                seen_domains.add(domain)
        
        return sorted(unique_suggestions, key=lambda x: x[1], reverse=True)[:3]
    
    def _generate_actions(self, harassment_type: Optional[str], urgency_level: str) -> List[str]:
        """Generate recommended actions based on harassment type and urgency"""
        
        actions = []
        
        # Urgency-based actions
        if urgency_level == 'emergency':
            actions.extend([
                "Call emergency services (100/112) if in immediate danger",
                "Contact local police station immediately",
                "Seek immediate safe shelter"
            ])
        elif urgency_level == 'high':
            actions.extend([
                "File police complaint (FIR) at nearest station",
                "Document all incidents with dates and evidence",
                "Consider seeking protection order"
            ])
        
        # Harassment-specific actions
        if harassment_type == 'sexual_harassment':
            actions.extend([
                "File complaint under Sexual Harassment Act",
                "Report to Internal Complaints Committee (if workplace)",
                "Consider filing under IPC Section 354 (assault/criminal force)"
            ])
        elif harassment_type == 'cyber_harassment':
            actions.extend([
                "Report to Cyber Crime Cell",
                "File complaint on cybercrime.gov.in portal",
                "Preserve digital evidence (screenshots, messages)"
            ])
        elif harassment_type == 'neighbor_harassment':
            actions.extend([
                "Approach building society/RWA first",
                "File police complaint if harassment continues",
                "Consider mediation through local authorities"
            ])
        
        # General actions
        actions.extend([
            "Maintain detailed record of all incidents",
            "Gather witness statements if available",
            "Consult with qualified legal professional"
        ])
        
        return actions[:5]  # Limit to top 5 actions
    
    def _get_constitutional_relevance(self, harassment_type: Optional[str]) -> List[str]:
        """Get relevant constitutional articles"""
        
        if harassment_type:
            return self.constitutional_articles.get('harassment', [])
        return []
    
    def _generate_specialized_advice(self, harassment_type: Optional[str], urgency_level: str) -> str:
        """Generate specialized legal advice"""
        
        if urgency_level == 'emergency':
            return "This appears to be an emergency situation. Contact emergency services immediately (100/112) and seek immediate safety. Legal action can be pursued once you are safe."
        
        if harassment_type == 'sexual_harassment':
            return "Sexual harassment is a serious criminal offense under IPC Section 354A. You have the right to file a police complaint and seek legal remedy. If workplace-related, also approach the Internal Complaints Committee."
        
        elif harassment_type == 'cyber_harassment':
            return "Cyber harassment falls under IT Act 2000 and IPC provisions. File a complaint with the Cyber Crime Cell and preserve all digital evidence. Online harassment is taken seriously by law enforcement."
        
        elif harassment_type == 'neighbor_harassment':
            return "Neighbor harassment can be addressed through police complaint under IPC Section 506 (criminal intimidation) or Section 294 (obscene acts). Try mediation first, but don't hesitate to involve police if harassment continues."
        
        elif harassment_type == 'workplace_harassment':
            return "Workplace harassment violates employment laws and may constitute criminal offense. Report to HR/management first, then consider police complaint if not resolved. You have protection against retaliation."
        
        else:
            return "Harassment in any form violates your fundamental rights. Document all incidents, gather evidence, and consider filing a police complaint. You have legal remedies available under various laws."


def create_enhanced_unknown_handler() -> EnhancedUnknownHandler:
    """Factory function to create enhanced unknown handler"""
    return EnhancedUnknownHandler()


# Test the enhanced unknown handler
if __name__ == "__main__":
    handler = create_enhanced_unknown_handler()
    
    test_queries = [
        "my neighbor girl is being harassed",
        "boss is sexually harassing me at work",
        "someone is stalking me online",
        "husband threatening me with violence",
        "colleague bothering me constantly"
    ]
    
    print("🧪 TESTING ENHANCED UNKNOWN HANDLER")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: \"{query}\"")
        
        # Simulate ML alternatives (low confidence)
        ml_alternatives = [('criminal_law', 0.15), ('family_law', 0.12)]
        
        analysis = handler.analyze_unknown_query(query, 0.1, ml_alternatives)
        
        print(f"Harassment Type: {analysis.harassment_type}")
        print(f"Urgency: {analysis.urgency_level}")
        print(f"Suggested Domains:")
        for domain, conf, reason in analysis.suggested_domains:
            print(f"  • {domain} ({conf:.1%}): {reason}")
        print(f"Top Actions:")
        for action in analysis.recommended_actions[:3]:
            print(f"  • {action}")
        print(f"Specialized Advice: {analysis.specialized_advice[:100]}...")
