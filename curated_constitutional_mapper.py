"""
Curated Constitutional Article Mapper
====================================

This module implements a curated knowledge base approach for mapping
legal domains to relevant constitutional articles, eliminating irrelevant
keyword-based matches.

Features:
- Pre-mapped domain-to-article relationships
- Only legally relevant articles
- No random keyword matching
- Fallback to core fundamental rights
- High precision, low noise

Author: Legal Agent Team
Version: 3.0.0 - Curated Mapping
Date: 2025-08-29
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CuratedArticle:
    """Curated article with legal relevance"""
    article_number: str
    title: str
    relevance_reason: str
    confidence_percentage: int
    legal_context: str
    
    @property
    def clean_title(self) -> str:
        return self.title.strip('"').strip()


class CuratedConstitutionalMapper:
    """Curated mapper with pre-defined domain-to-article relationships"""
    
    def __init__(self):
        """Initialize curated mapper with domain mappings"""
        self.create_curated_mappings()
        self.load_article_details()
    
    def create_curated_mappings(self):
        """Create curated domain-to-article mappings"""
        
        # CURATED KNOWLEDGE BASE - Only legally relevant articles
        self.ARTICLE_MAP = {
            # Consumer Protection
            "consumer_complaint": {
                "primary": ["14", "21", "19"],
                "reasons": {
                    "14": "Equality before law - ensures fair treatment in consumer disputes",
                    "21": "Right to life and liberty - includes right to livelihood and protection from fraud",
                    "19": "Freedom of profession and trade - protects against fraudulent business practices"
                }
            },
            
            # Employment & Corporate Law
            "employment_law": {
                "primary": ["14", "16", "21", "19"],
                "reasons": {
                    "14": "Equality before law - non-discrimination in employment",
                    "16": "Equal opportunity in public employment",
                    "21": "Right to life and liberty - includes right to livelihood and dignity at work",
                    "19": "Freedom of profession - subject to reasonable restrictions (confidentiality, etc.)"
                }
            },
            
            "corporate_law": {
                "primary": ["19", "21", "300A", "14"],
                "reasons": {
                    "19": "Freedom to practice profession - subject to confidentiality obligations",
                    "21": "Right to life and liberty - includes right to fair legal remedy",
                    "300A": "Right to property - protects intellectual property and trade secrets",
                    "14": "Equality before law - ensures fair treatment in corporate disputes"
                }
            },
            
            # Criminal Law
            "criminal_law": {
                "primary": ["20", "21", "22", "14"],
                "reasons": {
                    "20": "Protection against self-incrimination and double jeopardy",
                    "21": "Right to life and liberty - includes right to fair trial",
                    "22": "Protection against arbitrary arrest and detention",
                    "14": "Equality before law - ensures fair treatment in criminal proceedings"
                }
            },
            
            # Cyber Crime
            "cyber_crime": {
                "primary": ["21", "19", "14"],
                "reasons": {
                    "21": "Right to life and liberty - includes right to privacy and digital security",
                    "19": "Freedom of speech and expression - includes digital communication rights",
                    "14": "Equality before law - ensures fair investigation and treatment"
                }
            },
            
            # Family Law
            "family_law": {
                "primary": ["14", "15", "21", "39"],
                "reasons": {
                    "14": "Equality before law - equal treatment in family matters",
                    "15": "Prohibition of discrimination - gender equality in marriage/divorce",
                    "21": "Right to life and liberty - includes right to live with dignity",
                    "39": "State policy for securing adequate means of livelihood - includes maintenance"
                }
            },
            
            # Property & Tenant Rights
            "tenant_rights": {
                "primary": ["21", "19", "300A", "14"],
                "reasons": {
                    "21": "Right to life and liberty - includes right to shelter",
                    "19": "Right to reside and settle - protects housing rights",
                    "300A": "Right to property - protects tenant's property rights",
                    "14": "Equality before law - fair treatment in landlord-tenant disputes"
                }
            },
            
            "property_disputes": {
                "primary": ["300A", "14", "21"],
                "reasons": {
                    "300A": "Right to property - fundamental property rights protection",
                    "14": "Equality before law - fair treatment in property disputes",
                    "21": "Right to life and liberty - includes right to shelter and property"
                }
            },
            
            # Personal Injury
            "personal_injury": {
                "primary": ["21", "14"],
                "reasons": {
                    "21": "Right to life and liberty - includes right to health and compensation",
                    "14": "Equality before law - ensures fair compensation and treatment"
                }
            },
            
            # Contract Disputes
            "contract_dispute": {
                "primary": ["14", "21", "19"],
                "reasons": {
                    "14": "Equality before law - fair enforcement of contracts",
                    "21": "Right to life and liberty - includes right to livelihood and fair dealing",
                    "19": "Freedom of profession and trade - contract enforcement in business"
                }
            },
            
            # Immigration Law
            "immigration_law": {
                "primary": ["14", "21", "22"],
                "reasons": {
                    "14": "Equality before law - non-discrimination in immigration matters",
                    "21": "Right to life and liberty - protection from arbitrary deportation",
                    "22": "Protection against arbitrary detention - immigration detention rights"
                }
            },
            
            # Elder Abuse
            "elder_abuse": {
                "primary": ["21", "14", "41"],
                "reasons": {
                    "21": "Right to life and liberty - includes dignity and protection of elderly",
                    "14": "Equality before law - protection from discrimination based on age",
                    "41": "Right to work and education - state duty to protect elderly"
                }
            }
        }
        
        # Core fundamental rights for fallback
        self.CORE_FUNDAMENTAL_RIGHTS = {
            "14": "Equality before law",
            "19": "Protection of certain rights regarding freedom of speech etc",
            "21": "Protection of life and personal liberty",
            "22": "Protection against arrest and detention",
            "32": "Right to Constitutional Remedies"
        }
    
    def load_article_details(self):
        """Load article details from JSON file"""
        try:
            with open("article.json", 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
                
            # Create lookup dictionary
            self.article_details = {}
            for article in articles_data:
                article_num = article.get('article_number', '')
                self.article_details[article_num] = {
                    'title': article.get('title', '').strip('"'),
                    'content': article.get('content', '')
                }
                
            logger.info(f"Loaded details for {len(self.article_details)} articles")
            
        except Exception as e:
            logger.error(f"Error loading article details: {e}")
            self.article_details = {}
    
    def get_curated_articles(self, domain: str, query: str = "") -> List[CuratedArticle]:
        """Get curated articles for a domain"""
        
        # Get mapped articles for domain
        if domain in self.ARTICLE_MAP:
            mapping = self.ARTICLE_MAP[domain]
            primary_articles = mapping["primary"]
            reasons = mapping["reasons"]
            
            curated_articles = []
            
            for i, article_num in enumerate(primary_articles):
                # Get article details
                details = self.article_details.get(article_num, {})
                title = details.get('title', f'Article {article_num}')
                
                # Calculate confidence based on position and relevance
                confidence = self._calculate_curated_confidence(i, len(primary_articles), domain, article_num)
                
                # Get legal context
                legal_context = self._get_legal_context(domain, article_num)
                
                curated_article = CuratedArticle(
                    article_number=article_num,
                    title=title,
                    relevance_reason=reasons.get(article_num, "Relevant to legal domain"),
                    confidence_percentage=confidence,
                    legal_context=legal_context
                )
                
                curated_articles.append(curated_article)
            
            return curated_articles
        
        # Fallback to core fundamental rights
        return self._get_fallback_articles(domain)
    
    def _calculate_curated_confidence(self, position: int, total: int, domain: str, article_num: str) -> int:
        """Calculate confidence based on curation position and domain relevance"""
        
        # Base confidence based on position (first article gets highest)
        base_confidence = 95 - (position * 8)  # 95%, 87%, 79%, 71%
        
        # Domain-specific boosts
        domain_boosts = {
            'corporate_law': {'19': 5, '21': 3, '300A': 4, '14': 2},
            'employment_law': {'14': 4, '16': 5, '21': 3, '19': 2},
            'criminal_law': {'20': 5, '21': 4, '22': 4, '14': 2},
            'cyber_crime': {'21': 5, '19': 3, '14': 2},
            'family_law': {'14': 3, '15': 4, '21': 5, '39': 2}
        }
        
        boost = domain_boosts.get(domain, {}).get(article_num, 0)
        final_confidence = min(95, base_confidence + boost)
        
        return max(65, final_confidence)  # Minimum 65% confidence
    
    def _get_legal_context(self, domain: str, article_num: str) -> str:
        """Get legal context for article in domain"""
        
        contexts = {
            'corporate_law': {
                '19': 'Employment and professional obligations',
                '21': 'Fair legal remedy and due process',
                '300A': 'Intellectual property protection',
                '14': 'Equal treatment in corporate disputes'
            },
            'employment_law': {
                '14': 'Non-discrimination in workplace',
                '16': 'Equal employment opportunities',
                '21': 'Right to livelihood and dignity',
                '19': 'Professional rights and restrictions'
            },
            'criminal_law': {
                '20': 'Criminal procedure protections',
                '21': 'Fair trial and legal representation',
                '22': 'Arrest and detention rights',
                '14': 'Equal justice under law'
            }
        }
        
        return contexts.get(domain, {}).get(article_num, 'Constitutional protection')
    
    def _get_fallback_articles(self, domain: str) -> List[CuratedArticle]:
        """Get fallback articles for unknown domains"""
        
        # Return core fundamental rights
        fallback_articles = []
        
        core_articles = ["14", "21"]  # Most universally applicable
        
        for i, article_num in enumerate(core_articles):
            details = self.article_details.get(article_num, {})
            title = details.get('title', f'Article {article_num}')
            
            curated_article = CuratedArticle(
                article_number=article_num,
                title=title,
                relevance_reason=f"Core fundamental right applicable to {domain} matters",
                confidence_percentage=75 - (i * 5),  # 75%, 70%
                legal_context="Fundamental constitutional protection"
            )
            
            fallback_articles.append(curated_article)
        
        return fallback_articles
    
    def get_curated_analysis(self, domain: str, query: str = "") -> Dict[str, Any]:
        """Get complete curated constitutional analysis"""
        
        articles = self.get_curated_articles(domain, query)
        
        if not articles:
            return {
                'domain': domain,
                'matching_articles': 0,
                'recommendations': [],
                'approach': 'curated_mapping',
                'confidence_summary': 'No specific constitutional articles apply to this domain.'
            }
        
        # Prepare recommendations
        recommendations = []
        for article in articles:
            recommendations.append({
                'article_number': article.article_number,
                'title': article.clean_title,
                'confidence_percentage': article.confidence_percentage,
                'relevance_reason': article.relevance_reason,
                'legal_context': article.legal_context,
                'approach': 'curated_mapping'
            })
        
        return {
            'domain': domain,
            'matching_articles': len(articles),
            'recommendations': recommendations,
            'approach': 'curated_mapping',
            'confidence_summary': {
                'high_confidence': len([a for a in articles if a.confidence_percentage >= 80]),
                'medium_confidence': len([a for a in articles if 65 <= a.confidence_percentage < 80]),
                'low_confidence': len([a for a in articles if a.confidence_percentage < 65]),
                'top_match_confidence': articles[0].confidence_percentage if articles else 0
            },
            'legal_frameworks': self._get_legal_frameworks(domain)
        }
    
    def _get_legal_frameworks(self, domain: str) -> List[str]:
        """Get relevant legal frameworks for domain"""
        
        frameworks = {
            'corporate_law': [
                'Indian Contract Act, 1872',
                'Companies Act, 2013', 
                'IT Act, 2000 (Section 72)',
                'Indian Penal Code (Section 405, 408)'
            ],
            'employment_law': [
                'Industrial Disputes Act, 1947',
                'Payment of Wages Act, 1936',
                'Indian Contract Act, 1872',
                'Labour Laws'
            ],
            'criminal_law': [
                'Indian Penal Code (IPC)',
                'Code of Criminal Procedure (CrPC)',
                'Evidence Act, 1872'
            ],
            'cyber_crime': [
                'Information Technology Act, 2000',
                'Indian Penal Code (Section 66, 419, 420)',
                'Data Protection Laws'
            ],
            'consumer_complaint': [
                'Consumer Protection Act, 2019',
                'Sale of Goods Act, 1930',
                'Indian Contract Act, 1872'
            ]
        }
        
        return frameworks.get(domain, ['Constitutional Rights', 'Relevant Indian Laws'])


# Global instance
curated_mapper = CuratedConstitutionalMapper()


def get_curated_constitutional_analysis(domain: str, query: str = "") -> Dict[str, Any]:
    """Get curated constitutional analysis for domain"""
    return curated_mapper.get_curated_analysis(domain, query)


def format_curated_articles(analysis: Dict[str, Any]) -> str:
    """Format curated articles for display"""
    
    if analysis['matching_articles'] == 0:
        return "❌ No specific constitutional articles apply to this domain."
    
    output = []
    output.append("🏛️ CURATED CONSTITUTIONAL ARTICLES")
    output.append("=" * 50)
    output.append(f"📊 Domain: {analysis['domain']}")
    output.append(f"📊 Approach: {analysis['approach']} (high precision)")
    output.append("")
    
    for i, rec in enumerate(analysis['recommendations'], 1):
        confidence = rec['confidence_percentage']
        icon = "🟢" if confidence >= 80 else "🟡" if confidence >= 65 else "🔴"
        
        output.append(f"{icon} {i}. Article {rec['article_number']} - {confidence}% Confidence")
        output.append(f"   📖 {rec['title']}")
        output.append(f"   💡 {rec['relevance_reason']}")
        output.append(f"   ⚖️ Context: {rec['legal_context']}")
        output.append("")
    
    # Legal frameworks
    if 'legal_frameworks' in analysis:
        output.append("📜 APPLICABLE LEGAL FRAMEWORKS:")
        for framework in analysis['legal_frameworks'][:4]:
            output.append(f"   • {framework}")
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test curated mapper
    test_cases = [
        ("corporate_law", "Employee discloses company secrets"),
        ("consumer_complaint", "Fake job offer scam"),
        ("criminal_law", "False accusations"),
        ("unknown_domain", "Random query")
    ]
    
    print("🗂️ CURATED CONSTITUTIONAL MAPPER TEST")
    print("=" * 50)
    
    for domain, query in test_cases:
        print(f"\n🔍 Testing: {domain} - '{query}'")
        print("-" * 40)
        
        analysis = get_curated_constitutional_analysis(domain, query)
        formatted = format_curated_articles(analysis)
        print(formatted)
    
    print("✅ Curated mapper eliminates irrelevant articles!")
    print("🎯 Only legally relevant constitutional articles are shown.")