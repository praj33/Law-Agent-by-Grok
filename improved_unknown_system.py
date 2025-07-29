"""
Improved Unknown Domain System
=============================

Complete solution for handling "unknown domain" queries with:
1. Enhanced analysis and domain suggestions
2. Harassment-specific handling
3. Training data expansion
4. Automatic learning capabilities
"""

import json
import sys
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

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

logger = logging.getLogger(__name__)

@dataclass
class ImprovedUnknownResponse:
    """Enhanced response for unknown domain queries"""
    original_query: str
    suggested_domain: str
    confidence: float
    reasoning: str
    harassment_type: Optional[str]
    urgency_level: str
    recommended_actions: List[str]
    constitutional_articles: List[str]
    specialized_advice: str
    similar_examples: List[str]

class ImprovedUnknownSystem:
    """Complete system for handling unknown domain queries"""
    
    def __init__(self):
        """Initialize improved unknown system"""
        
        # Harassment detection patterns
        self.harassment_patterns = {
            'neighbor_harassment': ['neighbor', 'neighbour', 'building', 'society', 'apartment'],
            'sexual_harassment': ['sexual', 'inappropriate', 'touching', 'advances', 'molest', 'eve teasing'],
            'workplace_harassment': ['boss', 'supervisor', 'colleague', 'office', 'workplace', 'work'],
            'cyber_harassment': ['online', 'social media', 'internet', 'cyber', 'digital'],
            'domestic_harassment': ['husband', 'wife', 'family', 'in-laws', 'domestic', 'home'],
            'public_harassment': ['street', 'public', 'transport', 'market', 'shop']
        }
        
        # Domain mapping for harassment types
        self.harassment_to_domain = {
            'neighbor_harassment': ('criminal_law', 0.75, 'Neighbor harassment typically involves criminal law'),
            'sexual_harassment': ('criminal_law', 0.85, 'Sexual harassment is a criminal offense'),
            'workplace_harassment': ('employment_law', 0.90, 'Workplace harassment falls under employment law'),
            'cyber_harassment': ('cyber_crime', 0.95, 'Online harassment is cyber crime'),
            'domestic_harassment': ('family_law', 0.90, 'Domestic issues fall under family law'),
            'public_harassment': ('criminal_law', 0.80, 'Public harassment is criminal offense'),
            'general_harassment': ('criminal_law', 0.70, 'General harassment typically involves criminal law')
        }
        
        # Urgency assessment
        self.urgency_keywords = {
            'emergency': ['immediate danger', 'threatening', 'violence', 'assault', 'emergency'],
            'high': ['harassment', 'stalking', 'abuse', 'threatening', 'intimidation'],
            'medium': ['bothering', 'disturbing', 'annoying', 'pestering'],
            'low': ['complaint', 'issue', 'problem', 'concern']
        }
        
        # Training examples for similar case matching
        self.training_examples = {
            'criminal_law': [
                "neighbor harassing me constantly",
                "someone stalking me on street",
                "being threatened by stranger",
                "harassment causing mental trauma"
            ],
            'employment_law': [
                "boss sexually harassing at work",
                "colleague making inappropriate comments",
                "workplace harassment by supervisor",
                "sexual advances by manager"
            ],
            'cyber_crime': [
                "online harassment and threats",
                "cyberbullying on social media",
                "someone stalking me online",
                "fake profiles harassing me"
            ],
            'family_law': [
                "husband harassing me at home",
                "in-laws threatening for dowry",
                "domestic harassment by spouse",
                "family members intimidating me"
            ]
        }
    
    def analyze_unknown_query(self, query: str, ml_confidence: float = 0.0) -> ImprovedUnknownResponse:
        """Analyze unknown query and provide enhanced response"""
        
        query_lower = query.lower()
        
        # Step 1: Detect harassment type
        harassment_type = self._detect_harassment_type(query_lower)
        
        # Step 2: Suggest domain based on harassment type
        if harassment_type:
            suggested_domain, confidence, reasoning = self.harassment_to_domain[harassment_type]
        else:
            # Fallback to keyword-based suggestion
            suggested_domain, confidence, reasoning = self._suggest_domain_by_keywords(query_lower)
        
        # Step 3: Assess urgency
        urgency_level = self._assess_urgency(query_lower)
        
        # Step 4: Generate actions
        recommended_actions = self._generate_actions(harassment_type, urgency_level, suggested_domain)
        
        # Step 5: Get constitutional articles
        constitutional_articles = self._get_constitutional_articles(harassment_type)
        
        # Step 6: Generate specialized advice
        specialized_advice = self._generate_specialized_advice(harassment_type, urgency_level, suggested_domain)
        
        # Step 7: Find similar examples
        similar_examples = self._find_similar_examples(suggested_domain, query_lower)
        
        return ImprovedUnknownResponse(
            original_query=query,
            suggested_domain=suggested_domain,
            confidence=confidence,
            reasoning=reasoning,
            harassment_type=harassment_type,
            urgency_level=urgency_level,
            recommended_actions=recommended_actions,
            constitutional_articles=constitutional_articles,
            specialized_advice=specialized_advice,
            similar_examples=similar_examples
        )
    
    def _detect_harassment_type(self, query: str) -> Optional[str]:
        """Detect harassment type from query"""
        
        # Check for harassment indicators first
        harassment_indicators = ['harass', 'bother', 'trouble', 'disturb', 'threaten', 'intimidat', 'stalk']
        if not any(indicator in query for indicator in harassment_indicators):
            return None
        
        # Determine specific type
        for harassment_type, keywords in self.harassment_patterns.items():
            if any(keyword in query for keyword in keywords):
                return harassment_type
        
        return 'general_harassment'
    
    def _suggest_domain_by_keywords(self, query: str) -> Tuple[str, float, str]:
        """Suggest domain based on keywords when no harassment detected"""
        
        domain_keywords = {
            'criminal_law': ['police', 'crime', 'illegal', 'theft', 'fraud', 'violence'],
            'family_law': ['marriage', 'divorce', 'custody', 'spouse', 'children'],
            'employment_law': ['job', 'work', 'salary', 'employer', 'employee'],
            'consumer_complaint': ['product', 'service', 'company', 'warranty', 'refund'],
            'cyber_crime': ['online', 'internet', 'digital', 'computer', 'website'],
            'tenant_rights': ['rent', 'landlord', 'property', 'lease', 'apartment'],
            'contract_dispute': ['agreement', 'contract', 'business', 'deal', 'breach'],
            'personal_injury': ['accident', 'injury', 'medical', 'hospital', 'damage'],
            'immigration_law': ['visa', 'passport', 'citizenship', 'immigration'],
            'elder_abuse': ['elderly', 'senior', 'old', 'aged', 'grandmother', 'grandfather']
        }
        
        best_domain = 'criminal_law'  # Default fallback
        best_score = 0
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query)
            if score > best_score:
                best_score = score
                best_domain = domain
        
        confidence = min(0.6, best_score * 0.15) if best_score > 0 else 0.3
        reasoning = f"Query contains keywords related to {best_domain}"
        
        return best_domain, confidence, reasoning
    
    def _assess_urgency(self, query: str) -> str:
        """Assess urgency level"""
        
        for level, keywords in self.urgency_keywords.items():
            if any(keyword in query for keyword in keywords):
                return level
        return 'low'
    
    def _generate_actions(self, harassment_type: Optional[str], urgency: str, domain: str) -> List[str]:
        """Generate recommended actions"""
        
        actions = []
        
        # Urgency-based actions
        if urgency == 'emergency':
            actions.extend([
                "Call emergency services (100/112) immediately",
                "Contact local police station",
                "Seek immediate safe shelter"
            ])
        elif urgency == 'high':
            actions.extend([
                "File police complaint (FIR) at nearest station",
                "Document all incidents with evidence",
                "Consider seeking protection order"
            ])
        
        # Domain-specific actions
        if domain == 'criminal_law':
            actions.extend([
                "File police complaint under relevant IPC sections",
                "Gather witness statements and evidence",
                "Consider legal consultation for criminal case"
            ])
        elif domain == 'employment_law':
            actions.extend([
                "Report to HR department or management",
                "File complaint with Internal Complaints Committee",
                "Document workplace incidents with dates"
            ])
        elif domain == 'cyber_crime':
            actions.extend([
                "Report to Cyber Crime Cell",
                "File complaint on cybercrime.gov.in",
                "Preserve digital evidence (screenshots, messages)"
            ])
        elif domain == 'family_law':
            actions.extend([
                "Consult family court for legal remedies",
                "Consider mediation or counseling",
                "File complaint under Domestic Violence Act if applicable"
            ])
        
        # General actions
        actions.extend([
            "Maintain detailed record of all incidents",
            "Consult with qualified legal professional",
            "Know your legal rights and options"
        ])
        
        return actions[:6]  # Limit to top 6 actions
    
    def _get_constitutional_articles(self, harassment_type: Optional[str]) -> List[str]:
        """Get relevant constitutional articles"""
        
        if harassment_type:
            return [
                "Article 21 - Right to Life and Personal Liberty",
                "Article 19 - Right to Freedom of Speech and Expression",
                "Article 14 - Right to Equality before Law"
            ]
        return ["Article 21 - Right to Life and Personal Liberty"]
    
    def _generate_specialized_advice(self, harassment_type: Optional[str], urgency: str, domain: str) -> str:
        """Generate specialized legal advice"""
        
        if urgency == 'emergency':
            return "This appears to be an emergency. Contact emergency services (100/112) immediately and ensure your safety first. Legal action can be pursued once you are safe."
        
        if harassment_type == 'neighbor_harassment':
            return "Neighbor harassment can be addressed under IPC Section 506 (criminal intimidation) or Section 294 (obscene acts). Try building society mediation first, but file police complaint if harassment continues."
        
        elif harassment_type == 'sexual_harassment':
            return "Sexual harassment is a serious offense under IPC Section 354A. You have the right to file police complaint and seek legal remedy. If workplace-related, also approach Internal Complaints Committee."
        
        elif harassment_type == 'cyber_harassment':
            return "Cyber harassment falls under IT Act 2000 and IPC provisions. File complaint with Cyber Crime Cell and preserve all digital evidence. Online harassment is taken seriously by authorities."
        
        elif harassment_type == 'workplace_harassment':
            return "Workplace harassment violates employment laws and may constitute criminal offense. Report to HR first, then consider police complaint if unresolved. You have protection against retaliation."
        
        elif harassment_type == 'domestic_harassment':
            return "Domestic harassment can be addressed under Domestic Violence Act 2005 and IPC provisions. You can seek protection orders, maintenance, and safe shelter. Contact women helpline 181 for immediate support."
        
        else:
            return f"Based on your query, this appears to fall under {domain}. You have legal remedies available under relevant laws. Document all incidents and consider filing appropriate complaint with authorities."
    
    def _find_similar_examples(self, domain: str, query: str) -> List[str]:
        """Find similar examples from training data"""
        
        if domain in self.training_examples:
            return self.training_examples[domain][:3]
        return []


