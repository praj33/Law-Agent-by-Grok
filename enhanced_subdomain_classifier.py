#!/usr/bin/env python3
"""
Enhanced Subdomain Classifier - Handles ANY Query Type
=====================================================
"""

from typing import Dict, List, Tuple, Optional, Any
import re


class EnhancedSubdomainClassifier:
    """Enhanced classifier for ANY type of legal query"""
    
    def __init__(self):
        self.domain_subdomains = self._init_comprehensive_subdomains()
    
    def _init_comprehensive_subdomains(self):
        return {
            "criminal_law": {
                "murder": ["murder", "kill", "death", "homicide", "assassinate", "slay"],
                "kidnapping": ["kidnap", "abduct", "ransom", "hostage", "captive"],
                "theft": ["theft", "steal", "stolen", "burglary", "pickpocket", "shoplifting"],
                "robbery": ["rob", "robbery", "loot", "heist", "armed robbery"],
                "assault": ["assault", "attack", "beat", "hit", "violence", "fight"],
                "rape": ["rape", "sexual assault", "molestation", "sexual abuse"],
                "fraud": ["fraud", "cheat", "scam", "deceive", "con", "swindle"],
                "cybercrime": ["hack", "cyber", "online fraud", "phishing", "malware"],
                "drug_crimes": ["drug", "narcotic", "substance", "cocaine", "heroin"],
                "terrorism": ["terror", "bomb", "explosive", "terrorist"],
                "extortion": ["extortion", "blackmail", "ransom", "threat for money"],
                "forgery": ["forge", "fake document", "counterfeit", "false papers"],
                "domestic_violence": ["domestic violence", "wife beating", "husband abuse"],
                "acid_attack": ["acid", "chemical attack", "disfigure"],
                "dowry": ["dowry", "dowry death", "dowry harassment"],
                "honor_killing": ["honor killing", "family honor", "honor crime"],
                "human_trafficking": ["trafficking", "slave", "forced labor", "prostitution"],
                "money_laundering": ["money laundering", "black money", "illegal funds"],
                "corruption": ["corruption", "bribe", "kickback", "graft"],
                "smuggling": ["smuggling", "contraband", "illegal import", "bootleg"],
                "arson": ["arson", "fire", "burn", "incendiary"],
                "vandalism": ["vandalism", "damage property", "graffiti", "destruction"]
            },
            
            "sexual_offences": {
                "rape": ["rape", "sexual intercourse", "forced sex", "non-consensual"],
                "gang_rape": ["gang rape", "multiple rapists", "group assault"],
                "child_sexual_abuse": ["child abuse", "pedophile", "minor sexual", "underage"],
                "sexual_harassment": ["sexual harassment", "unwanted advances", "inappropriate touch"],
                "stalking": ["stalking", "following", "persistent contact", "obsessive"],
                "voyeurism": ["voyeurism", "peeping", "hidden camera", "spy"],
                "eve_teasing": ["eve teasing", "street harassment", "catcalling"],
                "molestation": ["molestation", "inappropriate touching", "groping"],
                "indecent_exposure": ["indecent exposure", "flashing", "exhibitionism"],
                "pornography": ["pornography", "obscene material", "adult content"],
                "prostitution": ["prostitution", "sex work", "brothel", "escort"],
                "marital_rape": ["marital rape", "spousal rape", "husband force"]
            },
            
            "property_crimes": {
                "theft": ["theft", "stealing", "stolen", "take without permission"],
                "burglary": ["burglary", "break in", "house breaking", "trespass"],
                "robbery": ["robbery", "armed robbery", "mugging", "hold up"],
                "dacoity": ["dacoity", "gang robbery", "group theft", "banditry"],
                "cheating": ["cheating", "fraud", "deception", "con game"],
                "criminal_breach_trust": ["breach of trust", "embezzlement", "misappropriation"],
                "receiving_stolen_goods": ["receiving stolen", "buying stolen", "fence"],
                "extortion": ["extortion", "blackmail", "protection money", "ransom"],
                "criminal_trespass": ["trespass", "unauthorized entry", "intrusion"],
                "mischief": ["mischief", "damage property", "vandalism", "destruction"],
                "counterfeiting": ["counterfeit", "fake currency", "forged money"],
                "identity_theft": ["identity theft", "impersonation", "fake identity"],
                "credit_card_fraud": ["credit card fraud", "card cloning", "skimming"],
                "insurance_fraud": ["insurance fraud", "false claim", "staged accident"],
                "tax_evasion": ["tax evasion", "tax fraud", "undeclared income"]
            },
            
            "violent_crimes": {
                "murder": ["murder", "killing", "homicide", "assassination"],
                "attempt_murder": ["attempt murder", "try to kill", "attempted killing"],
                "culpable_homicide": ["culpable homicide", "causing death", "negligent death"],
                "hurt": ["hurt", "injury", "harm", "wound"],
                "grievous_hurt": ["grievous hurt", "serious injury", "permanent damage"],
                "assault": ["assault", "attack", "battery", "violence"],
                "kidnapping": ["kidnapping", "abduction", "hostage", "captivity"],
                "wrongful_restraint": ["wrongful restraint", "illegal detention", "confinement"],
                "acid_attack": ["acid attack", "chemical assault", "disfigurement"],
                "dowry_death": ["dowry death", "bride burning", "dowry murder"],
                "lynching": ["lynching", "mob violence", "vigilante justice"],
                "rioting": ["rioting", "mob violence", "public disorder"],
                "unlawful_assembly": ["unlawful assembly", "illegal gathering", "mob"],
                "affray": ["affray", "public fighting", "street fight"],
                "criminal_intimidation": ["intimidation", "threat", "menace", "coercion"]
            },
            
            "cyber_crime": {
                "hacking": ["hacking", "hacked", "unauthorized access", "computer intrusion", "phone hacked"],
                "identity_theft": ["identity theft", "personal data theft", "account takeover"],
                "online_fraud": ["online fraud", "internet scam", "e-commerce fraud"],
                "cyberbullying": ["cyberbullying", "online harassment", "digital abuse"],
                "phishing": ["phishing", "fake email", "credential theft"],
                "malware": ["malware", "virus", "trojan", "ransomware"],
                "data_breach": ["data breach", "information leak", "privacy violation"],
                "online_stalking": ["online stalking", "cyber stalking", "digital harassment"],
                "revenge_porn": ["revenge porn", "non-consensual sharing", "intimate images"],
                "fake_news": ["fake news", "misinformation", "false information"],
                "online_gambling": ["online gambling", "illegal betting", "cyber casino"],
                "cryptocurrency_fraud": ["crypto fraud", "bitcoin scam", "digital currency"],
                "social_media_abuse": ["social media abuse", "platform harassment"],
                "email_fraud": ["email fraud", "business email compromise", "CEO fraud"],
                "online_impersonation": ["online impersonation", "fake profile", "catfishing"]
            },
            
            "employment_law": {
                "wrongful_termination": ["wrongful termination", "illegal firing", "unfair dismissal"],
                "sexual_harassment": ["workplace harassment", "sexual harassment", "inappropriate behavior"],
                "discrimination": ["discrimination", "bias", "unfair treatment", "prejudice"],
                "wage_theft": ["wage theft", "unpaid salary", "overtime violation"],
                "workplace_safety": ["workplace safety", "occupational hazard", "unsafe conditions"],
                "retaliation": ["retaliation", "revenge", "punishment for complaint"],
                "constructive_dismissal": ["constructive dismissal", "forced resignation"],
                "breach_of_contract": ["contract breach", "agreement violation", "terms violation"],
                "whistleblower": ["whistleblower", "reporting violations", "exposing wrongdoing"],
                "union_busting": ["union busting", "anti-union", "labor suppression"],
                "child_labor": ["child labor", "underage work", "minor employment"],
                "forced_labor": ["forced labor", "bonded labor", "slavery"],
                "maternity_discrimination": ["maternity discrimination", "pregnancy bias"],
                "disability_discrimination": ["disability discrimination", "accessibility issues"],
                "age_discrimination": ["age discrimination", "ageism", "elderly bias"]
            },
            
            "family_law": {
                "divorce": ["divorce", "separation", "marriage dissolution", "split"],
                "child_custody": ["child custody", "custody battle", "parental rights"],
                "domestic_violence": ["domestic violence", "family abuse", "spousal abuse"],
                "child_abuse": ["child abuse", "child neglect", "minor harm"],
                "alimony": ["alimony", "spousal support", "maintenance", "financial support"],
                "property_division": ["property division", "asset split", "marital property"],
                "adoption": ["adoption", "child adoption", "legal guardianship"],
                "paternity": ["paternity", "fatherhood", "biological father"],
                "bigamy": ["bigamy", "multiple marriage", "polygamy"],
                "dowry_harassment": ["dowry harassment", "dowry demand", "bride price"],
                "elder_abuse": ["elder abuse", "senior abuse", "elderly neglect"],
                "inheritance": ["inheritance", "will dispute", "estate battle"],
                "guardianship": ["guardianship", "legal custody", "ward"],
                "prenuptial": ["prenuptial", "pre-marriage agreement", "prenup"],
                "annulment": ["annulment", "marriage cancellation", "void marriage"]
            },
            
            "financial_crimes": {
                "fraud": ["fraud", "financial deception", "monetary scam"],
                "embezzlement": ["embezzlement", "fund misappropriation", "stealing money"],
                "money_laundering": ["money laundering", "dirty money", "illegal funds"],
                "tax_evasion": ["tax evasion", "tax fraud", "avoiding taxes"],
                "insider_trading": ["insider trading", "stock manipulation", "securities fraud"],
                "ponzi_scheme": ["ponzi scheme", "pyramid scheme", "investment fraud"],
                "credit_fraud": ["credit fraud", "loan fraud", "banking fraud"],
                "insurance_fraud": ["insurance fraud", "false claims", "staged incidents"],
                "bankruptcy_fraud": ["bankruptcy fraud", "asset hiding", "false bankruptcy"],
                "bribery": ["bribery", "corruption", "kickback", "payoff"],
                "forgery": ["forgery", "document fraud", "fake papers"],
                "counterfeiting": ["counterfeiting", "fake currency", "counterfeit goods"],
                "check_fraud": ["check fraud", "bounced check", "fake check"],
                "wire_fraud": ["wire fraud", "electronic fraud", "transfer fraud"],
                "mortgage_fraud": ["mortgage fraud", "property fraud", "real estate scam"]
            },
            
            "drug_crimes": {
                "possession": ["drug possession", "having drugs", "controlled substance", "found with drugs", "caught with drugs"],
                "trafficking": ["drug trafficking", "drug dealing", "narcotics trade"],
                "manufacturing": ["drug manufacturing", "producing drugs", "drug lab"],
                "distribution": ["drug distribution", "selling drugs", "drug supply"],
                "smuggling": ["drug smuggling", "narcotics smuggling", "border drugs", "airport drugs", "customs drugs", "caught with drugs at airport", "drugs at airport"],
                "prescription_fraud": ["prescription fraud", "fake prescription", "pill mill"],
                "money_laundering": ["drug money laundering", "narcotics proceeds"],
                "conspiracy": ["drug conspiracy", "narcotics conspiracy", "drug ring"],
                "cultivation": ["drug cultivation", "growing drugs", "cannabis farming"],
                "paraphernalia": ["drug paraphernalia", "drug equipment", "drug tools"],
                "under_influence": ["under influence", "intoxicated", "high on drugs"],
                "driving_under_influence": ["drunk driving", "DUI", "impaired driving"],
                "public_intoxication": ["public intoxication", "drunk in public"],
                "drug_induced": ["drug induced crime", "drug related violence"],
                "rehabilitation": ["drug rehabilitation", "addiction treatment", "recovery"],
                "airport_customs": ["caught with drugs at airport", "airport drugs", "customs drugs", "drug smuggling airport", "narcotics airport", "airport security drugs"]
            },
            
            "public_order": {
                "rioting": ["rioting", "public disorder", "mob violence"],
                "unlawful_assembly": ["unlawful assembly", "illegal gathering", "prohibited meeting"],
                "sedition": ["sedition", "anti-government", "inciting rebellion"],
                "terrorism": ["terrorism", "terrorist act", "extremism"],
                "public_nuisance": ["public nuisance", "disturbing peace", "noise pollution"],
                "obscenity": ["obscenity", "indecent behavior", "public indecency"],
                "hate_speech": ["hate speech", "communal tension", "inflammatory remarks"],
                "defamation": ["defamation", "character assassination", "reputation damage"],
                "contempt_of_court": ["contempt of court", "disrespecting court", "judicial contempt"],
                "perjury": ["perjury", "false testimony", "lying under oath"],
                "obstruction_of_justice": ["obstruction of justice", "interfering investigation"],
                "escape_from_custody": ["escape from custody", "jail break", "absconding"],
                "harboring_criminal": ["harboring criminal", "hiding fugitive", "aiding escape"],
                "vigilantism": ["vigilantism", "taking law in hands", "mob justice"],
                "bandh": ["bandh", "strike", "protest", "demonstration"]
            },
            "personal_injury": {
                "motor_vehicle": ["car accident", "vehicle collision", "motorcycle crash", "truck accident", "bus crash", "hit and run", "road accident", "car crash", "accident with car", "vehicle accident", "motor vehicle", "car accident"],
                "medical_malpractice": ["medical negligence", "doctor error", "surgical mistake", "misdiagnosis", "wrong medication", "hospital error", "malpractice", "doctor's malpractice", "medical malpractice", "surgical error", "hospital negligence"],
                "slip_and_fall": ["slip and fall", "trip and fall", "wet floor", "uneven surface", "pothole", "obstacle"],
                "workplace_injury": ["work injury", "occupational hazard", "industrial accident", "construction injury", "factory accident"],
                "product_liability": ["defective product", "dangerous product", "product recall", "manufacturing defect", "design flaw"],
                "dog_bites": ["dog bite", "animal attack", "pet attack", "dog attack", "animal bite"],
                "wrongful_death": ["wrongful death", "fatal accident", "death due to negligence", "survival claim"],
                "assault": ["assault", "battery", "physical attack", "intentional harm"],
                "toxic_exposure": ["toxic exposure", "chemical exposure", "asbestos", "lead poisoning", "environmental toxin"]
            }
        }
    
    def classify_subdomain(self, domain: str, query: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Classify subdomain for ANY query type"""
        
        domain = domain.lower().replace(' ', '_')
        query_lower = query.lower()
        
        if domain not in self.domain_subdomains:
            return "general", 0.5, [("general", 0.5)]
        
        subdomain_scores = {}
        
        # Score each subdomain based on keyword matches
        for subdomain, keywords in self.domain_subdomains[domain].items():
            score = 0
            matches = 0
            
            for keyword in keywords:
                # Check for partial matches as well as exact matches
                if keyword in query_lower:
                    score += len(keyword.split())  # Multi-word keywords get higher score
                    matches += 1
                # Also check if any word in the keyword is in the query
                elif any(word in query_lower for word in keyword.split()):
                    score += len(keyword.split()) * 0.5  # Partial match gets lower score
                    matches += 0.5
            
            if matches > 0:
                subdomain_scores[subdomain] = score / len(keywords) + (matches * 0.1)
            else:
                subdomain_scores[subdomain] = 0
        
        # Sort by score
        sorted_subdomains = sorted(subdomain_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_subdomains and sorted_subdomains[0][1] > 0:
            primary = sorted_subdomains[0]
            alternatives = sorted_subdomains[1:4]  # Top 3 alternatives
            return primary[0], min(primary[1], 0.95), alternatives
        else:
            return "general", 0.3, [("general", 0.3)]
    
    def get_subdomain_info(self, domain: str, subdomain: str) -> Dict[str, Any]:
        """Get subdomain information"""
        
        domain = domain.lower().replace(' ', '_')
        
        if domain not in self.domain_subdomains:
            return {"error": f"Domain '{domain}' not found"}
        
        if subdomain not in self.domain_subdomains[domain]:
            return {"error": f"Subdomain '{subdomain}' not found"}
        
        return {
            "domain": domain,
            "subdomain": subdomain,
            "keywords": self.domain_subdomains[domain][subdomain],
            "description": f"Legal matters related to {subdomain.replace('_', ' ')}"
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get classifier statistics"""
        
        total_subdomains = sum(len(subdomains) for subdomains in self.domain_subdomains.values())
        
        return {
            "total_domains": len(self.domain_subdomains),
            "total_subdomains": total_subdomains,
            "domains": list(self.domain_subdomains.keys()),
            "coverage": "Handles ANY type of legal query"
        }


def create_enhanced_subdomain_classifier():
    return EnhancedSubdomainClassifier()


if __name__ == "__main__":
    classifier = create_enhanced_subdomain_classifier()
    stats = classifier.get_stats()
    
    print("🎯 ENHANCED SUBDOMAIN CLASSIFIER")
    print(f"   Domains: {stats['total_domains']}")
    print(f"   Subdomains: {stats['total_subdomains']}")
    print(f"   Coverage: {stats['coverage']}")
    
    # Test various query types
    test_queries = [
        ("criminal_law", "someone murdered my brother"),
        ("criminal_law", "my child was kidnapped for ransom"),
        ("sexual_offences", "I was raped by my colleague"),
        ("cyber_crime", "someone hacked my bank account"),
        ("employment_law", "I was fired for reporting harassment"),
        ("family_law", "my husband beats me daily"),
        ("financial_crimes", "my business partner embezzled money"),
        ("drug_crimes", "caught with cocaine possession"),
        ("public_order", "arrested during protest riot"),
        ("personal_injury", "had an accident with my car"),
        ("personal_injury", "doctor's malpractice caused injury")
    ]
    
    print(f"\n🧪 Testing Query Coverage:")
    for domain, query in test_queries:
        subdomain, confidence, alternatives = classifier.classify_subdomain(domain, query)
        print(f"   '{query}' → {subdomain} ({confidence:.3f})")
    
    print("\n✅ Enhanced Classifier Ready for ANY Query Type!")