"""
Constitutional Articles Integration Module - Enhanced
=====================================================

This module integrates Indian Constitutional articles with the Legal Agent system
to provide constitutional backing for legal advice and enhance system credibility.

Features:
- Constitutional article search and retrieval
- Domain-specific constitutional references
- Enhanced legal backing with proper legal acts
- Production-grade legal references without misleading confidence percentages
- Proper constitutional articles based on legal context

Author: Legal Agent Team
Version: 5.0.0 - Enhanced Legal Backing
Date: 2025-08-28
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
from pathlib import Path

# Import enhanced legal backing system
try:
    from enhanced_legal_backing import create_enhanced_legal_backing_system, EnhancedLegalBacking
    ENHANCED_BACKING_AVAILABLE = True
except ImportError:
    ENHANCED_BACKING_AVAILABLE = False
    print("Enhanced legal backing not available, using basic system")

# Import existing constitutional matcher for fallback
try:
    from constitutional_article_matcher import get_constitutional_articles_with_confidence
    CONSTITUTIONAL_MATCHER_AVAILABLE = True
except ImportError:
    CONSTITUTIONAL_MATCHER_AVAILABLE = False
    print("Constitutional matcher not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConstitutionalArticle:
    """Data structure for constitutional articles"""
    article_number: str
    title: str
    content: str
    
    @property
    def clean_title(self) -> str:
        """Get cleaned title without quotes and extra formatting"""
        return self.title.strip('"').strip()
    
    @property
    def has_content(self) -> bool:
        """Check if article has substantial content"""
        return bool(self.content and self.content.strip())
    
    @property
    def summary(self) -> str:
        """Get a brief summary of the article"""
        if not self.has_content:
            return self.clean_title
        
        # Extract first sentence or first 100 characters
        content = self.content.strip()
        first_sentence = content.split('.')[0] if '.' in content else content
        
        if len(first_sentence) > 100:
            return first_sentence[:100] + "..."
        return first_sentence


class ConstitutionalDatabase:
    """Database of constitutional articles with search capabilities"""
    
    def __init__(self, articles_file: str = "article.json"):
        """Initialize with constitutional articles"""
        self.articles_file = articles_file
        self.articles: Dict[str, ConstitutionalArticle] = {}
        self.domain_mappings: Dict[str, List[str]] = {}
        self.load_articles()
        self.create_domain_mappings()
    
    def load_articles(self):
        """Load constitutional articles from JSON file"""
        try:
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            for article_data in articles_data:
                article = ConstitutionalArticle(
                    article_number=article_data['article_number'],
                    title=article_data['title'],
                    content=article_data.get('content', '')
                )
                self.articles[article.article_number] = article
            
            logger.info(f"Loaded {len(self.articles)} constitutional articles")
            
        except FileNotFoundError:
            logger.warning(f"Constitutional articles file {self.articles_file} not found")
            self.articles = {}
        except Exception as e:
            logger.error(f"Error loading constitutional articles: {e}")
            self.articles = {}
    
    def create_domain_mappings(self):
        """Create mappings between legal domains and relevant constitutional articles"""
        
        # Define domain-specific constitutional mappings
        self.domain_mappings = {
            'tenant rights': ['19', '21', '300'],  # Property rights, life & liberty
            'consumer complaint': ['19', '21'],     # Trade & commerce, consumer protection
            'family law': ['15', '16', '21', '25'], # Equality, marriage, personal liberty, religion
            'employment law': ['14', '15', '16', '19', '21', '23', '24'], # Equality, non-discrimination, work
            'contract dispute': ['19', '21', '300'], # Freedom of trade, liberty, property
            'personal injury': ['21'],              # Right to life and personal liberty
            'criminal law': ['14', '20', '21', '22'], # Equality, protection from crimes, liberty, arrest
            'immigration law': ['5', '6', '7', '8', '9', '10'], # Citizenship articles
            'elder abuse': ['21', '41'],            # Right to life, elderly care
            'cyber crime': ['19', '21'],            # Freedom of expression, privacy
            
            # Additional mappings for comprehensive coverage
            'fundamental_rights': ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '35'],
            'citizenship': ['5', '6', '7', '8', '9', '10', '11'],
            'union_territory': ['1', '2', '3', '4'],
            'constitutional_structure': ['1', '2', '3', '4']
        }
    
    def search_articles(self, query: str, limit: int = 5) -> List[ConstitutionalArticle]:
        """Search articles by content and title"""
        query_lower = query.lower()
        matches = []
        
        for article in self.articles.values():
            score = 0
            
            # Check title match
            if query_lower in article.clean_title.lower():
                score += 3
            
            # Check content match
            if article.has_content and query_lower in article.content.lower():
                score += 2
            
            # Check for keyword matches
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in article.clean_title.lower():
                    score += 1
                if article.has_content and keyword in article.content.lower():
                    score += 1
            
            if score > 0:
                matches.append((score, article))
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x[0], reverse=True)
        return [article for score, article in matches[:limit]]
    
    def get_articles_for_domain(self, domain: str) -> List[ConstitutionalArticle]:
        """Get relevant constitutional articles for a legal domain"""
        article_numbers = self.domain_mappings.get(domain, [])
        
        relevant_articles = []
        for article_num in article_numbers:
            if article_num in self.articles:
                relevant_articles.append(self.articles[article_num])
        
        return relevant_articles
    
    def get_article(self, article_number: str) -> Optional[ConstitutionalArticle]:
        """Get specific article by number"""
        return self.articles.get(article_number)
    
    def get_citizenship_articles(self) -> List[ConstitutionalArticle]:
        """Get all citizenship-related articles"""
        return self.get_articles_for_domain('citizenship')
    
    def get_fundamental_rights_articles(self) -> List[ConstitutionalArticle]:
        """Get fundamental rights articles"""
        return self.get_articles_for_domain('fundamental_rights')


class ConstitutionalAdvisor:
    """Provides enhanced constitutional backing for legal advice with proper legal acts"""
    
    def __init__(self, articles_file: str = "article.json"):
        """Initialize constitutional advisor with enhanced backing"""
        self.db = ConstitutionalDatabase(articles_file)
        
        # Initialize enhanced legal backing system if available
        if ENHANCED_BACKING_AVAILABLE:
            self.enhanced_backing = create_enhanced_legal_backing_system()
            self.use_enhanced = True
            logger.info("Enhanced legal backing system initialized")
        else:
            self.enhanced_backing = None
            self.use_enhanced = False
            logger.warning("Enhanced legal backing not available, using basic system")
    
    def get_constitutional_backing(self, domain: str, query: str) -> Dict[str, Any]:
        """Get enhanced constitutional backing with proper legal acts and constitutional articles"""
        
        if self.use_enhanced:
            return self._get_enhanced_backing(domain, query)
        else:
            return self._get_basic_backing(domain, query)
    
    def _get_enhanced_backing(self, domain: str, query: str) -> Dict[str, Any]:
        """Get enhanced legal backing with proper legal acts"""
        
        try:
            # Get comprehensive legal backing
            enhanced_backing = self.enhanced_backing.get_enhanced_legal_backing(domain, query)
            
            # Convert to expected format for compatibility
            articles_detailed = []
            for article in enhanced_backing.constitutional_articles:
                articles_detailed.append({
                    'article_number': article.article_number,
                    'title': article.title,
                    'content_summary': article.relevance_reason,
                    'is_primary': article.is_primary,
                    'relevance_type': 'PRIMARY' if article.is_primary else 'SUPPORTING'
                })
            
            # Format legal acts for display
            legal_acts_formatted = []
            for act in enhanced_backing.legal_acts:
                legal_acts_formatted.append({
                    'act_name': act.act_name,
                    'sections': act.sections,
                    'description': act.description,
                    'relevance_reason': act.relevance_reason
                })
            
            # Generate enhanced constitutional basis
            constitutional_basis = self._generate_enhanced_basis(
                enhanced_backing.constitutional_articles,
                enhanced_backing.legal_acts,
                enhanced_backing.primary_laws,
                domain
            )
            
            return {
                'relevant_articles': [],  # Keep for compatibility
                'articles': articles_detailed,
                'legal_acts': legal_acts_formatted,
                'primary_laws': enhanced_backing.primary_laws,
                'constitutional_basis': constitutional_basis,
                'article_count': len(articles_detailed),
                'domain': domain,
                'enhanced_backing': enhanced_backing,
                'backing_summary': enhanced_backing.backing_summary
            }
            
        except Exception as e:
            logger.error(f"Enhanced backing failed: {e}")
            return self._get_basic_backing(domain, query)
    
    def _get_basic_backing(self, domain: str, query: str) -> Dict[str, Any]:
        """Fallback to basic constitutional backing"""
        
        # Get specific constitutional articles based on query type
        specific_articles = self._get_specific_constitutional_articles(domain, query)

        # Get domain-specific articles as backup
        domain_articles = self.db.get_articles_for_domain(domain)

        # Search for query-specific articles
        query_articles = self.db.search_articles(query, limit=2)

        # Prioritize specific articles first, then add others only if needed
        unique_articles = {}

        # Add specific articles first (highest priority)
        for article in specific_articles:
            unique_articles[article.article_number] = article

        # Only add domain/query articles if we don't have enough specific ones
        if len(unique_articles) < 3:
            for article in domain_articles + query_articles:
                if article.article_number not in unique_articles:
                    unique_articles[article.article_number] = article
                if len(unique_articles) >= 5:
                    break

        relevant_articles = list(unique_articles.values())[:5]  # Limit to top 5

        # Build articles without misleading confidence percentages
        articles_detailed = []
        for article in relevant_articles[:3]:
            articles_detailed.append({
                'article_number': article.article_number,
                'title': article.clean_title,
                'content_summary': article.summary or 'Constitutional article',
                'relevance_type': 'RELEVANT'
            })

        # Generate base constitutional basis text (domain/context specific)
        base_text = self._generate_constitutional_basis(relevant_articles, domain, query)

        return {
            'relevant_articles': relevant_articles,
            'articles': articles_detailed,
            'constitutional_basis': base_text.strip(),
            'article_count': len(relevant_articles),
            'domain': domain,
            'specific_articles': [f"Article {art.article_number}" for art in specific_articles[:3]]
        }
    
    def _generate_enhanced_basis(self, articles, legal_acts, primary_laws, domain) -> str:
        """Generate enhanced constitutional basis with legal acts"""
        
        parts = []
        
        # Constitutional foundation
        if articles:
            primary_articles = [art for art in articles if art.is_primary]
            if primary_articles:
                primary_nums = [f"Article {art.article_number}" for art in primary_articles]
                parts.append(f"Constitutional foundation: {', '.join(primary_nums)} provide fundamental rights protection.")
        
        # Legal framework
        if primary_laws:
            parts.append(f"Primary legal framework: {', '.join(primary_laws)} govern this matter.")
        
        # Specific legal provisions
        if legal_acts:
            act_names = [act.act_name for act in legal_acts]
            parts.append(f"Specific provisions under {', '.join(act_names[:2])} apply directly.")
        
        # Domain-specific guidance
        domain_guidance = {
            'cyber_crime': 'IT Act 2000 provides comprehensive framework for cyber offences.',
            'employment_law': 'Employment matters governed by contract law and labor legislation.',
            'tenant_rights': 'Tenant protection under state Rent Control Acts.',
            'consumer_complaint': 'Consumer Protection Act 2019 provides dispute resolution.',
            'family_law': 'Family matters under personal laws and constitutional equality.',
            'criminal_law': 'Criminal justice ensures due process and constitutional safeguards.'
        }
        
        if domain.lower() in domain_guidance:
            parts.append(domain_guidance[domain.lower()])
        
        return ' '.join(parts)

    def _get_specific_constitutional_articles(self, domain: str, query: str) -> List[ConstitutionalArticle]:
        """Get specific constitutional articles based on query subcategory"""

        query_lower = query.lower()
        specific_mappings = {
            # Employment Law specific mappings
            'workplace_harassment': ['Article 14', 'Article 15', 'Article 19', 'Article 21'],  # Equality, non-discrimination, profession, life & dignity
            'sexual_harassment': ['Article 14', 'Article 15', 'Article 19', 'Article 21'],
            'wrongful_termination': ['Article 19', 'Article 21', 'Article 14'],  # Right to profession, life, equality
            'salary_issues': ['Article 23', 'Article 24', 'Article 21'],  # Against exploitation, child labor, life
            'discrimination': ['Article 14', 'Article 15', 'Article 16'],  # Equality provisions

            # Criminal Law specific mappings
            'sexual_assault': ['Article 21', 'Article 14', 'Article 15'],  # Life & dignity, equality
            'theft_robbery': ['Article 21', 'Article 300A'],  # Life, property rights
            'fraud': ['Article 21', 'Article 300A', 'Article 14'],  # Life, property, equality
            'murder': ['Article 21'],  # Right to life

            # Family Law specific mappings
            'domestic_violence': ['Article 21', 'Article 14', 'Article 15'],  # Life, equality, gender equality
            'divorce': ['Article 25', 'Article 21', 'Article 14'],  # Personal law, life, equality
            'child_custody': ['Article 21', 'Article 14', 'Article 15'],  # Child welfare, equality

            # Tenant Rights specific mappings
            'deposit_issues': ['Article 300A', 'Article 21', 'Article 14'],  # Property rights, life, equality
            'eviction': ['Article 21', 'Article 19', 'Article 300A'],  # Shelter, movement, property
            'maintenance': ['Article 21', 'Article 300A'],  # Life, property

            # Cyber Crime specific mappings
            'online_fraud': ['Article 19', 'Article 21', 'Article 300A'],  # Expression, privacy, property
            'hacking': ['Article 19', 'Article 21', 'Article 300A'],  # Communication, privacy, digital property
            'cyberbullying': ['Article 19', 'Article 21', 'Article 300A'],  # Expression, dignity, digital property
        }

        # Find matching articles with better keyword matching
        relevant_article_numbers = []

        # Check for specific harassment patterns first
        if any(word in query_lower for word in ['sexually harassing', 'sexual harassment', 'harassing', 'harassment']):
            if any(word in query_lower for word in ['work', 'office', 'workplace', 'coworker', 'colleague', 'boss']):
                relevant_article_numbers.extend(specific_mappings['workplace_harassment'])
            else:
                relevant_article_numbers.extend(specific_mappings['sexual_harassment'])
        else:
            # General pattern matching
            for key, articles in specific_mappings.items():
                if any(keyword in query_lower for keyword in key.split('_')):
                    relevant_article_numbers.extend(articles)
                    break

        # If no specific match, use domain defaults
        if not relevant_article_numbers:
            domain_defaults = {
                'employment_law': ['Article 14', 'Article 19', 'Article 21'],
                'criminal_law': ['Article 21', 'Article 14', 'Article 20'],
                'family_law': ['Article 21', 'Article 25', 'Article 14'],
                'tenant_rights': ['Article 300A', 'Article 21', 'Article 19'],
                'cyber_crime': ['Article 19', 'Article 21', 'Article 300A'],
                'consumer_complaint': ['Article 21', 'Article 14', 'Article 19']
            }
            relevant_article_numbers = domain_defaults.get(domain, ['Article 21', 'Article 14'])

        # Get actual article objects
        specific_articles = []
        for article_num in relevant_article_numbers[:3]:  # Limit to top 3
            article_obj = self.db.get_article(article_num.replace('Article ', ''))
            if article_obj:
                specific_articles.append(article_obj)

        return specific_articles

    def _generate_workplace_harassment_constitutional_basis(self) -> str:
        """Generate comprehensive constitutional basis specifically for workplace harassment"""

        constitutional_framework = []

        # Core constitutional rights
        constitutional_framework.append("🏛️ CONSTITUTIONAL FRAMEWORK FOR WORKPLACE HARASSMENT:")
        constitutional_framework.append("")

        # Article 14 - Right to Equality
        constitutional_framework.append("📋 Article 14 - Right to Equality:")
        constitutional_framework.append("   • Ensures equal treatment regardless of gender in workplace")
        constitutional_framework.append("   • Prohibits discriminatory treatment based on sex")
        constitutional_framework.append("   • Guarantees equal protection under law for harassment victims")
        constitutional_framework.append("")

        # Article 15 - Prohibition of discrimination
        constitutional_framework.append("📋 Article 15 - Prohibition of Discrimination:")
        constitutional_framework.append("   • Specifically prohibits discrimination on grounds of sex")
        constitutional_framework.append("   • Covers workplace discrimination and harassment")
        constitutional_framework.append("   • Empowers state to make special provisions for women's safety")
        constitutional_framework.append("")

        # Article 19(1)(g) - Right to profession
        constitutional_framework.append("📋 Article 19(1)(g) - Right to Practice Profession:")
        constitutional_framework.append("   • Guarantees right to work in harassment-free environment")
        constitutional_framework.append("   • Protects against interference with professional activities")
        constitutional_framework.append("   • Ensures workplace safety as fundamental right")
        constitutional_framework.append("")

        # Article 21 - Right to life and dignity
        constitutional_framework.append("📋 Article 21 - Right to Life and Personal Dignity:")
        constitutional_framework.append("   • Protects personal dignity and honor from harassment")
        constitutional_framework.append("   • Covers psychological harm and mental trauma")
        constitutional_framework.append("   • Ensures right to live with dignity at workplace")
        constitutional_framework.append("")

        # Article 51A(e) - Fundamental Duties
        constitutional_framework.append("📋 Article 51A(e) - Fundamental Duties:")
        constitutional_framework.append("   • Duty to promote harmony and dignity of women")
        constitutional_framework.append("   • Obligation to renounce practices derogatory to women")
        constitutional_framework.append("   • Creates societal responsibility to prevent harassment")
        constitutional_framework.append("")

        # Legal framework
        constitutional_framework.append("⚖️ SUPPORTING LEGAL FRAMEWORK:")
        constitutional_framework.append("   • Prevention of Sexual Harassment (POSH) Act, 2013")
        constitutional_framework.append("   • Vishaka Guidelines (1997) - Supreme Court landmark judgment")
        constitutional_framework.append("   • Indian Penal Code Sections 354, 354A, 354B, 354C, 354D")
        constitutional_framework.append("   • Labour laws ensuring safe working conditions")
        constitutional_framework.append("")

        # Enforcement mechanisms
        constitutional_framework.append("🛡️ CONSTITUTIONAL ENFORCEMENT:")
        constitutional_framework.append("   • Right to approach High Court under Article 226 (Writ Jurisdiction)")
        constitutional_framework.append("   • Right to approach Supreme Court under Article 32 (Right to Constitutional Remedies)")
        constitutional_framework.append("   • Mandatory Internal Complaints Committee (ICC) under POSH Act")
        constitutional_framework.append("   • State obligation to ensure effective implementation")

        return "\\n".join(constitutional_framework)

    def _generate_domestic_violence_constitutional_basis(self) -> str:
        """Generate constitutional basis for domestic violence cases"""

        framework = [
            "🏛️ CONSTITUTIONAL FRAMEWORK FOR DOMESTIC VIOLENCE:",
            "",
            "📋 Article 21 - Right to Life and Personal Dignity:",
            "   • Fundamental right to live without violence and abuse",
            "   • Protection from physical and mental torture",
            "   • Right to safe and secure living environment",
            "",
            "📋 Article 14 - Right to Equality:",
            "   • Equal protection under law regardless of gender",
            "   • Non-discriminatory access to justice and remedies",
            "",
            "📋 Article 15 - Prohibition of Discrimination:",
            "   • Special protection for women against gender-based violence",
            "   • State obligation to prevent discrimination",
            "",
            "⚖️ SUPPORTING LEGAL FRAMEWORK:",
            "   • Protection of Women from Domestic Violence Act, 2005",
            "   • Indian Penal Code Sections 498A, 323, 324, 506",
            "   • Criminal Procedure Code provisions for immediate relief"
        ]
        return "\\n".join(framework)

    def _generate_property_rights_constitutional_basis(self) -> str:
        """Generate constitutional basis for property/tenant rights"""

        framework = [
            "🏛️ CONSTITUTIONAL FRAMEWORK FOR PROPERTY RIGHTS:",
            "",
            "📋 Article 300A - Right to Property:",
            "   • No person shall be deprived of property save by authority of law",
            "   • Protection against arbitrary seizure of security deposits",
            "   • Legal procedure required for any property deprivation",
            "",
            "📋 Article 21 - Right to Life:",
            "   • Right to shelter as part of right to life",
            "   • Protection against illegal eviction",
            "   • Dignified living conditions",
            "",
            "📋 Article 19(1)(e) - Right to Reside:",
            "   • Freedom to reside and settle in any part of India",
            "   • Protection against forced displacement",
            "",
            "⚖️ SUPPORTING LEGAL FRAMEWORK:",
            "   • Rent Control Acts (State-specific)",
            "   • Transfer of Property Act, 1882",
            "   • Consumer Protection Act, 2019"
        ]
        return "\\n".join(framework)

    def _generate_employment_rights_constitutional_basis(self) -> str:
        """Generate constitutional basis for employment rights"""

        framework = [
            "🏛️ CONSTITUTIONAL FRAMEWORK FOR EMPLOYMENT RIGHTS:",
            "",
            "📋 Article 19(1)(g) - Right to Practice Profession:",
            "   • Fundamental right to carry on any occupation or trade",
            "   • Protection against arbitrary termination",
            "   • Right to fair working conditions",
            "",
            "📋 Article 23 - Prohibition of Forced Labour:",
            "   • Protection against exploitation and unpaid work",
            "   • Right to fair wages for work done",
            "",
            "📋 Article 14 - Right to Equality:",
            "   • Equal pay for equal work",
            "   • Non-discriminatory employment practices",
            "",
            "⚖️ SUPPORTING LEGAL FRAMEWORK:",
            "   • Industrial Disputes Act, 1947",
            "   • Minimum Wages Act, 1948",
            "   • Payment of Wages Act, 1936",
            "   • Labour Laws (various state and central acts)"
        ]
        return "\\n".join(framework)

    def _generate_criminal_law_constitutional_basis(self) -> str:
        """Generate constitutional basis for criminal law matters"""

        framework = [
            "🏛️ CONSTITUTIONAL FRAMEWORK FOR CRIMINAL MATTERS:",
            "",
            "📋 Article 21 - Right to Life and Personal Liberty:",
            "   • Protection from harm to life and property",
            "   • Right to security and safety",
            "   • Due process in criminal proceedings",
            "",
            "📋 Article 20 - Protection in Respect of Conviction:",
            "   • Protection against double jeopardy",
            "   • Right against self-incrimination",
            "   • Ex-post facto law protection",
            "",
            "📋 Article 22 - Protection Against Arrest:",
            "   • Right to be informed of grounds of arrest",
            "   • Right to legal representation",
            "   • Protection against arbitrary detention",
            "",
            "⚖️ SUPPORTING LEGAL FRAMEWORK:",
            "   • Indian Penal Code, 1860",
            "   • Criminal Procedure Code, 1973",
            "   • Indian Evidence Act, 1872"
        ]
        return "\\n".join(framework)

    def _generate_constitutional_basis(self, articles: List[ConstitutionalArticle], domain: str, query: str = "") -> str:
        """Generate constitutional basis text for legal advice"""

        if not articles:
            return "Constitutional provisions may apply to this matter. Consult legal expert for specific constitutional references."

        # Debug: Print what articles we're getting from our enhanced matcher
        # print(f"DEBUG: Articles received: {[f'Article {a.article_number}' for a in articles]}")

        # Provide specific constitutional frameworks for different query types
        query_lower = query.lower()

        # Workplace harassment
        if any(word in query_lower for word in ['harassment', 'harassing', 'sexually harassing']):
            if any(word in query_lower for word in ['work', 'workplace', 'coworker', 'colleague', 'office']):
                return self._generate_workplace_harassment_constitutional_basis()

        # Domestic violence
        if any(word in query_lower for word in ['domestic violence', 'wife beating', 'husband abuse', 'beating me']):
            return self._generate_domestic_violence_constitutional_basis()

        # Property/tenant rights
        if any(word in query_lower for word in ['landlord', 'deposit', 'rent', 'eviction', 'tenant']):
            return self._generate_property_rights_constitutional_basis()

        # Employment issues
        if any(word in query_lower for word in ['fired', 'terminated', 'salary', 'wages', 'overtime']):
            return self._generate_employment_rights_constitutional_basis()

        # Criminal matters
        if any(word in query_lower for word in ['stolen', 'theft', 'robbery', 'fraud', 'cheated']):
            return self._generate_criminal_law_constitutional_basis()

        basis_parts = []

        # Add domain-specific constitutional context
        domain_contexts = {
            'criminal law': "Under the Constitution, you have fundamental rights including protection from arbitrary arrest and fair trial guarantees.",
            'employment law': "The Constitution guarantees equality and prohibits discrimination in employment matters.",
            'family law': "Constitutional provisions protect personal liberty and family rights while ensuring gender equality.",
            'immigration law': "Constitutional citizenship provisions define rights and procedures for Indian citizenship.",
            'elder abuse': "The Constitution's right to life and dignity extends special protection to vulnerable populations including elderly citizens.",
            'cyber crime': "Constitutional rights to privacy and freedom of expression apply to digital spaces and cyber crimes."
        }

        if domain in domain_contexts:
            basis_parts.append(domain_contexts[domain])

        # Add specific article references
        if len(articles) <= 2:
            for article in articles:
                if article.has_content:
                    basis_parts.append(f"Article {article.article_number}: {article.summary}")
                else:
                    basis_parts.append(f"Article {article.article_number}: {article.clean_title}")
        # Note: Removed the line that says "Relevant constitutional provisions include..." as per user request
        
        return " ".join(basis_parts)
    
    def get_article_details(self, article_number: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific article"""
        article = self.db.get_article(article_number)
        
        if not article:
            return None
        
        return {
            'article_number': article.article_number,
            'title': article.clean_title,
            'content': article.content,
            'summary': article.summary,
            'has_content': article.has_content
        }
    
    def search_constitutional_provisions(self, query: str) -> List[Dict[str, Any]]:
        """Search constitutional provisions by query"""
        articles = self.db.search_articles(query)
        
        return [
            {
                'article_number': article.article_number,
                'title': article.clean_title,
                'summary': article.summary,
                'relevance': 'high' if query.lower() in article.clean_title.lower() else 'medium'
            }
            for article in articles
        ]


