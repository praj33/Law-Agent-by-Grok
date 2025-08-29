"""
Enhanced Legal Backing System - Production Grade
================================================

This module provides enhanced legal backing that includes:
- Relevant legal acts and sections (IT Act 2000, IPC, etc.)
- Proper constitutional articles based on legal context
- Production-grade legal references without misleading confidence percentages
- Context-aware legal backing for different domains

Author: Legal Agent Team  
Version: 1.0.0 - Production Grade Legal Backing
Date: 2025-08-28
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalActReference:
    """Structure for legal act references"""
    act_name: str
    sections: List[str]
    description: str
    relevance_reason: str


@dataclass
class ConstitutionalReference:
    """Structure for constitutional references"""
    article_number: str
    title: str
    relevance_reason: str
    is_primary: bool = False


@dataclass
class EnhancedLegalBacking:
    """Complete legal backing structure"""
    constitutional_articles: List[ConstitutionalReference]
    legal_acts: List[LegalActReference]
    primary_laws: List[str]
    domain: str
    backing_summary: str


class EnhancedLegalBackingSystem:
    """Production-grade legal backing system"""
    
    def __init__(self):
        """Initialize enhanced legal backing system"""
        self.domain_legal_mappings = self._initialize_domain_mappings()
        self.constitutional_database = self._load_constitutional_articles()
        
    def _load_constitutional_articles(self) -> Dict[str, Dict]:
        """Load constitutional articles from database"""
        try:
            with open('article.json', 'r', encoding='utf-8') as f:
                articles = json.load(f)
            return {str(art.get('number', '')): art for art in articles if art.get('number')}
        except Exception as e:
            logger.error(f"Error loading constitutional articles: {e}")
            return {}
    
    def _initialize_domain_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive domain-to-legal-reference mappings"""
        return {
            'cyber_crime': {
                'constitutional_articles': [
                    ConstitutionalReference('21', 'Protection of life and personal liberty (Right to Privacy)', 
                                          'Privacy is fundamental right as per Puttaswamy judgment (2017)', True),
                    ConstitutionalReference('14', 'Equality before law', 
                                          'Ensures equal protection against cyber crimes', False),
                    ConstitutionalReference('300A', 'Right to property', 
                                          'Digital data and assets are protected property', False)
                ],
                'legal_acts': [
                    LegalActReference('Information Technology Act, 2000', 
                                    ['Section 43 - Unauthorized access', 
                                     'Section 66 - Hacking with criminal intent',
                                     'Section 66C - Identity theft',
                                     'Section 66D - Cheating by personation'],
                                    'Primary legislation for cyber crimes in India',
                                    'Directly applicable to hacking and unauthorized access'),
                    LegalActReference('Indian Penal Code, 1860',
                                    ['Section 379 - Theft', 
                                     'Section 420 - Cheating',
                                     'Section 468 - Forgery'],
                                    'General criminal law provisions',
                                    'Applicable when cyber crime involves fraud or theft')
                ],
                'primary_laws': ['IT Act 2000', 'IPC 1860']
            },
            
            'employment_law': {
                'constitutional_articles': [
                    ConstitutionalReference('19(1)(g)', 'Freedom to practice profession', 
                                          'Includes employment rights with confidentiality restrictions', True),
                    ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                          'Includes right to livelihood and privacy at workplace', False),
                    ConstitutionalReference('14', 'Equality before law', 
                                          'Ensures fair treatment in employment matters', False),
                    ConstitutionalReference('15', 'Prohibition of discrimination', 
                                          'Prevents workplace discrimination', False)
                ],
                'legal_acts': [
                    LegalActReference('Indian Contract Act, 1872',
                                    ['Section 27 - Restraint of trade',
                                     'Section 73 - Compensation for breach'],
                                    'Governs employment contracts and confidentiality agreements',
                                    'Primary law for employment contract disputes'),
                    LegalActReference('Industrial Disputes Act, 1947',
                                    ['Section 2A - Unfair labor practices',
                                     'Section 25F - Conditions for retrenchment'],
                                    'Governs industrial relations and employment disputes',
                                    'Applicable to wrongful termination and labor disputes'),
                    LegalActReference('Sexual Harassment of Women at Workplace Act, 2013',
                                    ['Section 4 - Duties of employer',
                                     'Section 9 - Complaint procedure'],
                                    'Specific law for workplace harassment',
                                    'Mandatory for sexual harassment cases')
                ],
                'primary_laws': ['Contract Act 1872', 'Industrial Disputes Act 1947', 'POSH Act 2013']
            },
            
            'tenant_rights': {
                'constitutional_articles': [
                    ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                          'Right to shelter as part of right to life', True),
                    ConstitutionalReference('300A', 'Right to property', 
                                          'Protects tenant rights and security deposits', True),
                    ConstitutionalReference('19(1)(e)', 'Freedom to reside and settle', 
                                          'Right to peaceful residence', False)
                ],
                'legal_acts': [
                    LegalActReference('State Rent Control Acts',
                                    ['Rent regulation provisions',
                                     'Eviction procedures',
                                     'Security deposit rules'],
                                    'State-specific tenant protection laws',
                                    'Primary legislation for tenant-landlord disputes'),
                    LegalActReference('Transfer of Property Act, 1882',
                                    ['Section 105 - Lease definition',
                                     'Section 108 - Rights of lessee'],
                                    'Governs property transfer and lease agreements',
                                    'Applicable to lease agreement disputes')
                ],
                'primary_laws': ['State Rent Control Acts', 'Transfer of Property Act 1882']
            },
            
            'consumer_complaint': {
                'constitutional_articles': [
                    ConstitutionalReference('19(1)(g)', 'Freedom to practice trade and business', 
                                          'Includes consumer protection in business transactions', True),
                    ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                          'Includes right to quality goods and services', False),
                    ConstitutionalReference('14', 'Equality before law', 
                                          'Equal protection for consumers', False)
                ],
                'legal_acts': [
                    LegalActReference('Consumer Protection Act, 2019',
                                    ['Section 2 - Consumer rights',
                                     'Section 35 - Complaint procedure',
                                     'Section 79 - Product liability'],
                                    'Primary consumer protection legislation',
                                    'Directly applicable to all consumer complaints'),
                    LegalActReference('Sale of Goods Act, 1930',
                                    ['Section 14 - Sale by description',
                                     'Section 16 - Warranty conditions'],
                                    'Governs sale transactions and warranties',
                                    'Applicable to defective product complaints')
                ],
                'primary_laws': ['Consumer Protection Act 2019', 'Sale of Goods Act 1930']
            },
            
            'family_law': {
                'constitutional_articles': [
                    ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                          'Includes right to live with dignity, free from violence', True),
                    ConstitutionalReference('14', 'Equality before law', 
                                          'Equal rights for all family members', True),
                    ConstitutionalReference('15', 'Prohibition of discrimination', 
                                          'Gender equality in family matters', False),
                    ConstitutionalReference('25', 'Freedom of religion', 
                                          'Personal law matters and religious practices', False)
                ],
                'legal_acts': [
                    LegalActReference('Hindu Marriage Act, 1955',
                                    ['Section 13 - Divorce grounds',
                                     'Section 24 - Maintenance'],
                                    'Governs Hindu marriages and divorce',
                                    'Applicable to Hindu marriage disputes'),
                    LegalActReference('Protection of Women from Domestic Violence Act, 2005',
                                    ['Section 12 - Protection orders',
                                     'Section 19 - Monetary relief'],
                                    'Protects women from domestic violence',
                                    'Primary law for domestic violence cases'),
                    LegalActReference('Guardians and Wards Act, 1890',
                                    ['Section 17 - Welfare of minor',
                                     'Section 25 - Guardianship orders'],
                                    'Governs child custody and guardianship',
                                    'Applicable to child custody disputes')
                ],
                'primary_laws': ['Hindu Marriage Act 1955', 'DV Act 2005', 'Guardians Act 1890']
            },
            
            'criminal_law': {
                'constitutional_articles': [
                    ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                          'Protection from criminal acts and right to fair trial', True),
                    ConstitutionalReference('20', 'Protection in respect of conviction for offences', 
                                          'Protection from ex post facto laws and double jeopardy', True),
                    ConstitutionalReference('22', 'Protection against arrest and detention', 
                                          'Rights during arrest and detention', True),
                    ConstitutionalReference('14', 'Equality before law', 
                                          'Equal protection under criminal law', False)
                ],
                'legal_acts': [
                    LegalActReference('Indian Penal Code, 1860',
                                    ['Section 375 - Rape',
                                     'Section 302 - Murder',
                                     'Section 379 - Theft',
                                     'Section 420 - Cheating'],
                                    'Primary criminal law of India',
                                    'Defines all major criminal offences'),
                    LegalActReference('Code of Criminal Procedure, 1973',
                                    ['Section 154 - FIR registration',
                                     'Section 161 - Police examination',
                                     'Section 437 - Bail provisions'],
                                    'Governs criminal procedure and investigation',
                                    'Applicable to all criminal proceedings')
                ],
                'primary_laws': ['Indian Penal Code 1860', 'CrPC 1973']
            },
            
            'immigration_law': {
                'constitutional_articles': [
                    ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                          'Right to life includes right to livelihood and residence', True),
                    ConstitutionalReference('14', 'Equality before law', 
                                          'Equal treatment in immigration matters', True),
                    ConstitutionalReference('5', 'Citizenship at the commencement of the Constitution', 
                                          'Defines citizenship criteria and rights', False),
                    ConstitutionalReference('6', 'Rights of citizenship of certain persons who have migrated to India from Pakistan', 
                                          'Migration and citizenship provisions', False)
                ],
                'legal_acts': [
                    LegalActReference('Passport Act, 1967',
                                    ['Section 3 - Passport authority',
                                     'Section 6 - Application for passport',
                                     'Section 12 - Refusal of passport'],
                                    'Primary law governing passports and travel documents',
                                    'Directly applicable to passport and visa matters'),
                    LegalActReference('Foreigners Act, 1946',
                                    ['Section 3 - Power to make orders',
                                     'Section 9 - Burden of proof',
                                     'Section 14 - Penalty for contravention'],
                                    'Governs entry, stay, and departure of foreigners in India',
                                    'Applicable to visa violations and foreign national issues'),
                    LegalActReference('Citizenship Act, 1955',
                                    ['Section 3 - Citizenship by birth',
                                     'Section 5 - Citizenship by registration',
                                     'Section 6 - Citizenship by naturalization'],
                                    'Defines acquisition and termination of Indian citizenship',
                                    'Applicable to citizenship and residency matters')
                ],
                'primary_laws': ['Passport Act 1967', 'Foreigners Act 1946', 'Citizenship Act 1955']
            }
        }
    
    def get_enhanced_legal_backing(self, domain: str, query: str) -> EnhancedLegalBacking:
        """Get comprehensive legal backing for a query"""
        
        # Normalize domain
        normalized_domain = self._normalize_domain(domain)
        
        # Get domain-specific mappings
        domain_mapping = self.domain_legal_mappings.get(normalized_domain, {})
        
        if not domain_mapping:
            # Fallback for unknown domains
            return self._get_fallback_backing(domain, query)
        
        # Extract components
        constitutional_articles = domain_mapping.get('constitutional_articles', [])
        legal_acts = domain_mapping.get('legal_acts', [])
        primary_laws = domain_mapping.get('primary_laws', [])
        
        # Filter articles based on query context
        relevant_articles = self._filter_articles_by_context(constitutional_articles, query)
        
        # Filter legal acts based on query context  
        relevant_acts = self._filter_acts_by_context(legal_acts, query)
        
        # Generate backing summary
        backing_summary = self._generate_backing_summary(
            relevant_articles, relevant_acts, primary_laws, normalized_domain
        )
        
        return EnhancedLegalBacking(
            constitutional_articles=relevant_articles,
            legal_acts=relevant_acts,
            primary_laws=primary_laws,
            domain=normalized_domain,
            backing_summary=backing_summary
        )
    
    def _normalize_domain(self, domain: str) -> str:
        """Normalize domain names to match mappings"""
        domain_lower = domain.lower().replace(' ', '_').replace('-', '_')
        
        # Handle common variations
        if 'cyber' in domain_lower or 'hack' in domain_lower:
            return 'cyber_crime'
        elif 'employment' in domain_lower or 'workplace' in domain_lower:
            return 'employment_law'
        elif 'tenant' in domain_lower or 'landlord' in domain_lower:
            return 'tenant_rights'  
        elif 'consumer' in domain_lower:
            return 'consumer_complaint'
        elif 'family' in domain_lower or 'divorce' in domain_lower:
            return 'family_law'
        elif 'criminal' in domain_lower:
            return 'criminal_law'
        else:
            return domain_lower
    
    def _filter_articles_by_context(self, articles: List[ConstitutionalReference], query: str) -> List[ConstitutionalReference]:
        """Filter constitutional articles based on query context"""
        query_lower = query.lower()
        
        # Always include primary articles
        relevant = [art for art in articles if art.is_primary]
        
        # Add context-specific articles
        context_filters = {
            'privacy': ['21', '19'],
            'harassment': ['21', '14', '15'],  
            'discrimination': ['14', '15', '16'],
            'property': ['300A', '21'],
            'arrest': ['20', '21', '22'],
            'business': ['19', '300A']
        }
        
        for context_word, article_nums in context_filters.items():
            if context_word in query_lower:
                for article in articles:
                    if article.article_number in article_nums and article not in relevant:
                        relevant.append(article)
        
        # Limit to top 4 most relevant articles
        return relevant[:4]
    
    def _filter_acts_by_context(self, acts: List[LegalActReference], query: str) -> List[LegalActReference]:
        """Filter legal acts based on query context"""
        # For now, return all acts for the domain (they're already domain-specific)
        # In production, this could be enhanced with more sophisticated filtering
        return acts
    
    def _generate_backing_summary(self, articles: List[ConstitutionalReference], 
                                 acts: List[LegalActReference], primary_laws: List[str], 
                                 domain: str) -> str:
        """Generate comprehensive backing summary"""
        
        summary_parts = []
        
        # Constitutional foundation
        if articles:
            primary_articles = [art for art in articles if art.is_primary]
            if primary_articles:
                primary_desc = ", ".join([f"Article {art.article_number}" for art in primary_articles])
                summary_parts.append(f"Constitutional foundation: {primary_desc}")
        
        # Legal framework
        if primary_laws:
            laws_desc = ", ".join(primary_laws)
            summary_parts.append(f"Primary legal framework: {laws_desc}")
        
        # Domain-specific guidance
        domain_guidance = {
            'cyber_crime': 'IT Act 2000 provides comprehensive framework for cyber offences with specific penalties.',
            'employment_law': 'Employment disputes governed by contract law and industrial relations legislation.',
            'tenant_rights': 'Tenant protection varies by state under respective Rent Control Acts.',
            'consumer_complaint': 'Consumer Protection Act 2019 provides three-tier dispute resolution mechanism.',
            'family_law': 'Family matters governed by personal laws and constitutional principles of equality.',
            'criminal_law': 'Criminal justice system ensures due process and constitutional safeguards.',
            'immigration_law': 'Immigration matters governed by Passport Act 1967, Foreigners Act 1946, and Citizenship Act 1955.'
        }
        
        if domain in domain_guidance:
            summary_parts.append(domain_guidance[domain])
        
        return ". ".join(summary_parts) + "."
    
    def _get_fallback_backing(self, domain: str, query: str) -> EnhancedLegalBacking:
        """Provide fallback legal backing for unknown domains"""
        
        # Basic constitutional articles applicable to most legal issues
        fallback_articles = [
            ConstitutionalReference('21', 'Protection of life and personal liberty', 
                                  'Fundamental right applicable to all legal matters', True),
            ConstitutionalReference('14', 'Equality before law', 
                                  'Ensures equal protection under law', False)
        ]
        
        # Basic legal framework
        fallback_acts = [
            LegalActReference('Code of Civil Procedure, 1908',
                            ['Section 9 - Courts to try civil suits',
                             'Section 26 - Institution of suits'],
                            'Governs civil legal proceedings',
                            'Applicable to civil legal matters')
        ]
        
        return EnhancedLegalBacking(
            constitutional_articles=fallback_articles,
            legal_acts=fallback_acts,
            primary_laws=['Civil Procedure Code 1908'],
            domain=domain,
            backing_summary='Constitutional rights ensure equal protection under law with civil procedure for legal remedies.'
        )
    
    def format_legal_backing_display(self, backing: EnhancedLegalBacking) -> str:
        """Format legal backing for display (without misleading confidence percentages)"""
        
        output_parts = []
        
        # Constitutional Articles Section
        output_parts.append("🏛️ CONSTITUTIONAL FOUNDATION:")
        for article in backing.constitutional_articles:
            priority = "PRIMARY" if article.is_primary else "SUPPORTING"
            output_parts.append(f"   • Article {article.article_number}: {article.title} ({priority})")
            output_parts.append(f"     Relevance: {article.relevance_reason}")
        
        # Legal Acts Section
        if backing.legal_acts:
            output_parts.append("\n⚖️ APPLICABLE LEGAL FRAMEWORK:")
            for act in backing.legal_acts:
                output_parts.append(f"   • {act.act_name}:")
                for section in act.sections:
                    output_parts.append(f"     - {section}")
                output_parts.append(f"     Relevance: {act.relevance_reason}")
        
        # Summary
        output_parts.append(f"\n📋 LEGAL BACKING SUMMARY:")
        output_parts.append(f"   {backing.backing_summary}")
        
        return "\n".join(output_parts)


def create_enhanced_legal_backing_system() -> EnhancedLegalBackingSystem:
    """Factory function to create enhanced legal backing system"""
    return EnhancedLegalBackingSystem()


# Example usage and testing
if __name__ == "__main__":
    system = create_enhanced_legal_backing_system()
    
    # Test with cyber crime query
    backing = system.get_enhanced_legal_backing("cyber_crime", "my phone is being hacked")
    print("=== CYBER CRIME LEGAL BACKING ===")
    print(system.format_legal_backing_display(backing))
    
    print("\n" + "="*60 + "\n")
    
    # Test with employment law query  
    backing = system.get_enhanced_legal_backing("employment_law", "employee disclosed company secrets")
    print("=== EMPLOYMENT LAW LEGAL BACKING ===")
    print(system.format_legal_backing_display(backing))