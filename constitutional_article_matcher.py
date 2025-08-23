"""
Constitutional Article Matcher with Confidence Scoring
=====================================================

This module provides comprehensive constitutional article matching with confidence
percentages based on query analysis. It searches through all articles in the
article.json file and provides specific article recommendations with confidence scores.

Features:
- Confidence-based article matching
- Comprehensive article database search
- Query-specific constitutional recommendations
- Detailed relevance scoring

Author: Legal Agent Team
Version: 1.0.0 - Constitutional Article Matcher
Date: 2025-08-23
"""

import json
import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import logging
from pathlib import Path
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ArticleMatch:
    """Data structure for article matches with confidence scores"""
    article_number: str
    title: str
    content: str
    confidence: float
    relevance_score: int
    matching_keywords: List[str]
    match_reasons: List[str]
    
    @property
    def clean_title(self) -> str:
        """Get cleaned title without quotes"""
        return self.title.strip('"').strip()
    
    @property
    def confidence_percentage(self) -> int:
        """Get confidence as percentage"""
        return min(100, max(0, int(self.confidence * 100)))


class ConstitutionalArticleMatcher:
    """Advanced constitutional article matcher with confidence scoring"""
    
    def __init__(self, articles_file: str = "article.json"):
        """Initialize the article matcher"""
        self.articles_file = articles_file
        self.articles = []
        self.load_articles()
        self.create_keyword_mappings()
    
    def load_articles(self):
        """Load all constitutional articles from JSON file"""
        try:
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                self.articles = json.load(f)
            
            logger.info(f"Loaded {len(self.articles)} constitutional articles for matching")
            
        except FileNotFoundError:
            logger.error(f"Constitutional articles file {self.articles_file} not found")
            self.articles = []
        except Exception as e:
            logger.error(f"Error loading constitutional articles: {e}")
            self.articles = []
    
    def create_keyword_mappings(self):
        """Create comprehensive keyword mappings for better matching"""
        
        self.domain_keywords = {
            # Employment & Workplace
            'employment': ['work', 'job', 'employment', 'workplace', 'office', 'employee', 'employer', 'salary', 'wages', 'termination'],
            'harassment': ['harassment', 'harassing', 'harass', 'abuse', 'misbehavior', 'misconduct', 'inappropriate'],
            'discrimination': ['discrimination', 'discriminate', 'bias', 'prejudice', 'unfair treatment', 'inequality'],
            
            # Property & Housing  
            'property': ['property', 'house', 'home', 'rent', 'tenant', 'landlord', 'deposit', 'eviction', 'maintenance'],
            'housing': ['housing', 'shelter', 'residence', 'dwelling', 'accommodation'],
            
            # Criminal Law
            'crime': ['crime', 'criminal', 'theft', 'robbery', 'murder', 'assault', 'fraud', 'cheat', 'violence'],
            'cyber': ['cyber', 'online', 'internet', 'hacking', 'digital', 'computer', 'technology', 'electronic'],
            
            # Family Law
            'family': ['family', 'marriage', 'divorce', 'child', 'custody', 'domestic', 'spouse', 'husband', 'wife'],
            'violence': ['violence', 'abuse', 'beating', 'torture', 'harm', 'injury', 'threat'],
            
            # Rights & Freedoms
            'freedom': ['freedom', 'liberty', 'right', 'expression', 'speech', 'religion', 'movement'],
            'equality': ['equality', 'equal', 'discrimination', 'caste', 'religion', 'sex', 'gender'],
            
            # Government & Administration
            'government': ['government', 'state', 'parliament', 'president', 'governor', 'minister', 'administration'],
            'election': ['election', 'voting', 'vote', 'candidate', 'electoral', 'democracy'],
            'citizenship': ['citizen', 'citizenship', 'nationality', 'passport', 'migration'],
            
            # Legal Process
            'court': ['court', 'judge', 'justice', 'legal', 'law', 'jurisdiction', 'appeal', 'writ'],
            'emergency': ['emergency', 'crisis', 'martial law', 'proclamation', 'suspension']
        }
        
        # Article-specific keyword mappings
        self.article_keywords = {
            # Territory & Union (Articles 1-4)
            'territory': ['1', '2', '3', '4'],
            'union': ['1', '2', '3'],
            'states': ['1', '2', '3', '4'],
            
            # Citizenship (Articles 5-11)
            'citizenship': ['5', '6', '7', '8', '9', '10', '11'],
            'migration': ['6', '7'],
            'foreign': ['8', '9'],
            
            # Fundamental Rights (Articles 12-35)
            'equality': ['12', '13', '14', '15', '16', '17', '18'],
            'freedom': ['19', '20', '21', '22'],
            'exploitation': ['23', '24'],
            'religion': ['25', '26', '27', '28'],
            'minorities': ['29', '30'],
            'remedies': ['32', '33', '34', '35'],
            
            # Government Structure (Articles 52-123)
            'president': ['52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62'],
            'parliament': ['79', '80', '81', '82', '83', '84', '85', '86'],
            'ministers': ['74', '75', '76', '77', '78'],
            'procedures': ['87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98'],
            'bills': ['107', '108', '109', '110', '111'],
            'financial': ['112', '113', '114', '115', '116', '117'],
            'ordinance': ['123'],
            
            # Judiciary (Articles 124-147)
            'supreme_court': ['124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147'],
            'chief_justice': ['124', '126', '128'],
            'jurisdiction': ['131', '132', '133', '134', '136', '138'],
            
            # State Government (Articles 153-167)
            'governor': ['153', '154', '155', '156', '157', '158', '159', '160', '161'],
            'state_executive': ['162', '163', '164', '165', '166', '167'],
            
            # High Courts (Articles 214-231)
            'high_court': ['214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231'],
            
            # Elections (Articles 324-329)
            'election': ['324', '325', '326', '327', '328', '329'],
            'voting': ['325', '326'],
            
            # Language (Articles 343-351)
            'language': ['343', '344', '345', '346', '347', '348', '349', '350', '351'],
            'hindi': ['343', '344', '351'],
            
            # Emergency (Articles 352-360)
            'emergency': ['352', '356', '360'],
            
            # Amendment (Article 368)
            'amendment': ['368']
        }
    
    def calculate_confidence(self, article: Dict, query: str, matching_keywords: List[str], 
                           relevance_score: int) -> float:
        """Calculate confidence score for article match"""
        
        query_lower = query.lower()
        title_lower = article.get('title', '').lower().strip('"')
        content_lower = article.get('content', '').lower()
        
        confidence = 0.0
        
        # Base score from relevance
        confidence += min(0.4, relevance_score * 0.05)
        
        # Exact article number match (if query contains "article X")
        article_num = article.get('article_number', '')
        if f"article {article_num}" in query_lower or f"article{article_num}" in query_lower:
            confidence += 0.5
        
        # Title relevance scoring
        title_words = title_lower.split()
        query_words = query_lower.split()
        
        # Calculate title word overlap
        common_words = set(title_words) & set(query_words)
        if title_words:
            title_overlap = len(common_words) / len(title_words)
            confidence += title_overlap * 0.3
        
        # Keyword matching bonus
        keyword_bonus = min(0.2, len(matching_keywords) * 0.05)
        confidence += keyword_bonus
        
        # Content relevance (if available)
        if content_lower:
            content_words = set(content_lower.split())
            content_overlap = len(set(query_words) & content_words) / max(1, len(query_words))
            confidence += content_overlap * 0.2
        
        # Domain-specific bonuses
        domain_bonus = self._calculate_domain_bonus(query_lower, title_lower, content_lower)
        confidence += domain_bonus
        
        # Normalize confidence to 0-1 range
        return min(1.0, max(0.0, confidence))
    
    def _calculate_domain_bonus(self, query: str, title: str, content: str) -> float:
        """Calculate domain-specific confidence bonus"""
        
        bonus = 0.0
        text_combined = f"{title} {content}".lower()
        
        # Specific domain patterns
        domain_patterns = {
            'fundamental rights': ['right', 'freedom', 'equality', 'liberty', 'protection'],
            'government structure': ['president', 'parliament', 'minister', 'governor', 'executive'],
            'judiciary': ['court', 'judge', 'justice', 'jurisdiction', 'appeal'],
            'citizenship': ['citizen', 'nationality', 'migration', 'foreign'],
            'elections': ['election', 'vote', 'electoral', 'suffrage'],
            'emergency': ['emergency', 'proclamation', 'martial law'],
            'language': ['language', 'hindi', 'english', 'official']
        }
        
        for domain, keywords in domain_patterns.items():
            if any(keyword in query for keyword in keywords):
                matching_keywords_in_text = sum(1 for kw in keywords if kw in text_combined)
                if matching_keywords_in_text > 0:
                    bonus += 0.1 * (matching_keywords_in_text / len(keywords))
        
        return min(0.2, bonus)
    
    def find_matching_articles(self, query: str, limit: int = 10) -> List[ArticleMatch]:
        """Find constitutional articles matching the query with confidence scores"""
        
        if not self.articles:
            return []
        
        query_lower = query.lower()
        matches = []
        
        # Analyze each article
        for article in self.articles:
            article_number = article.get('article_number', '')
            title = article.get('title', '').strip('"')
            content = article.get('content', '')
            
            # Calculate relevance score
            relevance_score = 0
            matching_keywords = []
            match_reasons = []
            
            # Check for direct matches
            title_lower = title.lower()
            content_lower = content.lower()
            
            # Exact article number reference
            if f"article {article_number}" in query_lower or f"article{article_number}" in query_lower:
                relevance_score += 10
                matching_keywords.append(f"Article {article_number}")
                match_reasons.append(f"Direct article reference: Article {article_number}")
            
            # Title keyword matching
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 2:  # Skip very short words
                    if word in title_lower:
                        relevance_score += 3
                        matching_keywords.append(word)
                        match_reasons.append(f"Title contains: '{word}'")
                    
                    if content and word in content_lower:
                        relevance_score += 2
                        if word not in matching_keywords:
                            matching_keywords.append(word)
                        if f"Content contains: '{word}'" not in match_reasons:
                            match_reasons.append(f"Content contains: '{word}'")
            
            # Domain-based keyword matching
            for domain, keywords in self.domain_keywords.items():
                for keyword in keywords:
                    if keyword in query_lower:
                        if keyword in title_lower or (content and keyword in content_lower):
                            relevance_score += 1
                            if keyword not in matching_keywords:
                                matching_keywords.append(keyword)
                            if f"Domain relevance: {domain}" not in match_reasons:
                                match_reasons.append(f"Domain relevance: {domain}")
            
            # Article-specific keyword matching
            for topic, article_numbers in self.article_keywords.items():
                if article_number in article_numbers:
                    if any(kw in query_lower for kw in topic.split('_')):
                        relevance_score += 2
                        match_reasons.append(f"Topic relevance: {topic}")
            
            # Only include articles with some relevance
            if relevance_score > 0:
                confidence = self.calculate_confidence(article, query, matching_keywords, relevance_score)
                
                match = ArticleMatch(
                    article_number=article_number,
                    title=title,
                    content=content,
                    confidence=confidence,
                    relevance_score=relevance_score,
                    matching_keywords=matching_keywords[:5],  # Limit keywords
                    match_reasons=match_reasons[:3]  # Limit reasons
                )
                
                matches.append(match)
        
        # Sort by confidence (highest first)
        matches.sort(key=lambda x: x.confidence, reverse=True)
        
        return matches[:limit]
    
    def get_article_recommendations(self, query: str) -> Dict[str, Any]:
        """Get comprehensive article recommendations with confidence analysis"""
        
        matches = self.find_matching_articles(query, limit=10)
        
        if not matches:
            return {
                'total_articles_searched': len(self.articles),
                'matching_articles': 0,
                'recommendations': [],
                'confidence_summary': 'No relevant constitutional articles found for this query.'
            }
        
        # Categorize matches by confidence
        high_confidence = [m for m in matches if m.confidence >= 0.7]
        medium_confidence = [m for m in matches if 0.4 <= m.confidence < 0.7]
        low_confidence = [m for m in matches if m.confidence < 0.4]
        
        # Prepare recommendations
        recommendations = []
        for match in matches[:5]:  # Top 5 recommendations
            recommendations.append({
                'article_number': match.article_number,
                'title': match.clean_title,
                'confidence_percentage': match.confidence_percentage,
                'relevance_score': match.relevance_score,
                'matching_keywords': match.matching_keywords,
                'match_reasons': match.match_reasons,
                'content_preview': match.content[:200] + "..." if len(match.content) > 200 else match.content
            })
        
        return {
            'total_articles_searched': len(self.articles),
            'matching_articles': len(matches),
            'recommendations': recommendations,
            'confidence_summary': {
                'high_confidence': len(high_confidence),
                'medium_confidence': len(medium_confidence),  
                'low_confidence': len(low_confidence),
                'top_match_confidence': matches[0].confidence_percentage if matches else 0
            },
            'query_analysis': {
                'processed_query': query,
                'total_keywords_found': len(set([kw for m in matches[:3] for kw in m.matching_keywords])),
                'primary_domains': self._identify_primary_domains(query)
            }
        }
    
    def _identify_primary_domains(self, query: str) -> List[str]:
        """Identify primary legal domains from query"""
        
        query_lower = query.lower()
        identified_domains = []
        
        domain_indicators = {
            'employment_law': ['work', 'job', 'employment', 'workplace', 'salary', 'boss', 'colleague'],
            'criminal_law': ['crime', 'theft', 'murder', 'assault', 'police', 'arrest'],
            'family_law': ['marriage', 'divorce', 'family', 'child', 'custody', 'domestic'],
            'property_law': ['property', 'house', 'rent', 'landlord', 'tenant', 'deposit'],
            'constitutional_law': ['constitution', 'fundamental', 'rights', 'freedom', 'government'],
            'cyber_law': ['cyber', 'online', 'internet', 'hacking', 'digital']
        }
        
        for domain, indicators in domain_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                identified_domains.append(domain.replace('_', ' ').title())
        
        return identified_domains[:3]  # Return top 3 domains