def create_constitutional_advisor(articles_file: str = "article.json") -> ConstitutionalAdvisor:
    """Factory function to create constitutional advisor"""
    return ConstitutionalAdvisor(articles_file)


# Test the constitutional integration
if __name__ == "__main__":
    print("🏛️ CONSTITUTIONAL INTEGRATION TEST")
    print("=" * 50)
    
    advisor = create_constitutional_advisor()
    
    # Test domain-specific constitutional backing
    test_cases = [
        ("criminal law", "I was arrested without warrant"),
        ("employment law", "I'm facing workplace discrimination"),
        ("immigration law", "I need help with citizenship application"),
        ("elder abuse", "My elderly father is being mistreated"),
        ("cyber crime", "My privacy was violated online")
    ]
    
    for domain, query in test_cases:
        print(f"\n📋 Domain: {domain.title()}")
        print(f"Query: \"{query}\"")
        print("-" * 40)
        
        backing = advisor.get_constitutional_backing(domain, query)
        
        print(f"Constitutional Articles Found: {backing['article_count']}")
        print(f"Constitutional Basis: {backing['constitutional_basis'][:150]}...")
        
        if backing['relevant_articles']:
            print("Relevant Articles:")
            for article in backing['relevant_articles'][:2]:
                print(f"  • Article {article.article_number}: {article.clean_title[:60]}...")
    
    # Test article search
    print(f"\n🔍 Testing Article Search:")
    print("-" * 30)
    
    search_results = advisor.search_constitutional_provisions("citizenship")
    print(f"Search for 'citizenship' found {len(search_results)} articles:")
    for result in search_results[:3]:
        print(f"  • Article {result['article_number']}: {result['title'][:50]}...")
    
    print(f"\n✅ Constitutional integration ready for Legal Agent!")
    print(f"📊 Database contains {len(advisor.db.articles)} constitutional articles")
    print(f"🎯 Supports {len(advisor.db.domain_mappings)} legal domains")