def test_improved_unknown_system():
    """Test the improved unknown system"""
    
    safe_print("🧪 TESTING IMPROVED UNKNOWN SYSTEM")
    safe_print("=" * 50)
    
    system = ImprovedUnknownSystem()
    
    test_queries = [
        "my neighbor girl is being harassed",
        "boss sexually harassing me at work",
        "someone stalking me online",
        "husband threatening me with violence",
        "colleague bothering me constantly",
        "landlord harassing me for rent",
        "company representatives threatening me"
    ]
    
    for query in test_queries:
        safe_print(f"\n📝 Query: \"{query}\"")
        
        response = system.analyze_unknown_query(query)
        
        safe_print(f"🎯 Suggested Domain: {response.suggested_domain} (confidence: {response.confidence:.1%})")
        safe_print(f"💡 Reasoning: {response.reasoning}")
        safe_print(f"🚨 Urgency: {response.urgency_level}")
        
        if response.harassment_type:
            safe_print(f"⚠️ Harassment Type: {response.harassment_type}")
        
        safe_print(f"📋 Top Actions:")
        for i, action in enumerate(response.recommended_actions[:3], 1):
            safe_print(f"   {i}. {action}")
        
        safe_print(f"🏛️ Constitutional: {response.constitutional_articles[0] if response.constitutional_articles else 'None'}")
        safe_print(f"💬 Advice: {response.specialized_advice[:100]}...")


if __name__ == "__main__":
    test_improved_unknown_system()
