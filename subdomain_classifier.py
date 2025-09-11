#!/usr/bin/env python3
"""
Subdomain Classifier for Legal Agent
===================================

Provides detailed subdomain classification within each main legal domain
to offer more specific and targeted legal guidance.

Features:
- Hierarchical domain -> subdomain classification
- Confidence scoring for subdomain predictions
- Comprehensive subdomain coverage for all legal areas
- ML-based subdomain detection with fallback rules

Author: Legal Agent Team
Version: 1.0.0 - Subdomain Classification
Date: 2025-09-02
"""

import json
import pickle
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubdomainClassifier:
    """Hierarchical subdomain classifier for legal domains"""
    
    def __init__(self):
        """Initialize subdomain classifier"""
        
        # Define comprehensive subdomain structure
        self.domain_subdomains = {
            "criminal_law": {
                "kidnapping": ["kidnapping", "abduction", "ransom", "child abduction", "human trafficking"],
                "rape": ["rape", "sexual assault", "sexual abuse", "molestation", "sexual violence", "was raped"],
                "theft": ["phone theft", "mobile theft", "wallet theft", "purse snatching", "bag theft", "laptop theft", "jewelry theft", "car theft", "bike theft", "pickpocketing", "burglary", "robbery", "stolen property", "house burglary"],
                "cyber_crime": ["phone hacking", "mobile hacking", "computer hacking", "identity theft", "online fraud", "cyberbullying", "data breach", "phishing", "malware", "social media stalking", "email hacking", "online impersonation"],
                "assault": ["physical assault", "battery", "domestic violence", "harassment", "stalking", "threats", "intimidation", "physical abuse"],
                "fraud": ["financial fraud", "cheque fraud", "credit card fraud", "insurance fraud", "bank fraud", "investment fraud", "ponzi scheme", "embezzlement"],
                "drug_offenses": ["drug possession", "drug trafficking", "drug manufacturing", "drug distribution", "substance abuse"],
                "white_collar": ["corporate fraud", "tax evasion", "money laundering", "bribery", "corruption", "insider trading"],
                "traffic_violations": ["drunk driving", "reckless driving", "hit and run", "traffic accidents", "license violations"],
                "other_criminal": ["vandalism", "trespassing", "public disorder", "weapons charges", "juvenile crimes"]
            },
            
            "employment_law": {
                "wrongful_termination": ["fired without cause", "unfair dismissal", "constructive dismissal", "retaliation firing", "discriminatory termination"],
                "workplace_harassment": ["sexual harassment", "bullying", "hostile work environment", "supervisor harassment", "peer harassment"],
                "discrimination": ["gender discrimination", "racial discrimination", "age discrimination", "disability discrimination", "religious discrimination", "pregnancy discrimination"],
                "wage_issues": ["unpaid wages", "overtime violations", "minimum wage violations", "salary disputes", "commission disputes", "bonus disputes", "salary not paid", "not paying salary"],
                "workplace_safety": ["unsafe conditions", "workplace injuries", "OSHA violations", "health hazards", "safety equipment"],
                "confidentiality_breach": ["trade secrets", "non-disclosure violations", "confidential information", "proprietary data", "company secrets"],
                "benefits_disputes": ["health insurance", "retirement benefits", "vacation pay", "sick leave", "family leave"],
                "contract_violations": ["employment contract breach", "non-compete violations", "severance disputes", "job description changes"],
                "whistleblower": ["retaliation", "reporting violations", "protected disclosures", "safety reporting"]
            },
            
            "family_law": {
                "divorce": ["divorce proceedings", "separation", "annulment", "marital dissolution", "uncontested divorce", "contested divorce"],
                "child_custody": ["custody battles", "visitation rights", "parenting plans", "custody modifications", "international custody"],
                "domestic_violence": ["spousal abuse", "child abuse", "restraining orders", "protection orders", "family violence", "domestic abuse"],
                "child_support": ["support payments", "support modifications", "unpaid support", "enforcement", "paternity", "child support", "not paying child support"],
                "alimony": ["spousal support", "maintenance", "alimony modifications", "temporary support", "permanent support"],
                "adoption": ["adoption process", "stepparent adoption", "international adoption", "adoption rights", "birth parent rights"],
                "property_division": ["marital property", "asset division", "debt division", "business valuation", "retirement accounts"],
                "prenuptial": ["prenuptial agreements", "postnuptial agreements", "marital contracts", "property agreements"],
                "guardianship": ["legal guardianship", "conservatorship", "elderly care", "disabled adult care", "minor guardianship"]
            },
            
            "tenant_rights": {
                "security_deposit": ["deposit return", "deposit deductions", "deposit disputes", "deposit withholding", "deposit interest"],
                "eviction": ["unlawful eviction", "eviction notice", "eviction proceedings", "tenant defenses", "eviction timeline"],
                "rent_issues": ["rent increases", "rent control", "rent withholding", "rent disputes", "late fees"],
                "habitability": ["unsafe conditions", "mold problems", "heating issues", "plumbing problems", "electrical issues", "pest control"],
                "landlord_harassment": ["illegal entry", "harassment", "intimidation", "privacy violations", "retaliation"],
                "lease_disputes": ["lease violations", "lease terms", "lease renewal", "lease termination", "subletting"],
                "discrimination": ["housing discrimination", "fair housing", "disability accommodation", "familial status", "source of income"],
                "repairs": ["maintenance requests", "emergency repairs", "landlord obligations", "tenant improvements"],
                "utilities": ["utility shutoffs", "utility responsibilities", "utility deposits", "utility disputes"]
            },
            
            "consumer_complaint": {
                "defective_products": ["product defects", "manufacturing defects", "design defects", "product recalls", "safety hazards", "defective phone", "bought defective"],
                "warranty_issues": ["warranty claims", "warranty denials", "extended warranties", "warranty repairs", "warranty refunds"],
                "online_shopping": ["e-commerce fraud", "delivery issues", "return problems", "fake products", "online scams"],
                "service_disputes": ["poor service", "service failures", "service contracts", "service cancellations", "service billing"],
                "billing_disputes": ["overcharging", "unauthorized charges", "billing errors", "subscription issues", "automatic renewals"],
                "financial_services": ["bank disputes", "credit card issues", "loan problems", "insurance claims", "investment disputes"],
                "telecommunications": ["phone service", "internet service", "cable service", "billing disputes", "service quality"],
                "automotive": ["car repairs", "auto warranties", "lemon law", "dealer fraud", "financing issues"],
                "healthcare": ["medical billing", "insurance denials", "medical malpractice", "prescription issues", "healthcare fraud"],
                "food_safety": ["contaminated food", "food poisoning", "restaurant food", "food safety"]
            },
            
            "personal_injury": {
                "motor_vehicle": ["car accidents", "motorcycle accidents", "truck accidents", "bus accidents", "pedestrian accidents", "bicycle accidents"],
                "slip_and_fall": ["premises liability", "wet floors", "uneven surfaces", "inadequate lighting", "snow and ice", "slipped and fell", "slip and fall"],
                "medical_malpractice": ["surgical errors", "misdiagnosis", "medication errors", "birth injuries", "hospital negligence"],
                "workplace_injury": ["construction accidents", "industrial accidents", "repetitive stress", "toxic exposure", "machinery accidents"],
                "product_liability": ["defective products", "dangerous products", "product recalls", "manufacturing defects", "design defects"],
                "dog_bites": ["animal attacks", "dog bite injuries", "owner liability", "dangerous animals", "premises liability"],
                "wrongful_death": ["fatal accidents", "survival claims", "loss of consortium", "funeral expenses", "lost income"],
                "assault": ["intentional torts", "battery", "false imprisonment", "emotional distress", "assault claims"],
                "toxic_exposure": ["asbestos exposure", "chemical exposure", "environmental toxins", "occupational diseases", "mass torts"]
            },
            
            "contract_dispute": {
                "breach_of_contract": ["material breach", "minor breach", "anticipatory breach", "contract performance", "contract remedies"],
                "employment_contracts": ["non-compete agreements", "employment terms", "severance agreements", "confidentiality agreements"],
                "business_contracts": ["partnership agreements", "vendor contracts", "service agreements", "licensing agreements", "franchise agreements"],
                "real_estate": ["purchase agreements", "lease agreements", "construction contracts", "property management", "real estate closings"],
                "consumer_contracts": ["purchase agreements", "service contracts", "warranty agreements", "subscription agreements", "financing agreements"],
                "construction": ["contractor disputes", "construction delays", "defective work", "change orders", "payment disputes"],
                "intellectual_property": ["licensing disputes", "trademark agreements", "copyright agreements", "patent licensing", "trade secrets"],
                "insurance": ["policy disputes", "claim denials", "coverage disputes", "bad faith claims", "premium disputes"],
                "debt_collection": ["collection practices", "debt validation", "harassment", "credit reporting", "bankruptcy"]
            },
            
            "immigration_law": {
                "visa_issues": ["visa applications", "visa denials", "visa renewals", "visa extensions", "visa violations"],
                "passport_issues": ["passport renewals", "passport applications", "passport delays", "passport denials", "emergency passports"],
                "green_card": ["permanent residency", "green card applications", "green card renewals", "conditional residence", "removal of conditions"],
                "citizenship": ["naturalization", "citizenship applications", "citizenship tests", "dual citizenship", "citizenship ceremonies"],
                "deportation": ["removal proceedings", "deportation defense", "asylum claims", "withholding of removal", "cancellation of removal"],
                "family_immigration": ["family petitions", "spouse visas", "fiancé visas", "parent visas", "child visas"],
                "employment_immigration": ["work visas", "employment petitions", "labor certifications", "investor visas", "specialty occupations"],
                "asylum_refugee": ["asylum applications", "refugee status", "persecution claims", "country conditions", "credibility issues"],
                "student_immigration": ["student visas", "school transfers", "practical training", "academic status", "visa maintenance"]
            },
            
            "elder_abuse": {
                "financial_abuse": ["financial exploitation", "theft from elderly", "power of attorney abuse", "trust violations", "scams targeting seniors"],
                "physical_abuse": ["physical harm", "neglect", "medical neglect", "abandonment", "restraints"],
                "emotional_abuse": ["psychological abuse", "isolation", "intimidation", "threats", "verbal abuse"],
                "institutional_abuse": ["nursing home abuse", "assisted living abuse", "hospital abuse", "caregiver abuse", "facility neglect"],
                "healthcare_abuse": ["medical fraud", "unnecessary procedures", "medication abuse", "healthcare neglect", "insurance fraud"],
                "legal_abuse": ["guardianship abuse", "conservatorship abuse", "legal capacity", "undue influence", "estate planning abuse"],
                "housing_abuse": ["housing fraud", "mortgage scams", "reverse mortgage abuse", "property theft", "housing discrimination"],
                "consumer_fraud": ["telemarketing scams", "internet fraud", "identity theft", "investment fraud", "charity scams"]
            },
            
            "cyber_crime": {
                "identity_theft": ["personal information theft", "financial identity theft", "medical identity theft", "tax identity theft", "child identity theft"],
                "online_fraud": ["e-commerce fraud", "auction fraud", "investment fraud", "romance scams", "phishing scams"],
                "cyberbullying": ["online harassment", "social media bullying", "cyberstalking", "revenge porn", "doxxing"],
                "computer_crimes": ["hacking", "malware", "ransomware", "data breaches", "unauthorized access", "phone is being hacked"],
                "financial_crimes": ["online banking fraud", "credit card fraud", "cryptocurrency fraud", "payment fraud", "wire fraud"],
                "privacy_violations": ["data privacy", "surveillance", "tracking", "personal information misuse", "privacy breaches"],
                "intellectual_property": ["copyright infringement", "trademark violations", "trade secret theft", "piracy", "counterfeiting"],
                "communication_crimes": ["email fraud", "text message scams", "voice phishing", "social engineering", "impersonation"]
            }
        }
        
        # Create training data for subdomain classification
        self.subdomain_training_data = self._create_subdomain_training_data()
        
        # Initialize ML components for each domain
        self.domain_classifiers = {}
        self.domain_vectorizers = {}
        
        # Train subdomain classifiers
        self._train_subdomain_classifiers()
        
        logger.info(f"Subdomain classifier initialized with {len(self.domain_subdomains)} domains")
    
    def _create_subdomain_training_data(self) -> Dict[str, List[Dict]]:
        """Create training data for subdomain classification"""
        
        training_data = {}
        
        for domain, subdomains in self.domain_subdomains.items():
            training_data[domain] = []
            
            for subdomain, keywords in subdomains.items():
                # Create training examples for each subdomain
                for keyword in keywords:
                    # Create variations of the keyword
                    examples = [
                        f"I have a problem with {keyword}",
                        f"Need help with {keyword}",
                        f"Issue related to {keyword}",
                        f"Legal advice for {keyword}",
                        f"My case involves {keyword}",
                        keyword,
                        f"{keyword} legal help",
                        f"{keyword} assistance needed"
                    ]
                    
                    for example in examples:
                        training_data[domain].append({
                            "text": example,
                            "subdomain": subdomain
                        })
        
        return training_data
    
    def _train_subdomain_classifiers(self):
        """Train ML classifiers for each domain's subdomains"""
        
        for domain, training_examples in self.subdomain_training_data.items():
            if len(training_examples) < 2:
                continue
            
            # Prepare training data
            texts = [example["text"] for example in training_examples]
            subdomains = [example["subdomain"] for example in training_examples]
            
            # Create and train vectorizer
            vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=1000,
                lowercase=True
            )
            
            try:
                X = vectorizer.fit_transform(texts)
                
                # Train classifier
                classifier = MultinomialNB(alpha=0.1)
                classifier.fit(X, subdomains)
                
                # Store trained components
                self.domain_vectorizers[domain] = vectorizer
                self.domain_classifiers[domain] = classifier
                
                logger.info(f"Trained subdomain classifier for {domain} with {len(set(subdomains))} subdomains")
                
            except Exception as e:
                logger.warning(f"Failed to train classifier for {domain}: {e}")
    
    def classify_subdomain(self, domain: str, query: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """
        Classify subdomain within a given domain
        
        Args:
            domain: Main legal domain
            query: User query text
            
        Returns:
            Tuple of (primary_subdomain, confidence, alternative_subdomains)
        """
        
        # Clean domain name
        domain = domain.lower().replace(' ', '_')
        
        # Check if we have a classifier for this domain
        if domain not in self.domain_classifiers:
            return self._fallback_subdomain_classification(domain, query)
        
        try:
            # Vectorize query
            vectorizer = self.domain_vectorizers[domain]
            classifier = self.domain_classifiers[domain]
            
            query_vector = vectorizer.transform([query.lower()])
            
            # Get predictions with probabilities
            probabilities = classifier.predict_proba(query_vector)[0]
            classes = classifier.classes_
            
            # Create sorted list of predictions
            subdomain_scores = list(zip(classes, probabilities))
            subdomain_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get primary prediction
            primary_subdomain, primary_confidence = subdomain_scores[0]
            
            # Enhance with keyword matching
            enhanced_scores = self._enhance_with_keywords(domain, query, subdomain_scores)
            
            return enhanced_scores[0][0], enhanced_scores[0][1], enhanced_scores[:3]
            
        except Exception as e:
            logger.warning(f"Error in subdomain classification for {domain}: {e}")
            return self._fallback_subdomain_classification(domain, query)
    
    def _enhance_with_keywords(self, domain: str, query: str, ml_scores: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """Enhance ML predictions with keyword matching"""
        
        query_lower = query.lower()
        enhanced_scores = {}
        
        # Start with ML scores (weight 0.7)
        for subdomain, score in ml_scores:
            enhanced_scores[subdomain] = score * 0.7
        
        # Add keyword matching scores (weight 0.3)
        if domain in self.domain_subdomains:
            for subdomain, keywords in self.domain_subdomains[domain].items():
                keyword_score = 0
                for keyword in keywords:
                    if keyword.lower() in query_lower:
                        keyword_score += 1
                
                # Normalize keyword score
                if keywords:
                    keyword_score = keyword_score / len(keywords)
                
                # Add to enhanced score
                if subdomain in enhanced_scores:
                    enhanced_scores[subdomain] += keyword_score * 0.3
                else:
                    enhanced_scores[subdomain] = keyword_score * 0.3
        
        # Sort by enhanced score
        sorted_scores = sorted(enhanced_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_scores
    
    def _fallback_subdomain_classification(self, domain: str, query: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Fallback subdomain classification using keyword matching"""
        
        if domain not in self.domain_subdomains:
            return "general", 0.5, [("general", 0.5)]
        
        query_lower = query.lower()
        subdomain_scores = {}
        
        # Score each subdomain based on keyword matches
        for subdomain, keywords in self.domain_subdomains[domain].items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    score += 1
            
            # Normalize score
            if keywords:
                subdomain_scores[subdomain] = score / len(keywords)
            else:
                subdomain_scores[subdomain] = 0
        
        # Sort by score
        sorted_subdomains = sorted(subdomain_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_subdomains and sorted_subdomains[0][1] > 0:
            return sorted_subdomains[0][0], sorted_subdomains[0][1], sorted_subdomains[:3]
        else:
            return "general", 0.3, [("general", 0.3)]
    
    def get_subdomain_info(self, domain: str, subdomain: str) -> Dict[str, Any]:
        """Get detailed information about a specific subdomain"""
        
        domain = domain.lower().replace(' ', '_')
        
        if domain not in self.domain_subdomains:
            return {"error": f"Domain '{domain}' not found"}
        
        if subdomain not in self.domain_subdomains[domain]:
            return {"error": f"Subdomain '{subdomain}' not found in domain '{domain}'"}
        
        return {
            "domain": domain,
            "subdomain": subdomain,
            "keywords": self.domain_subdomains[domain][subdomain],
            "description": self._get_subdomain_description(domain, subdomain)
        }
    
    def _get_subdomain_description(self, domain: str, subdomain: str) -> str:
        """Get human-readable description of subdomain"""
        
        descriptions = {
            "criminal_law": {
                "theft": "Physical theft of property including phones, wallets, vehicles, and other personal belongings",
                "cyber_crime": "Digital crimes including hacking, online fraud, identity theft, and cyberbullying",
                "assault": "Physical or verbal attacks, domestic violence, harassment, and threats",
                "fraud": "Financial deception including check fraud, credit card fraud, and investment scams",
                "drug_offenses": "Drug-related crimes including possession, trafficking, and manufacturing",
                "white_collar": "Corporate crimes including fraud, tax evasion, bribery, and corruption",
                "traffic_violations": "Vehicle-related offenses including drunk driving and traffic accidents",
                "other_criminal": "Other criminal activities including vandalism, trespassing, and weapons charges"
            },
            "employment_law": {
                "wrongful_termination": "Unfair or illegal firing from employment",
                "workplace_harassment": "Harassment, bullying, or hostile work environment",
                "discrimination": "Workplace discrimination based on protected characteristics",
                "wage_issues": "Problems with pay, overtime, or wage theft",
                "workplace_safety": "Unsafe working conditions and workplace injuries",
                "confidentiality_breach": "Violations of confidentiality and trade secret agreements",
                "benefits_disputes": "Issues with health insurance, retirement, and other benefits",
                "contract_violations": "Breaches of employment contracts and agreements",
                "whistleblower": "Retaliation for reporting workplace violations"
            },
            "family_law": {
                "divorce": "Marriage dissolution and separation proceedings",
                "child_custody": "Child custody, visitation, and parenting arrangements",
                "domestic_violence": "Family violence, abuse, and protection orders",
                "child_support": "Child support payments and enforcement",
                "alimony": "Spousal support and maintenance payments",
                "adoption": "Adoption processes and parental rights",
                "property_division": "Division of marital assets and debts",
                "prenuptial": "Prenuptial and postnuptial agreements",
                "guardianship": "Legal guardianship and conservatorship matters"
            },
            "tenant_rights": {
                "security_deposit": "Security deposit return and dispute issues",
                "eviction": "Eviction proceedings and tenant defenses",
                "rent_issues": "Rent increases, disputes, and payment problems",
                "habitability": "Unsafe or unhealthy living conditions",
                "landlord_harassment": "Landlord harassment and privacy violations",
                "lease_disputes": "Lease agreement violations and disputes",
                "discrimination": "Housing discrimination and fair housing violations",
                "repairs": "Maintenance and repair responsibilities",
                "utilities": "Utility service and billing disputes"
            },
            "consumer_complaint": {
                "defective_products": "Defective or dangerous products and recalls",
                "warranty_issues": "Warranty claims and coverage disputes",
                "online_shopping": "E-commerce fraud and delivery problems",
                "service_disputes": "Poor service quality and contract violations",
                "billing_disputes": "Billing errors and unauthorized charges",
                "financial_services": "Banking, credit, and insurance disputes",
                "telecommunications": "Phone, internet, and cable service issues",
                "automotive": "Car repairs, warranties, and dealer fraud",
                "healthcare": "Medical billing and healthcare service issues"
            },
            "personal_injury": {
                "motor_vehicle": "Car, motorcycle, and other vehicle accidents",
                "slip_and_fall": "Premises liability and slip and fall accidents",
                "medical_malpractice": "Medical errors and healthcare negligence",
                "workplace_injury": "Work-related injuries and accidents",
                "product_liability": "Injuries caused by defective products",
                "dog_bites": "Animal attacks and owner liability",
                "wrongful_death": "Fatal accidents and wrongful death claims",
                "assault": "Intentional harm and assault claims",
                "toxic_exposure": "Exposure to harmful substances and chemicals"
            },
            "contract_dispute": {
                "breach_of_contract": "Violations of contract terms and agreements",
                "employment_contracts": "Employment agreement disputes",
                "business_contracts": "Business partnership and vendor disputes",
                "real_estate": "Real estate transaction and property disputes",
                "consumer_contracts": "Consumer purchase and service agreements",
                "construction": "Construction contract and contractor disputes",
                "intellectual_property": "IP licensing and agreement disputes",
                "insurance": "Insurance policy and claim disputes",
                "debt_collection": "Debt collection and credit disputes"
            },
            "immigration_law": {
                "visa_issues": "Visa applications, renewals, and violations",
                "passport_issues": "Passport applications, renewals, and problems",
                "green_card": "Permanent residency and green card matters",
                "citizenship": "Naturalization and citizenship applications",
                "deportation": "Removal proceedings and deportation defense",
                "family_immigration": "Family-based immigration petitions",
                "employment_immigration": "Work-based immigration and visas",
                "asylum_refugee": "Asylum and refugee status applications",
                "student_immigration": "Student visas and academic status"
            },
            "elder_abuse": {
                "financial_abuse": "Financial exploitation and theft from elderly",
                "physical_abuse": "Physical harm, neglect, and abandonment",
                "emotional_abuse": "Psychological abuse and emotional harm",
                "institutional_abuse": "Nursing home and care facility abuse",
                "healthcare_abuse": "Medical fraud and healthcare neglect",
                "legal_abuse": "Guardianship and legal capacity abuse",
                "housing_abuse": "Housing fraud and property theft",
                "consumer_fraud": "Scams and fraud targeting seniors"
            },
            "cyber_crime": {
                "identity_theft": "Theft and misuse of personal information",
                "online_fraud": "Internet fraud and online scams",
                "cyberbullying": "Online harassment and cyberbullying",
                "computer_crimes": "Hacking, malware, and computer intrusion",
                "financial_crimes": "Online financial fraud and theft",
                "privacy_violations": "Data privacy and surveillance issues",
                "intellectual_property": "Online IP theft and infringement",
                "communication_crimes": "Email fraud and communication scams"
            }
        }
        
        return descriptions.get(domain, {}).get(subdomain, f"Legal matters related to {subdomain.replace('_', ' ')}")
    
    def get_all_subdomains(self, domain: str = None) -> Dict[str, Any]:
        """Get all available subdomains, optionally filtered by domain"""
        
        if domain:
            domain = domain.lower().replace(' ', '_')
            if domain in self.domain_subdomains:
                return {domain: self.domain_subdomains[domain]}
            else:
                return {"error": f"Domain '{domain}' not found"}
        
        return self.domain_subdomains
    
    def get_stats(self) -> Dict[str, Any]:
        """Get classifier statistics"""
        
        total_subdomains = sum(len(subdomains) for subdomains in self.domain_subdomains.values())
        trained_domains = len(self.domain_classifiers)
        
        return {
            "total_domains": len(self.domain_subdomains),
            "total_subdomains": total_subdomains,
            "trained_classifiers": trained_domains,
            "training_examples": sum(len(examples) for examples in self.subdomain_training_data.values()),
            "domains": list(self.domain_subdomains.keys())
        }


def create_subdomain_classifier() -> SubdomainClassifier:
    """Factory function to create subdomain classifier"""
    return SubdomainClassifier()


# Test the subdomain classifier
if __name__ == "__main__":
    print("🎯 SUBDOMAIN CLASSIFIER TEST")
    print("=" * 50)
    
    classifier = create_subdomain_classifier()
    
    # Test queries with expected subdomains
    test_cases = [
        ("criminal_law", "my phone is stolen", "theft"),
        ("criminal_law", "someone is hacking my phone", "cyber_crime"),
        ("employment_law", "I was fired from my job", "wrongful_termination"),
        ("employment_law", "employee disclosed company secrets", "confidentiality_breach"),
        ("family_law", "I want to divorce my spouse", "divorce"),
        ("family_law", "child custody battle", "child_custody"),
        ("tenant_rights", "landlord won't return deposit", "security_deposit"),
        ("tenant_rights", "apartment has mold problems", "habitability"),
        ("consumer_complaint", "bought defective phone", "defective_products"),
        ("consumer_complaint", "warranty claim denied", "warranty_issues"),
        ("personal_injury", "car accident injury", "motor_vehicle"),
        ("personal_injury", "slip and fall at store", "slip_and_fall"),
        ("immigration_law", "passport is expired", "passport_issues"),
        ("immigration_law", "visa application denied", "visa_issues"),
        ("cyber_crime", "identity theft online", "identity_theft"),
        ("cyber_crime", "cyberbullying on social media", "cyberbullying")
    ]
    
    print(f"📊 Classifier Stats:")
    stats = classifier.get_stats()
    print(f"   Domains: {stats['total_domains']}")
    print(f"   Subdomains: {stats['total_subdomains']}")
    print(f"   Trained Classifiers: {stats['trained_classifiers']}")
    print(f"   Training Examples: {stats['training_examples']}")
    
    print(f"\n🧪 Testing Subdomain Classification:")
    print("-" * 50)
    
    correct_predictions = 0
    total_predictions = len(test_cases)
    
    for domain, query, expected_subdomain in test_cases:
        subdomain, confidence, alternatives = classifier.classify_subdomain(domain, query)
        
        is_correct = subdomain == expected_subdomain
        if is_correct:
            correct_predictions += 1
        
        status = "✅" if is_correct else "❌"
        print(f"\n{status} Domain: {domain}")
        print(f"   Query: \"{query}\"")
        print(f"   Predicted: {subdomain} (confidence: {confidence:.3f})")
        print(f"   Expected: {expected_subdomain}")
        
        if alternatives and len(alternatives) > 1:
            print("   Alternatives:")
            for alt_subdomain, alt_conf in alternatives[1:3]:
                print(f"     • {alt_subdomain} (confidence: {alt_conf:.3f})")
    
    accuracy = correct_predictions / total_predictions
    print(f"\n📈 Accuracy: {accuracy:.1%} ({correct_predictions}/{total_predictions})")
    print(f"\n✅ Subdomain Classifier ready for integration!")
    print(f"🎯 Provides detailed subdomain classification within each legal domain")