# Create global matcher instance
constitutional_matcher = ConstitutionalArticleMatcher()


def get_constitutional_articles_with_confidence(query: str) -> Dict[str, Any]:
    """Main function to get constitutional articles with confidence percentages"""
    return constitutional_matcher.get_article_recommendations(query)


def format_article_recommendations(recommendations: Dict[str, Any]) -> str:
    """Format article recommendations for display"""
    
    if recommendations['matching_articles'] == 0:
        return "❌ No relevant constitutional articles found for this query."
    
    output = []
    
    # Header
    output.append("🏛️ CONSTITUTIONAL ARTICLES ANALYSIS")
    output.append("=" * 50)
    output.append("")
    
    # Search summary
    output.append(f"📊 Search Summary:")
    output.append(f"   • Total Articles Searched: {recommendations['total_articles_searched']}")
    output.append(f"   • Matching Articles Found: {recommendations['matching_articles']}")
    output.append(f"   • Primary Domains: {', '.join(recommendations['query_analysis']['primary_domains'])}")
    output.append("")
    
    # Confidence summary
    conf_summary = recommendations['confidence_summary']
    output.append(f"🎯 Confidence Distribution:")
    output.append(f"   • High Confidence (70-100%): {conf_summary['high_confidence']} articles")
    output.append(f"   • Medium Confidence (40-69%): {conf_summary['medium_confidence']} articles")
    output.append(f"   • Low Confidence (0-39%): {conf_summary['low_confidence']} articles")
    output.append(f"   • Top Match Confidence: {conf_summary['top_match_confidence']}%")
    output.append("")
    
    # Article recommendations
    output.append("📋 RECOMMENDED CONSTITUTIONAL ARTICLES:")
    output.append("")
    
    for i, rec in enumerate(recommendations['recommendations'], 1):
        # Confidence indicator
        confidence = rec['confidence_percentage']
        if confidence >= 70:
            conf_icon = "🟢"
        elif confidence >= 40:
            conf_icon = "🟡"
        else:
            conf_icon = "🔴"
        
        output.append(f"{conf_icon} {i}. Article {rec['article_number']} - {confidence}% Confidence")
        output.append(f"   📖 Title: {rec['title']}")
        
        if rec['matching_keywords']:
            output.append(f"   🔍 Keywords: {', '.join(rec['matching_keywords'])}")
        
        if rec['match_reasons']:
            output.append(f"   💡 Relevance: {rec['match_reasons'][0]}")
        
        if rec.get('content_preview'):
            output.append(f"   📄 Content: {rec['content_preview']}")
        
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test the matcher
    test_queries = [
        "my phone is being hacked",
        "landlord not returning security deposit", 
        "workplace harassment by colleague",
        "fundamental rights violation"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        print("-" * 50)
        recommendations = get_constitutional_articles_with_confidence(query)
        formatted_output = format_article_recommendations(recommendations)
        print(formatted_output)