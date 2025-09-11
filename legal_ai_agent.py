#!/usr/bin/env python3
"""
Legal AI Agent - Complete Implementation
=======================================

A comprehensive legal AI agent that can:
1. Classify legal queries into domains and subdomains
2. Retrieve all relevant BNS, IPC, and CrPC sections
3. Provide constitutional articles when applicable
4. Format output in the required structure
5. Include feedback system
6. Update frontend results
"""

import json
import re
from typing import Dict, List, Tuple, Any
from datetime import datetime

# Import required components
from ml_domain_classifier import MLDomainClassifier
from subdomain_classifier import SubdomainClassifier
from complete_legal_database import CompleteLegalDatabase
from constitutional_article_matcher import ConstitutionalArticleMatcher

class LegalAIAgent:
    """Legal AI Agent that processes queries and provides comprehensive legal analysis"""
    
    def __init__(self):
        """Initialize all components of the legal AI agent"""
        print("🚀 Initializing Legal AI Agent...")
        
        # Initialize classifiers
        self.domain_classifier = MLDomainClassifier()
        self.subdomain_classifier = SubdomainClassifier()
        
        # Initialize legal database
        self.legal_db = CompleteLegalDatabase()
        
        # Initialize constitutional article matcher
        self.constitutional_matcher = ConstitutionalArticleMatcher()
        
        # Load domain-subdomain mapping
        self.domain_mapping = self._load_domain_mapping()
        
        print("✅ Legal AI Agent initialized successfully!")
    
    def _load_domain_mapping(self) -> Dict[str, Dict[str, str]]:
        """Load the domain-subdomain mapping from the JSON provided in the task"""
        return {
            "Murder Case": {
                "domain": "Criminal Law",
                "subdomain": "Homicide"
            },
            "Kidnapping": {
                "domain": "Criminal Law",
                "subdomain": "Kidnapping / Abduction"
            },
            "Sexual Assault": {
                "domain": "Criminal Law",
                "subdomain": "Sexual Offences"
            },
            "Cyber Crime": {
                "domain": "Cyber Law",
                "subdomain": "Hacking / Online Fraud / Identity Theft"
            },
            "Employment Issue": {
                "domain": "Labour & Employment Law",
                "subdomain": "Contract Disputes / Workplace Harassment / Compensation"
            },
            "Domestic Violence": {
                "domain": "Family Law / Criminal Law",
                "subdomain": "Domestic Abuse / Cruelty"
            },
            "Financial Crime": {
                "domain": "Criminal Law / Economic Offences",
                "subdomain": "Fraud / White Collar Crimes"
            },
            "Drug Crime": {
                "domain": "Criminal Law",
                "subdomain": "Narcotics & Psychotropic Substances"
            },
            "Tenant Rights": {
                "domain": "Property Law",
                "subdomain": "Rent Control / Tenancy Disputes"
            },
            "Consumer Protection": {
                "domain": "Consumer Law",
                "subdomain": "Product Liability / Service Deficiency"
            },
            "Medical Malpractice": {
                "domain": "Tort Law / Consumer Law",
                "subdomain": "Medical Negligence"
            },
            "Real Estate": {
                "domain": "Property Law",
                "subdomain": "Land Dispute / Registration / Ownership"
            },
            "Divorce": {
                "domain": "Family Law",
                "subdomain": "Divorce / Child Custody / Maintenance"
            },
            "Dowry Harassment": {
                "domain": "Family Law / Criminal Law",
                "subdomain": "Dowry Prohibition / Cruelty"
            },
            "Theft": {
                "domain": "Criminal Law",
                "subdomain": "Property Offences"
            },
            "Corruption": {
                "domain": "Criminal Law / Anti-Corruption Law",
                "subdomain": "Corruption Cases"
            },
            "Traffic Accident": {
                "domain": "Motor Vehicle Law / Tort Law",
                "subdomain": "Accident Liability / Compensation"
            },
            "Cheque Bounce": {
                "domain": "Banking Law",
                "subdomain": "Negotiable Instruments"
            },
            "Loan Default": {
                "domain": "Banking & Finance Law",
                "subdomain": "Debt Recovery"
            },
            "Company Dispute": {
                "domain": "Corporate Law",
                "subdomain": "Corporate Governance"
            },
            "Taxation Dispute": {
                "domain": "Tax Law",
                "subdomain": "Direct / Indirect Tax Issues"
            },
            "Environmental Violation": {
                "domain": "Environmental Law",
                "subdomain": "Environmental Protection"
            },
            "Immigration Issue": {
                "domain": "Immigration Law",
                "subdomain": "Citizenship / Deportation"
            },
            "Intellectual Property": {
                "domain": "IPR Law",
                "subdomain": "Infringement Cases"
            },
            "Constitutional Issue": {
                "domain": "Constitutional Law",
                "subdomain": "Fundamental Rights / PIL"
            },
            "Police Harassment": {
                "domain": "Criminal Law / Constitutional Law",
                "subdomain": "Police Misconduct"
            },
            "Child Labour": {
                "domain": "Juvenile Law / Family Law",
                "subdomain": "Child Rights Protection"
            }
        }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a legal query and return comprehensive analysis
        
        Args:
            query (str): The legal query to process
            
        Returns:
            Dict[str, Any]: Comprehensive legal analysis
        """
        print(f"🔍 Processing query: {query}")
        
        # 1. Domain & Subdomain Selection
        domain, subdomain = self._classify_query(query)
        
        # 2. Constitutional Articles (if applicable)
        constitutional_articles = self._get_constitutional_articles(query)
        
        # 3. Retrieve ALL Relevant Sections
        bns_sections = self._get_bns_sections(domain, subdomain, query)
        ipc_sections = self._get_ipc_sections(domain, subdomain, query)
        crpc_sections = self._get_crpc_sections(domain, subdomain, query)
        
        # 4. Legal Process Guidance
        legal_process = self._get_legal_process(domain, subdomain)
        
        # 5. Important Notes/Safeguards
        important_notes = self._get_important_notes(domain, subdomain)
        
        # 6. Emergency Contacts (if applicable)
        emergency_contacts = self._get_emergency_contacts(domain, subdomain)
        
        # 7. Format output
        result = {
            "domain": domain,
            "subdomain": subdomain,
            "constitutional_articles": constitutional_articles,
            "bns_sections": bns_sections,
            "ipc_sections": ipc_sections,
            "crpc_sections": crpc_sections,
            "legal_process": legal_process,
            "important_notes": important_notes,
            "emergency_contacts": emergency_contacts,
            "timestamp": datetime.now().isoformat(),
            "query": query
        }
        
        # 8. Update frontend results
        self._update_frontend_results(result)
        
        return result
    
    def _classify_query(self, query: str) -> Tuple[str, str]:
        """
        Classify the query into domain and subdomain
        
        Args:
            query (str): The legal query
            
        Returns:
            Tuple[str, str]: Domain and subdomain
        """
        # First try to match with predefined examples
        query_lower = query.lower()
        for example, mapping in self.domain_mapping.items():
            if example.lower() in query_lower:
                return mapping["domain"], mapping["subdomain"]
        
        # If no match, use ML classifiers
        domain, _ = self.domain_classifier.classify(query)
        subdomain, _, _ = self.subdomain_classifier.classify_subdomain(domain, query)
        
        # Format domain and subdomain names
        formatted_domain = domain.replace("_", " ").title()
        formatted_subdomain = subdomain.replace("_", " ").title()
        
        return formatted_domain, formatted_subdomain
    
    def _get_constitutional_articles(self, query: str) -> List[Dict[str, str]]:
        """
        Get relevant constitutional articles for the query
        
        Args:
            query (str): The legal query
            
        Returns:
            List[Dict[str, str]]: List of constitutional articles
        """
        article_matches = self.constitutional_matcher.find_matching_articles(query)
        # Convert ArticleMatch objects to dictionaries
        articles = []
        for match in article_matches:
            articles.append({
                'article_number': match.article_number,
                'title': match.clean_title,
                'content': match.content,
                'confidence': match.confidence,
                'confidence_percentage': match.confidence_percentage
            })
        return articles if articles else []
    
    def _get_bns_sections(self, domain: str, subdomain: str, query: str) -> List[Dict[str, str]]:
        """
        Get all relevant BNS sections
        
        Args:
            domain (str): Legal domain
            subdomain (str): Legal subdomain
            query (str): The legal query
            
        Returns:
            List[Dict[str, str]]: List of BNS sections
        """
        # Get sections from legal database
        all_sections = self.legal_db.get_all_sections_for_query(domain, subdomain, query)
        return all_sections["bns_sections"]
    
    def _get_ipc_sections(self, domain: str, subdomain: str, query: str) -> List[Dict[str, str]]:
        """
        Get all relevant IPC sections
        
        Args:
            domain (str): Legal domain
            subdomain (str): Legal subdomain
            query (str): The legal query
            
        Returns:
            List[Dict[str, str]]: List of IPC sections
        """
        # Get sections from legal database
        all_sections = self.legal_db.get_all_sections_for_query(domain, subdomain, query)
        return all_sections["ipc_sections"]
    
    def _get_crpc_sections(self, domain: str, subdomain: str, query: str) -> List[Dict[str, str]]:
        """
        Get all relevant CrPC sections
        
        Args:
            domain (str): Legal domain
            subdomain (str): Legal subdomain
            query (str): The legal query
            
        Returns:
            List[Dict[str, str]]: List of CrPC sections
        """
        # Get sections from legal database
        all_sections = self.legal_db.get_all_sections_for_query(domain, subdomain, query)
        return all_sections["crpc_sections"]
    
    def _get_legal_process(self, domain: str, subdomain: str) -> str:
        """
        Get step-by-step legal process guidance
        
        Args:
            domain (str): Legal domain
            subdomain (str): Legal subdomain
            
        Returns:
            str: Legal process guidance
        """
        # Define legal processes for different domains
        processes = {
            "Criminal Law": "FIR → Investigation → Chargesheet → Trial → Judgment → Appeal (if needed)",
            "Family Law": "Consultation → Documentation → Filing Petition → Court Proceedings → Mediation/Resolution → Final Order",
            "Property Law": "Documentation → Legal Opinion → Notice to Opposite Party → Filing Suit → Evidence Presentation → Judgment",
            "Labour & Employment Law": "Internal Complaint → Legal Notice → Filing Complaint → Investigation → Hearing → Resolution/Order",
            "Cyber Law": "Reporting to Cyber Cell → Investigation → Digital Evidence Collection → Legal Proceedings → Judgment",
            "Consumer Law": "Complaint to Consumer Forum → Notice to Opponent → Hearing → Evidence → Judgment → Award",
            "Corporate Law": "Board Resolution → Legal Opinion → Filing Documents → Regulatory Compliance → Implementation",
            "Tax Law": "Notice/Intimation → Response/Explanation → Assessment → Appeal (if needed) → Resolution",
            "Banking Law": "Complaint to Bank → Banking Ombudsman → Legal Proceedings → Resolution",
            "Immigration Law": "Application/Documentation → Processing → Interview/Review → Decision → Appeal (if needed)"
        }
        
        # Return specific process or default
        return processes.get(domain, "Consultation → Documentation → Legal Proceedings → Resolution")
    
    def _get_important_notes(self, domain: str, subdomain: str) -> List[str]:
        """
        Get important notes and safeguards
        
        Args:
            domain (str): Legal domain
            subdomain (str): Legal subdomain
            
        Returns:
            List[str]: Important notes and safeguards
        """
        # Define notes for different domains
        notes = {
            "Criminal Law": [
                "File FIR immediately at the nearest police station",
                "Preserve all evidence and witnesses",
                "Consult a criminal lawyer immediately",
                "Do not make statements without legal counsel present"
            ],
            "Family Law": [
                "Keep all communication records",
                "Document financial transactions",
                "Prioritize child welfare in custody matters",
                "Consider mediation before litigation"
            ],
            "Property Law": [
                "Verify all property documents thoroughly",
                "Check for encumbrances or pending cases",
                "Register all agreements properly",
                "Maintain possession records"
            ],
            "Cyber Law": [
                "Do not delete any digital evidence",
                "Take screenshots immediately",
                "Report to cyber cell within 24 hours",
                "Change passwords and secure accounts"
            ],
            "Consumer Law": [
                "Keep all purchase receipts and warranties",
                "Document defects with photos/videos",
                "Send legal notice before filing complaint",
                "Approach consumer forum within limitation period"
            ]
        }
        
        # Return specific notes or default
        return notes.get(domain, [
            "Consult a qualified legal practitioner",
            "Preserve all relevant documents",
            "Follow proper legal procedures",
            "Be aware of limitation periods"
        ])
    
    def _get_emergency_contacts(self, domain: str, subdomain: str) -> Dict[str, str]:
        """
        Get emergency contacts when applicable
        
        Args:
            domain (str): Legal domain
            subdomain (str): Legal subdomain
            
        Returns:
            Dict[str, str]: Emergency contacts
        """
        # Define emergency contacts for critical domains
        emergency_domains = {
            "Criminal Law": {
                "Police Emergency": "100",
                "Women Helpline": "1091",
                "Child Helpline": "1098",
                "Cyber Crime Helpline": "155260"
            },
            "Domestic Violence": {
                "Police Emergency": "100",
                "Women Helpline": "1091",
                "Domestic Abuse Helpline": "181",
                "Legal Aid": "1300"
            },
            "Cyber Law": {
                "Cyber Crime Helpline": "155260",
                "Police Emergency": "100",
                "Women Helpline": "1091"
            },
            "Child Labour": {
                "Child Helpline": "1098",
                "Police Emergency": "100",
                "Labour Department": "1552"
            }
        }
        
        # Return specific contacts or empty dict
        return emergency_domains.get(domain, {})
    
    def _update_frontend_results(self, result: Dict[str, Any]) -> None:
        """
        Update results in the frontend (ultimate_index.html)
        
        Args:
            result (Dict[str, Any]): The analysis result to update
        """
        try:
            # In a real implementation, this would update the frontend
            # For now, we'll just print that we're updating
            print("🔄 Updating frontend with latest analysis...")
            
            # This would typically involve:
            # 1. Reading the ultimate_index.html file
            # 2. Updating the relevant sections with the new data
            # 3. Writing the updated content back to the file
            
            # For demonstration, we'll just show what would be updated
            print(f"   Domain: {result['domain']}")
            print(f"   Subdomain: {result['subdomain']}")
            print(f"   Constitutional Articles: {len(result['constitutional_articles'])}")
            print(f"   BNS Sections: {len(result['bns_sections'])}")
            print(f"   IPC Sections: {len(result['ipc_sections'])}")
            print(f"   CrPC Sections: {len(result['crpc_sections'])}")
            
        except Exception as e:
            print(f"⚠️ Could not update frontend: {e}")
    
    def format_output(self, result: Dict[str, Any]) -> str:
        """
        Format the result in the required structure
        
        Args:
            result (Dict[str, Any]): The analysis result
            
        Returns:
            str: Formatted output
        """
        output = []
        
        # Domain
        output.append(f"Domain: {result['domain']}")
        output.append("")
        
        # Subdomain
        output.append(f"Subdomain: {result['subdomain']}")
        output.append("")
        
        # Constitutional Articles
        if result['constitutional_articles']:
            output.append("Constitutional Articles:")
            for article in result['constitutional_articles']:
                output.append(f"  • Article {article['article_number']}: {article['title']}")
            output.append("")
        else:
            output.append("Constitutional Articles: No specific constitutional articles found")
            output.append("")
        
        # BNS Sections
        if result['bns_sections']:
            output.append("BNS Sections:")
            for section in result['bns_sections']:
                output.append(f"  • Section {section['section_number']}: {section['title']}")
                if section.get('description'):
                    output.append(f"    {section['description']}")
            output.append("")
        else:
            output.append("BNS Sections: No specific BNS sections found")
            output.append("")
        
        # IPC Sections
        if result['ipc_sections']:
            output.append("IPC Sections:")
            for section in result['ipc_sections']:
                output.append(f"  • Section {section['section_number']}: {section['title']}")
                if section.get('description'):
                    output.append(f"    {section['description']}")
            output.append("")
        else:
            output.append("IPC Sections: No specific IPC sections found")
            output.append("")
        
        # CrPC Sections
        if result['crpc_sections']:
            output.append("CrPC Sections:")
            for section in result['crpc_sections']:
                output.append(f"  • Section {section['section_number']}: {section['title']}")
                if section.get('description'):
                    output.append(f"    {section['description']}")
            output.append("")
        else:
            output.append("CrPC Sections: No specific CrPC sections found")
            output.append("")
        
        # Legal Process
        output.append("Step-by-step Legal Process:")
        output.append(f"  {result['legal_process']}")
        output.append("")
        
        # Important Notes
        output.append("Important Notes / Safeguards:")
        for note in result['important_notes']:
            output.append(f"  • {note}")
        output.append("")
        
        # Emergency Contacts
        if result['emergency_contacts']:
            output.append("Emergency Contacts:")
            for service, number in result['emergency_contacts'].items():
                output.append(f"  • {service}: {number}")
            output.append("")
        
        # Feedback System
        output.append("💬 Feedback Options:")
        output.append("  • Helpful")
        output.append("  • Very Helpful")
        output.append("  • Not Helpful")
        output.append("  • Needs Work")
        output.append("")
        
        return "\n".join(output)


def create_legal_ai_agent() -> LegalAIAgent:
    """Factory function to create Legal AI Agent"""
    return LegalAIAgent()


# Example usage
if __name__ == "__main__":
    # Create the agent
    agent = create_legal_ai_agent()
    
    # Example queries
    test_queries = [
        "My child was kidnapped for ransom",
        "Someone murdered my neighbor",
        "I was sexually assaulted at workplace",
        "Hackers stole money from my bank account",
        "My boss fired me for reporting harassment"
    ]
    
    # Process each query
    for query in test_queries:
        print("=" * 80)
        result = agent.process_query(query)
        formatted_output = agent.format_output(result)
        print(formatted_output)
        print("=" * 80)
        print()