"""
State Memory - Task 2 Implementation
===================================

This module tracks how the agent has improved on each query using SQLite storage.
Implements the state_memory.py requirement for Task 2.

Features:
- SQLite database for persistent storage
- Pattern recognition across similar queries
- Query evolution tracking
- Performance improvement metrics
- Learning progress persistence

Author: Legal Agent Team
Version: 3.0.0 (Task 2 - State Memory)
Date: 2025-08-15
"""

import sqlite3
import json
import datetime
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, Counter
import logging
import os
import re

logger = logging.getLogger(__name__)


@dataclass
class QueryPattern:
    """Query pattern for similarity matching"""
    pattern_id: str
    domain: str
    keywords: List[str]
    query_count: int
    average_confidence: float
    improvement_trend: float
    last_updated: str


@dataclass
class ImprovementRecord:
    """Individual improvement record"""
    record_id: str
    session_id: str
    query: str
    domain: str
    confidence_before: float
    confidence_after: float
    feedback_type: str
    improvement_score: float
    pattern_id: Optional[str]
    timestamp: str


class StateMemory:
    """
    SQLite-based improvement tracker with pattern recognition.
    
    This is the main state_memory.py module required for Task 2.
    Tracks agent learning and improvement over time.
    """

    def __init__(self, 
                 db_file: str = "state_memory.db",
                 evolution_log_file: str = "query_evolution_log.json"):
        """Initialize state memory"""
        
        self.db_file = db_file
        self.evolution_log_file = evolution_log_file
        
        # Initialize database
        self.init_database()
        
        # Pattern matching parameters
        self.similarity_threshold = 0.5  # Lowered from 0.7 for better grouping
        self.min_pattern_queries = 3
        
        # Learning statistics
        self.learning_stats = {
            'total_records': 0,
            'unique_patterns': 0,
            'average_improvement': 0.0,
            'successful_learnings': 0
        }
        
        # Load existing data
        self.load_learning_stats()
        
        logger.info(f"State memory initialized with database: {self.db_file}")

    def init_database(self):
        """Initialize SQLite database with required tables"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create improvement_records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS improvement_records (
                    record_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    query TEXT,
                    domain TEXT,
                    confidence_before REAL,
                    confidence_after REAL,
                    feedback_type TEXT,
                    improvement_score REAL,
                    pattern_id TEXT,
                    timestamp TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create query_patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    domain TEXT,
                    keywords TEXT,
                    query_count INTEGER,
                    average_confidence REAL,
                    improvement_trend REAL,
                    last_updated TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create learning_sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT,
                    end_time TEXT,
                    total_queries INTEGER,
                    total_improvements REAL,
                    success_rate REAL,
                    domains TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create confidence_evolution table for detailed tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS confidence_evolution (
                    evolution_id TEXT PRIMARY KEY,
                    query_hash TEXT,
                    domain TEXT,
                    confidence_values TEXT,
                    feedback_history TEXT,
                    improvement_trajectory REAL,
                    last_updated TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain ON improvement_records(domain)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_pattern ON improvement_records(pattern_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON improvement_records(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_query_hash ON confidence_evolution(query_hash)')
            
            conn.commit()
            conn.close()
            
            logger.info("Database tables initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def record_query_improvement(self,
                                query: str,
                                domain: str,
                                confidence_before: float,
                                confidence_after: float,
                                feedback_type: str,
                                session_id: str = None) -> str:
        """
        Record a query improvement event.
        
        Args:
            query: User query text
            domain: Legal domain
            confidence_before: Confidence before feedback
            confidence_after: Confidence after feedback
            feedback_type: Type of feedback (positive, negative, etc.)
            session_id: Optional session ID
            
        Returns:
            record_id: Unique identifier for the record
        """
        
        # Generate record ID
        record_id = self._generate_record_id()
        session_id = session_id or f"session_{record_id[:8]}"
        
        # Calculate improvement score
        improvement_score = confidence_after - confidence_before
        
        # Find or create query pattern
        pattern_id = self._find_or_create_pattern(query, domain)
        
        # Create improvement record
        record = ImprovementRecord(
            record_id=record_id,
            session_id=session_id,
            query=query,
            domain=domain,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            feedback_type=feedback_type,
            improvement_score=improvement_score,
            pattern_id=pattern_id,
            timestamp=datetime.datetime.now().isoformat()
        )
        
        # Store in database
        self._store_improvement_record(record)
        
        # Update query pattern statistics
        self._update_pattern_statistics(pattern_id, improvement_score, confidence_after)
        
        # Update confidence evolution tracking
        self._update_confidence_evolution(query, domain, confidence_after, feedback_type)
        
        # Update learning statistics
        self._update_learning_statistics(improvement_score)
        
        # Log to evolution file
        self._log_evolution_event(record)
        
        logger.info(f"Recorded improvement: {improvement_score:+.3f} for domain {domain}")
        
        return record_id

    def _find_or_create_pattern(self, query: str, domain: str) -> str:
        """Find existing pattern or create new one"""
        
        # Extract keywords from query
        keywords = self._extract_keywords(query)
        
        # Find similar existing patterns
        similar_pattern = self._find_similar_pattern(keywords, domain)
        
        if similar_pattern:
            return similar_pattern
        else:
            # Create new pattern
            return self._create_new_pattern(keywords, domain)

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query for pattern matching"""
        
        # Clean and tokenize query
        query_clean = re.sub(r'[^\w\s]', ' ', query.lower())
        words = query_clean.split()
        
        # Filter out common stop words and short words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
            'not', 'no', 'what', 'how', 'when', 'where', 'why', 'who'
        }
        
        # Legal concept keywords that should be prioritized
        legal_concepts = {
            'landlord': 'landlord', 'tenant': 'tenant', 'rent': 'rent', 'deposit': 'deposit',
            'security': 'deposit', 'eviction': 'eviction', 'lease': 'lease', 'contract': 'contract',
            'employer': 'employer', 'employee': 'employee', 'wages': 'wages', 'overtime': 'wages',
            'harassment': 'harassment', 'discrimination': 'discrimination', 'termination': 'termination',
            'cyber': 'cybercrime', 'hack': 'cybercrime', 'fraud': 'fraud', 'scam': 'fraud',
            'police': 'criminal', 'court': 'court', 'lawyer': 'legal', 'legal': 'legal'
        }
        
        # Extract keywords with concept mapping
        keywords = []
        for word in words:
            if len(word) > 2 and word not in stop_words:
                # Map to legal concept if available
                concept = legal_concepts.get(word, word)
                if concept not in keywords:  # Avoid duplicates
                    keywords.append(concept)
        
        # Limit to most important keywords
        return keywords[:8]  # Increased from 10 to focus on key terms

    def _find_similar_pattern(self, keywords: List[str], domain: str) -> Optional[str]:
        """Find similar existing pattern"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get patterns for the same domain
            cursor.execute('''
                SELECT pattern_id, keywords 
                FROM query_patterns 
                WHERE domain = ?
            ''', (domain,))
            
            patterns = cursor.fetchall()
            conn.close()
            
            # Calculate similarity with each pattern
            for pattern_id, keywords_str in patterns:
                pattern_keywords = json.loads(keywords_str)
                similarity = self._calculate_keyword_similarity(keywords, pattern_keywords)
                
                if similarity >= self.similarity_threshold:
                    return pattern_id
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding similar pattern: {e}")
            return None

    def _calculate_keyword_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """Calculate similarity between two keyword lists"""
        
        if not keywords1 or not keywords2:
            return 0.0
        
        set1 = set(keywords1)
        set2 = set(keywords2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0

    def _create_new_pattern(self, keywords: List[str], domain: str) -> str:
        """Create new query pattern"""
        
        pattern_id = f"pattern_{domain}_{len(keywords)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO query_patterns 
                (pattern_id, domain, keywords, total_queries, current_confidence, improvement_score, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern_id,
                domain,
                json.dumps(keywords),
                1,
                0.5,  # Initial confidence
                0.0,  # Initial improvement score
                datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created new pattern: {pattern_id}")
            return pattern_id
            
        except Exception as e:
            logger.error(f"Error creating new pattern: {e}")
            return pattern_id

    def _store_improvement_record(self, record: ImprovementRecord):
        """Store improvement record in database"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO improvement_records 
                (record_id, session_id, query, domain, confidence_before, confidence_after,
                 feedback_type, improvement_score, pattern_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record.record_id,
                record.session_id,
                record.query,
                record.domain,
                record.confidence_before,
                record.confidence_after,
                record.feedback_type,
                record.improvement_score,
                record.pattern_id,
                record.timestamp
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing improvement record: {e}")

    def _update_pattern_statistics(self, pattern_id: str, improvement_score: float, confidence: float):
        """Update pattern statistics"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get current statistics (using correct column names)
            cursor.execute('''
                SELECT total_queries, current_confidence, improvement_score
                FROM query_patterns 
                WHERE pattern_id = ?
            ''', (pattern_id,))
            
            result = cursor.fetchone()
            if result:
                total_queries, current_confidence, current_improvement = result
                
                # Handle None values
                total_queries = total_queries or 0
                current_confidence = current_confidence or 0.5
                current_improvement = current_improvement or 0.0
                
                # Update statistics
                new_count = total_queries + 1
                new_avg_confidence = (current_confidence * total_queries + confidence) / new_count
                new_improvement = (current_improvement * 0.8) + (improvement_score * 0.2)  # Weighted average
                
                cursor.execute('''
                    UPDATE query_patterns 
                    SET total_queries = ?, current_confidence = ?, improvement_score = ?, last_updated = ?
                    WHERE pattern_id = ?
                ''', (
                    new_count,
                    new_avg_confidence,
                    new_improvement,
                    datetime.datetime.now().isoformat(),
                    pattern_id
                ))
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating pattern statistics: {e}")

    def _update_confidence_evolution(self, query: str, domain: str, confidence: float, feedback_type: str):
        """Update confidence evolution tracking"""
        
        query_hash = self._generate_query_hash(query)
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Check if evolution record exists
            cursor.execute('''
                SELECT confidence_values, feedback_history, improvement_trajectory
                FROM confidence_evolution 
                WHERE query_hash = ?
            ''', (query_hash,))
            
            result = cursor.fetchone()
            
            if result:
                # Update existing record
                confidence_values = json.loads(result[0])
                feedback_history = json.loads(result[1])
                current_trajectory = result[2]
                
                confidence_values.append(confidence)
                feedback_history.append(feedback_type)
                
                # Calculate new trajectory
                if len(confidence_values) >= 2:
                    trajectory = confidence_values[-1] - confidence_values[0]
                else:
                    trajectory = current_trajectory
                
                cursor.execute('''
                    UPDATE confidence_evolution 
                    SET confidence_values = ?, feedback_history = ?, improvement_trajectory = ?, last_updated = ?
                    WHERE query_hash = ?
                ''', (
                    json.dumps(confidence_values[-10:]),  # Keep last 10 values
                    json.dumps(feedback_history[-10:]),   # Keep last 10 feedback items
                    trajectory,
                    datetime.datetime.now().isoformat(),
                    query_hash
                ))
            else:
                # Create new evolution record
                evolution_id = f"evo_{query_hash}_{datetime.datetime.now().strftime('%Y%m%d')}"
                
                cursor.execute('''
                    INSERT INTO confidence_evolution 
                    (evolution_id, query_hash, domain, confidence_values, feedback_history, 
                     improvement_trajectory, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    evolution_id,
                    query_hash,
                    domain,
                    json.dumps([confidence]),
                    json.dumps([feedback_type]),
                    0.0,
                    datetime.datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating confidence evolution: {e}")

    def _generate_query_hash(self, query: str) -> str:
        """Generate hash for similar queries"""
        
        # Normalize query for hashing
        normalized = re.sub(r'[^\w\s]', ' ', query.lower())
        words = normalized.split()
        
        # Remove stop words and sort for consistent hashing
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        significant_words = [word for word in words if word not in stop_words and len(word) > 2]
        significant_words.sort()
        
        # Create hash from significant words
        hash_string = '_'.join(significant_words[:5])  # Use top 5 words
        return f"qhash_{hash(hash_string) % 1000000:06d}"

    def _update_learning_statistics(self, improvement_score: float):
        """Update global learning statistics"""
        
        self.learning_stats['total_records'] += 1
        
        # Update average improvement
        total_records = self.learning_stats['total_records']
        old_avg = self.learning_stats['average_improvement']
        self.learning_stats['average_improvement'] = (old_avg * (total_records - 1) + improvement_score) / total_records
        
        # Count successful learnings (positive improvement)
        if improvement_score > 0:
            self.learning_stats['successful_learnings'] += 1

    def _log_evolution_event(self, record: ImprovementRecord):
        """Log evolution event to JSON file"""
        
        try:
            # Load existing log
            evolution_log = []
            if os.path.exists(self.evolution_log_file):
                try:
                    # Try different encodings to handle existing files
                    with open(self.evolution_log_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read().strip()
                        if content:  # Only parse if file is not empty
                            evolution_log = json.loads(content)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # If there's an encoding or JSON error, start fresh
                    logger.warning(f"Could not read {self.evolution_log_file}, starting fresh")
                    evolution_log = []
            
            # Add new event
            evolution_event = {
                'timestamp': record.timestamp,
                'record_id': record.record_id,
                'session_id': record.session_id,
                'domain': record.domain,
                'feedback_type': record.feedback_type,
                'confidence_change': record.confidence_after - record.confidence_before,
                'improvement_score': record.improvement_score,
                'pattern_id': record.pattern_id
            }
            
            evolution_log.append(evolution_event)
            
            # Keep last 1000 events
            if len(evolution_log) > 1000:
                evolution_log = evolution_log[-800:]
            
            # Save updated log with proper encoding
            with open(self.evolution_log_file, 'w', encoding='utf-8') as f:
                json.dump(evolution_log, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error logging evolution event: {e}")

    def get_pattern_insights(self, domain: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get insights about query patterns"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if domain:
                cursor.execute('''
                    SELECT pattern_id, domain, keywords, total_queries, current_confidence, improvement_score
                    FROM query_patterns 
                    WHERE domain = ?
                    ORDER BY improvement_score DESC, total_queries DESC
                    LIMIT ?
                ''', (domain, limit))
            else:
                cursor.execute('''
                    SELECT pattern_id, domain, keywords, total_queries, current_confidence, improvement_score
                    FROM query_patterns 
                    ORDER BY improvement_score DESC, total_queries DESC
                    LIMIT ?
                ''', (limit,))
            
            patterns = cursor.fetchall()
            conn.close()
            
            insights = []
            for pattern in patterns:
                insights.append({
                    'pattern_id': pattern[0],
                    'domain': pattern[1],
                    'keywords': json.loads(pattern[2]) if pattern[2] else [],
                    'query_count': pattern[3] or 0,
                    'average_confidence': pattern[4] or 0.0,
                    'improvement_trend': pattern[5] or 0.0
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting pattern insights: {e}")
            return []

    def get_domain_performance(self, domain: str) -> Dict[str, Any]:
        """Get performance metrics for a specific domain"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get improvement statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_queries,
                    AVG(improvement_score) as avg_improvement,
                    AVG(confidence_after) as avg_confidence,
                    COUNT(CASE WHEN improvement_score > 0 THEN 1 END) as positive_improvements,
                    COUNT(CASE WHEN feedback_type = 'positive' THEN 1 END) as positive_feedback_count
                FROM improvement_records 
                WHERE domain = ?
            ''', (domain,))
            
            result = cursor.fetchone()
            
            if result and result[0] > 0:
                total_queries, avg_improvement, avg_confidence, positive_improvements, positive_feedback = result
                
                performance = {
                    'domain': domain,
                    'total_queries': total_queries,
                    'average_improvement': avg_improvement or 0.0,
                    'average_confidence': avg_confidence or 0.0,
                    'success_rate': positive_improvements / total_queries if total_queries > 0 else 0.0,
                    'positive_feedback_rate': positive_feedback / total_queries if total_queries > 0 else 0.0
                }
            else:
                performance = {
                    'domain': domain,
                    'total_queries': 0,
                    'average_improvement': 0.0,
                    'average_confidence': 0.0,
                    'success_rate': 0.0,
                    'positive_feedback_rate': 0.0
                }
            
            conn.close()
            return performance
            
        except Exception as e:
            logger.error(f"Error getting domain performance: {e}")
            return {}

    def get_learning_trajectory(self, query_hash: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get learning trajectory for specific query or overall"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if query_hash:
                cursor.execute('''
                    SELECT confidence_values, feedback_history, improvement_trajectory, last_updated
                    FROM confidence_evolution 
                    WHERE query_hash = ?
                ''', (query_hash,))
                
                result = cursor.fetchone()
                if result:
                    return [{
                        'query_hash': query_hash,
                        'confidence_values': json.loads(result[0]),
                        'feedback_history': json.loads(result[1]),
                        'improvement_trajectory': result[2],
                        'last_updated': result[3]
                    }]
            else:
                # Get overall learning trajectory
                cursor.execute('''
                    SELECT record_id, domain, confidence_before, confidence_after, 
                           improvement_score, feedback_type, timestamp
                    FROM improvement_records 
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                records = cursor.fetchall()
                trajectory = []
                
                for record in records:
                    trajectory.append({
                        'record_id': record[0],
                        'domain': record[1],
                        'confidence_before': record[2],
                        'confidence_after': record[3],
                        'improvement_score': record[4],
                        'feedback_type': record[5],
                        'timestamp': record[6]
                    })
                
                return trajectory
            
            conn.close()
            return []
            
        except Exception as e:
            logger.error(f"Error getting learning trajectory: {e}")
            return []

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get overall memory statistics"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get pattern count
            cursor.execute('SELECT COUNT(*) FROM query_patterns')
            pattern_count = cursor.fetchone()[0]
            
            # Get domain distribution
            cursor.execute('''
                SELECT domain, COUNT(*) 
                FROM improvement_records 
                GROUP BY domain 
                ORDER BY COUNT(*) DESC
            ''')
            domain_distribution = dict(cursor.fetchall())
            
            # Get recent activity
            cursor.execute('''
                SELECT COUNT(*) 
                FROM improvement_records 
                WHERE timestamp >= date('now', '-7 days')
            ''')
            recent_activity = cursor.fetchone()[0]
            
            conn.close()
            
            stats = {
                **self.learning_stats,
                'unique_patterns': pattern_count,
                'domain_distribution': domain_distribution,
                'recent_activity_7days': recent_activity,
                'database_file': self.db_file,
                'evolution_log_file': self.evolution_log_file
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return self.learning_stats

    def load_learning_stats(self):
        """Load learning statistics from database"""
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get total records
            cursor.execute('SELECT COUNT(*) FROM improvement_records')
            self.learning_stats['total_records'] = cursor.fetchone()[0]
            
            # Get average improvement
            cursor.execute('SELECT AVG(improvement_score) FROM improvement_records')
            result = cursor.fetchone()[0]
            self.learning_stats['average_improvement'] = result if result else 0.0
            
            # Get successful learnings
            cursor.execute('SELECT COUNT(*) FROM improvement_records WHERE improvement_score > 0')
            self.learning_stats['successful_learnings'] = cursor.fetchone()[0]
            
            # Get unique patterns
            cursor.execute('SELECT COUNT(*) FROM query_patterns')
            self.learning_stats['unique_patterns'] = cursor.fetchone()[0]
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error loading learning stats: {e}")

    def _generate_record_id(self) -> str:
        """Generate unique record ID"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        return f"rec_{timestamp}"


def create_state_memory(db_file: str = "state_memory.db") -> StateMemory:
    """Factory function to create state memory"""
    return StateMemory(db_file=db_file)


# Test the state memory
if __name__ == "__main__":
    print("🧠 STATE MEMORY TEST")
    print("=" * 50)
    
    # Create test state memory
    state_memory = create_state_memory("test_state_memory.db")
    
    # Test recording improvements
    test_cases = [
        {
            'query': 'my landlord is not returning my security deposit',
            'domain': 'tenant_rights',
            'confidence_before': 0.6,
            'confidence_after': 0.8,
            'feedback_type': 'positive'
        },
        {
            'query': 'landlord refusing to return deposit money',
            'domain': 'tenant_rights',
            'confidence_before': 0.7,
            'confidence_after': 0.9,
            'feedback_type': 'positive'
        },
        {
            'query': 'someone hacked my bank account',
            'domain': 'cyber_crime',
            'confidence_before': 0.5,
            'confidence_after': 0.4,
            'feedback_type': 'negative'
        }
    ]
    
    print("Recording test improvements:")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        record_id = state_memory.record_query_improvement(**test_case)
        print(f"Test {i}: Recorded {record_id}")
    
    # Get pattern insights
    print(f"\nPattern Insights:")
    insights = state_memory.get_pattern_insights()
    for insight in insights:
        print(f"   Pattern: {insight['pattern_id']}")
        print(f"   Domain: {insight['domain']}")
        print(f"   Keywords: {insight['keywords'][:3]}")
        print(f"   Improvement Trend: {insight['improvement_trend']:+.3f}")
        print()
    
    # Get domain performance
    print(f"Domain Performance:")
    for domain in ['tenant_rights', 'cyber_crime']:
        performance = state_memory.get_domain_performance(domain)
        print(f"   {domain}: {performance['total_queries']} queries, {performance['success_rate']:.1%} success")
    
    # Get memory statistics
    stats = state_memory.get_memory_stats()
    print(f"\nMemory Statistics:")
    print(f"   Total Records: {stats['total_records']}")
    print(f"   Unique Patterns: {stats['unique_patterns']}")
    print(f"   Average Improvement: {stats['average_improvement']:+.3f}")
    print(f"   Success Rate: {stats['successful_learnings']}/{stats['total_records']}")
    
    print("\n✅ State memory test completed successfully!")
    
    # Clean up test database
    import os
    if os.path.exists("test_state_memory.db"):
        os.remove("test_state_memory.db")
        print("🗑️ Test database cleaned up")