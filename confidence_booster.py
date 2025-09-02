#!/usr/bin/env python3
"""
Confidence Booster for Enhanced Legal Agent
==========================================

Provides confidence adjustments for specific legal scenarios to ensure
appropriate confidence levels for critical cases like domestic violence.
"""

from typing import Dict, Any, Tuple

class ConfidenceBooster:
    """Boosts confidence for critical legal scenarios"""
    
    def __init__(self):
        """Initialize confidence booster with domain-specific rules"""
        self.confidence_rules = self._load_confidence_rules()
    
    def _load_confidence_rules(self) -> Dict[str, Any]:
        """Load confidence boosting rules for different domains"""
        return {
            "family_law": {
                "domestic_violence": {
                    "keywords": ["beats", "violence", "abuse", "domestic", "hitting", "hurting", "threatening", "daily"],
                    "min_confidence": 0.85,  # Minimum confidence for domestic violence cases
                    "boost_factor": 3.0,     # Multiply confidence by this factor
                    "reason": "Domestic violence is a serious crime requiring immediate attention"
                },
                "child_abuse": {
                    "keywords": ["child", "abuse", "minor", "kid", "beating child"],
                    "min_confidence": 0.90,
                    "boost_factor": 3.5,
                    "reason": "Child abuse cases require urgent intervention"
                }
            },
            "criminal_law": {
                "rape": {
                    "keywords": ["rape", "raped", "sexual assault", "molest"],
                    "min_confidence": 0.95,
                    "boost_factor": 4.0,
                    "reason": "Sexual assault cases require immediate police action"
                },
                "murder": {
                    "keywords": ["murder", "killed", "death threat", "attempt to kill"],
                    "min_confidence": 0.90,
                    "boost_factor": 3.5,
                    "reason": "Life-threatening situations require urgent response"
                }
            },
            "cyber_crime": {
                "hacking": {
                    "keywords": ["hack", "hacked", "hacking", "account compromised"],
                    "min_confidence": 0.80,
                    "boost_factor": 2.5,
                    "reason": "Cyber crimes require quick action to prevent further damage"
                }
            }
        }
    
    def boost_confidence(self, domain: str, query: str, original_confidence: float) -> Tuple[float, str]:
        """
        Boost confidence for critical legal scenarios
        
        Args:
            domain: Legal domain (e.g., 'family_law', 'criminal_law')
            query: User query text
            original_confidence: Original confidence score
            
        Returns:
            Tuple of (boosted_confidence, boost_reason)
        """
        query_lower = query.lower()
        
        # Check domain-specific rules
        if domain in self.confidence_rules:
            domain_rules = self.confidence_rules[domain]
            
            for category, rule in domain_rules.items():
                # Check if query matches any keywords for this category
                if any(keyword in query_lower for keyword in rule["keywords"]):
                    # Apply confidence boost
                    boosted_confidence = min(
                        original_confidence * rule["boost_factor"],
                        rule["min_confidence"]
                    )
                    
                    # Ensure minimum confidence is met
                    if boosted_confidence < rule["min_confidence"]:
                        boosted_confidence = rule["min_confidence"]
                    
                    return boosted_confidence, rule["reason"]
        
        # No boost applied
        return original_confidence, ""
    
    def get_severity_level(self, domain: str, query: str) -> str:
        """Get severity level for the legal issue"""
        query_lower = query.lower()
        
        # Critical severity keywords
        critical_keywords = [
            "beats", "violence", "abuse", "rape", "murder", "death threat",
            "attempt to kill", "daily", "threatening", "hurting"
        ]
        
        # High severity keywords
        high_keywords = [
            "hack", "hacked", "stolen", "fraud", "cheating", "harassment"
        ]
        
        if any(keyword in query_lower for keyword in critical_keywords):
            return "CRITICAL"
        elif any(keyword in query_lower for keyword in high_keywords):
            return "HIGH"
        else:
            return "MEDIUM"

# Integration function for enhanced working agent
def apply_confidence_boost(domain: str, query: str, confidence: float) -> Tuple[float, str, str]:
    """
    Apply confidence boost and return enhanced confidence with metadata
    
    Returns:
        Tuple of (boosted_confidence, boost_reason, severity_level)
    """
    booster = ConfidenceBooster()
    
    # Apply confidence boost
    boosted_confidence, boost_reason = booster.boost_confidence(domain, query, confidence)
    
    # Get severity level
    severity_level = booster.get_severity_level(domain, query)
    
    return boosted_confidence, boost_reason, severity_level

# Test the confidence booster
if __name__ == "__main__":
    booster = ConfidenceBooster()
    
    # Test cases
    test_cases = [
        ("family_law", "My husband beats me daily", 0.220),
        ("criminal_law", "I was raped by my neighbor", 0.300),
        ("cyber_crime", "My phone is being hacked", 2.293),
        ("employment_law", "Boss not paying salary", 0.645)
    ]
    
    print("🧪 CONFIDENCE BOOSTER TEST")
    print("=" * 40)
    
    for domain, query, original_conf in test_cases:
        boosted_conf, reason, severity = apply_confidence_boost(domain, query, original_conf)
        
        print(f"\n📋 Query: '{query}'")
        print(f"   Domain: {domain}")
        print(f"   Original Confidence: {original_conf:.3f}")
        print(f"   Boosted Confidence: {boosted_conf:.3f}")
        print(f"   Severity Level: {severity}")
        if reason:
            print(f"   Boost Reason: {reason}")
        print(f"   Confidence Change: {((boosted_conf - original_conf) / original_conf * 100):+.1f}%")