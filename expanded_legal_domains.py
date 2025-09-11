#!/usr/bin/env python3
"""
Expanded Legal Domains - 25+ Legal Areas
=======================================

Comprehensive legal domain classification with 25+ major legal areas
and improved domain detection accuracy.
"""

from typing import Dict, List, Tuple, Optional, Any
import re


class ExpandedLegalDomains:
    """Expanded legal domains with 25+ major legal areas"""
    
    def __init__(self):
        self.domain_keywords = self._init_expanded_domains()
        self.domain_patterns = self._init_domain_patterns()
    
    def _init_expanded_domains(self) -> Dict[str, List[str]]:
        """Initialize 25+ legal domains with comprehensive keywords"""
        return {
            # 1. Criminal Law
            "criminal_law": [
                "murder", "kill", "death", "homicide", "assassination", "manslaughter",
                "crime", "criminal", "felony", "offense", "violation", "illegal",
                "arrest", "police", "jail", "prison", "custody", "detention"
            ],
            
            # 2. Sexual Offences
            "sexual_offences": [
                "rape", "sexual", "molestation", "harassment", "assault", "abuse",
                "modesty", "stalking", "voyeurism", "indecent", "inappropriate",
                "eve teasing", "groping", "touching", "pornography"
            ],
            
            # 3. Property Crimes
            "property_crimes": [
                "theft", "steal", "stolen", "burglary", "robbery", "dacoity",
                "cheating", "fraud", "scam", "embezzlement", "misappropriation",
                "extortion", "blackmail", "forgery", "counterfeit", "fake"
            ],
            
            # 4. Violent Crimes
            "violent_crimes": [
                "violence", "assault", "attack", "beat", "hurt", "injury",
                "kidnapping", "abduction", "hostage", "ransom", "captive",
                "acid attack", "lynching", "mob violence", "rioting"
            ],
            
            # 5. Cyber Crime
            "cyber_crime": [
                "cyber", "hack", "hacking", "online", "internet", "digital",
                "computer", "phishing", "malware", "virus", "data breach",
                "identity theft", "cyberbullying", "online fraud", "email fraud"
            ],
            
            # 6. Employment Law
            "employment_law": [
                "job", "work", "employment", "employee", "employer", "boss",
                "salary", "wage", "fired", "termination", "dismissal",
                "workplace", "office", "discrimination", "harassment at work"
            ],
            
            # 7. Family Law
            "family_law": [
                "family", "marriage", "divorce", "separation", "husband", "wife",
                "child", "custody", "adoption", "alimony", "maintenance",
                "domestic violence", "dowry", "bigamy", "inheritance"
            ],
            
            # 8. Financial Crimes
            "financial_crimes": [
                "financial", "money", "bank", "banking", "loan", "credit",
                "insurance", "investment", "ponzi", "pyramid", "bribery",
                "corruption", "tax evasion", "money laundering"
            ],
            
            # 9. Drug Crimes
            "drug_crimes": [
                "drug", "drugs", "narcotic", "cocaine", "heroin", "cannabis",
                "marijuana", "opium", "substance", "possession", "trafficking",
                "smuggling", "peddling", "addiction", "rehab"
            ],
            
            # 10. Public Order
            "public_order": [
                "public", "riot", "protest", "demonstration", "strike", "bandh",
                "unlawful assembly", "sedition", "terrorism", "bomb", "explosive",
                "hate speech", "communal", "defamation", "contempt"
            ],
            
            # 11. Consumer Protection
            "consumer_protection": [
                "consumer", "product", "service", "defective", "warranty",
                "guarantee", "refund", "replacement", "shop", "store",
                "merchant", "seller", "buyer", "purchase", "sale"
            ],
            
            # 12. Personal Injury
            "personal_injury": [
                "accident", "injury", "injured", "hurt", "medical", "hospital",
                "doctor", "treatment", "compensation", "insurance", "claim",
                "car", "vehicle", "motor", "bike", "truck", "bus",
                "collision", "crash", "wreck", "hit", "struck"
            ],
            
            # 13. Medical Law
            "medical_law": [
                "medical", "doctor", "hospital", "treatment", "surgery",
                "negligence", "malpractice", "patient", "medicine", "drug",
                "prescription", "health", "clinic", "nurse"
            ],
            
            # 13. Real Estate Law
            "real_estate_law": [
                "property", "real estate", "land", "house", "building",
                "apartment", "flat", "plot", "construction", "builder",
                "developer", "registry", "deed", "title", "possession"
            ],
            
            # 14. Contract Law
            "contract_law": [
                "contract", "agreement", "deal", "terms", "conditions",
                "breach", "violation", "performance", "obligation",
                "party", "clause", "provision", "binding"
            ],
            
            # 15. Intellectual Property
            "intellectual_property": [
                "patent", "trademark", "copyright", "intellectual property",
                "brand", "logo", "design", "invention", "innovation",
                "piracy", "infringement", "plagiarism", "royalty"
            ],
            
            # 16. Environmental Law
            "environmental_law": [
                "environment", "pollution", "waste", "water", "air",
                "noise", "forest", "wildlife", "green", "ecology",
                "climate", "emission", "toxic", "hazardous"
            ],
            
            # 17. Tax Law
            "tax_law": [
                "tax", "income tax", "gst", "vat", "customs", "excise",
                "duty", "return", "assessment", "penalty", "fine",
                "evasion", "avoidance", "refund", "tds"
            ],
            
            # 18. Immigration Law
            "immigration_law": [
                "visa", "passport", "immigration", "emigration", "citizen",
                "nationality", "resident", "foreigner", "alien",
                "deportation", "asylum", "refugee", "border"
            ],
            
            # 19. Corporate Law
            "corporate_law": [
                "company", "corporation", "business", "corporate", "firm",
                "partnership", "llp", "director", "shareholder", "board",
                "compliance", "governance", "merger", "acquisition"
            ],
            
            # 20. Banking Law
            "banking_law": [
                "bank", "banking", "account", "deposit", "withdrawal",
                "loan", "credit", "debit", "cheque", "draft",
                "interest", "emi", "mortgage", "collateral"
            ],
            
            # 21. Insurance Law
            "insurance_law": [
                "insurance", "policy", "premium", "claim", "coverage",
                "benefit", "compensation", "life insurance", "health insurance",
                "vehicle insurance", "fire insurance", "liability"
            ],
            
            # 22. Education Law
            "education_law": [
                "education", "school", "college", "university", "student",
                "teacher", "admission", "fee", "scholarship", "degree",
                "certificate", "exam", "result", "academic"
            ],
            
            # 23. Transport Law
            "transport_law": [
                "transport", "vehicle", "car", "bike", "truck", "bus",
                "driving", "license", "accident", "traffic", "road",
                "highway", "parking", "challan", "fine"
            ],
            
            # 24. Sports Law
            "sports_law": [
                "sports", "game", "player", "athlete", "team", "match",
                "tournament", "competition", "doping", "betting",
                "gambling", "fixing", "corruption in sports"
            ],
            
            # 25. Media Law
            "media_law": [
                "media", "press", "newspaper", "television", "radio",
                "journalist", "reporter", "news", "broadcast", "publication",
                "freedom of press", "censorship", "defamation in media"
            ],
            
            # 26. Human Rights
            "human_rights": [
                "human rights", "fundamental rights", "civil rights",
                "liberty", "freedom", "equality", "justice", "discrimination",
                "minority", "women rights", "child rights"
            ],
            
            # 27. Administrative Law
            "administrative_law": [
                "government", "administration", "bureaucracy", "public service",
                "civil service", "ias", "ips", "government employee",
                "public policy", "regulation", "license", "permit"
            ],
            
            # 28. Constitutional Law
            "constitutional_law": [
                "constitution", "constitutional", "fundamental rights",
                "directive principles", "amendment", "article", "supreme court",
                "high court", "judicial review", "writ petition"
            ],
            
            # 29. Election Law
            "election_law": [
                "election", "voting", "vote", "candidate", "political party",
                "campaign", "ballot", "constituency", "mla", "mp",
                "election commission", "electoral", "democracy"
            ],
            
            # 30. International Law
            "international_law": [
                "international", "treaty", "agreement", "diplomatic",
                "embassy", "consulate", "extradition", "arbitration",
                "world court", "united nations", "bilateral"
            ]
        }
    
    def _init_domain_patterns(self) -> Dict[str, List[str]]:
        """Initialize domain-specific patterns for better detection"""
        return {
            "criminal_law": [
                r"\b(murder|kill|death|crime|arrest|police)\b",
                r"\b(illegal|offense|violation|criminal)\b"
            ],
            "sexual_offences": [
                r"\b(rape|sexual|harassment|molest|stalk)\b",
                r"\b(inappropriate|indecent|modesty)\b"
            ],
            "property_crimes": [
                r"\b(theft|steal|stolen|rob|cheat|fraud)\b",
                r"\b(embezzle|forge|counterfeit|fake)\b"
            ],
            "cyber_crime": [
                r"\b(hack|cyber|online|internet|digital)\b",
                r"\b(phishing|malware|data breach)\b"
            ],
            "employment_law": [
                r"\b(job|work|employ|boss|salary|fired)\b",
                r"\b(workplace|office|discrimination)\b"
            ],
            "family_law": [
                r"\b(family|marriage|divorce|husband|wife)\b",
                r"\b(child|custody|domestic|dowry)\b"
            ],
            "personal_injury": [
                r"\b(accident|injury|injured|hurt)\b",
                r"\b(car|vehicle|motor|crash)\b"
            ],
            "medical_law": [
                r"\b(doctor|hospital|medical|treatment)\b",
                r"\b(negligence|malpractice|patient)\b"
            ],
            "real_estate_law": [
                r"\b(property|land|house|building|flat)\b",
                r"\b(builder|developer|construction)\b"
            ],
            "consumer_protection": [
                r"\b(consumer|product|service|defective)\b",
                r"\b(warranty|refund|shop|store)\b"
            ],
            "financial_crimes": [
                r"\b(financial|money|bank|loan|bribery)\b",
                r"\b(corruption|tax evasion|laundering)\b"
            ]
        }
    
    def classify_domain(self, query: str) -> Tuple[str, float]:
        """Classify domain with improved accuracy"""
        
        query_lower = query.lower()
        domain_scores = {}
        
        # Score based on keywords
        for domain, keywords in self.domain_keywords.items():
            score = 0
            matches = 0
            
            for keyword in keywords:
                if keyword in query_lower:
                    # Multi-word keywords get higher score
                    word_count = len(keyword.split())
                    score += word_count * 2
                    matches += 1
            
            if matches > 0:
                # Normalize score and add match bonus
                domain_scores[domain] = (score / len(keywords)) + (matches * 0.1)
        
        # Score based on patterns
        for domain, patterns in self.domain_patterns.items():
            pattern_score = 0
            for pattern in patterns:
                if re.search(pattern, query_lower, re.IGNORECASE):
                    pattern_score += 0.3
            
            if domain in domain_scores:
                domain_scores[domain] += pattern_score
            elif pattern_score > 0:
                domain_scores[domain] = pattern_score
        
        # Special handling for medical malpractice cases
        # If both personal_injury and medical_law are scored, and the query contains
        # malpractice/negligence AND injury/accident/harm, prioritize personal_injury
        if ("personal_injury" in domain_scores and 
            "medical_law" in domain_scores and
            any(word in query_lower for word in ["malpractice", "negligence"]) and
            any(word in query_lower for word in ["injury", "injured", "hurt", "accident", "accidental", "harm"])):
            # Boost personal_injury score to ensure it wins
            domain_scores["personal_injury"] = max(domain_scores["personal_injury"], domain_scores["medical_law"] + 0.1)
        
        # Find best domain
        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            confidence = min(domain_scores[best_domain], 0.95)
            
            # Boost confidence for strong matches
            if confidence > 0.5:
                confidence = min(confidence * 1.2, 0.95)
            
            return best_domain, confidence
        else:
            return "general_law", 0.3
    
    def get_all_domains(self) -> List[str]:
        """Get all available domains"""
        return list(self.domain_keywords.keys())
    
    def get_domain_info(self, domain: str) -> Dict[str, Any]:
        """Get domain information"""
        if domain not in self.domain_keywords:
            return {"error": f"Domain '{domain}' not found"}
        
        return {
            "domain": domain,
            "keywords": self.domain_keywords[domain],
            "description": f"Legal matters related to {domain.replace('_', ' ').title()}",
            "patterns": self.domain_patterns.get(domain, [])
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get domain classifier statistics"""
        total_keywords = sum(len(keywords) for keywords in self.domain_keywords.values())
        
        return {
            "total_domains": len(self.domain_keywords),
            "total_keywords": total_keywords,
            "domains": list(self.domain_keywords.keys()),
            "coverage": "30 major legal areas with comprehensive keyword coverage"
        }


def create_expanded_legal_domains():
    """Factory function"""
    return ExpandedLegalDomains()


if __name__ == "__main__":
    classifier = create_expanded_legal_domains()
    stats = classifier.get_stats()
    
    print("🎯 EXPANDED LEGAL DOMAINS")
    print(f"   Total Domains: {stats['total_domains']}")
    print(f"   Total Keywords: {stats['total_keywords']}")
    print(f"   Coverage: {stats['coverage']}")
    
    print(f"\n📋 Available Domains:")
    for i, domain in enumerate(classifier.get_all_domains(), 1):
        print(f"   {i:2d}. {domain.replace('_', ' ').title()}")
    
    # Test various query types
    test_queries = [
        "Someone murdered my brother",
        "My phone was stolen",
        "I was raped by colleague",
        "Hackers stole my bank account",
        "Doctor's negligence caused death",
        "Builder cheated me in property deal",
        "Boss fired me without notice",
        "Husband beats me daily",
        "Product is defective, want refund",
        "Tax department sent notice",
        "Had an accident with my car",
        "Doctor's malpractice caused injury"
    ]
    
    print(f"\n🧪 Testing Domain Classification:")
    for query in test_queries:
        domain, confidence = classifier.classify_domain(query)
        print(f"   '{query}' → {domain.replace('_', ' ').title()} ({confidence:.3f})")
    
    print("\n✅ Expanded Domain Classifier Ready!")