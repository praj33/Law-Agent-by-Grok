#!/usr/bin/env python3
"""
Query Storage System
===================

This module handles storage and retrieval of user queries for analysis and improvement.
Stores queries with timestamps, domains, confidence scores, and feedback.
"""

import json
import sqlite3
import datetime
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class StoredQuery:
    """Represents a stored query with metadata"""
    query_id: str
    timestamp: str
    user_query: str
    domain: str
    confidence: float
    legal_route: str
    timeline: str
    success_rate: str
    constitutional_articles: List[str]
    feedback: Optional[str] = None
    feedback_type: Optional[str] = None
    session_id: Optional[str] = None
    response_time: Optional[float] = None


class QueryStorage:
    """Handles storage and retrieval of user queries"""
    
    def __init__(self, db_path: str = "query_storage.db"):
        """Initialize query storage with SQLite database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create queries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    query_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    user_query TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    legal_route TEXT,
                    timeline TEXT,
                    success_rate TEXT,
                    constitutional_articles TEXT,
                    feedback TEXT,
                    feedback_type TEXT,
                    session_id TEXT,
                    response_time REAL
                )
            ''')
            
            # Create index for faster searching
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON queries(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain ON queries(domain)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_query ON queries(user_query)')
            
            conn.commit()
            conn.close()
            logger.info("Query storage database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing query storage database: {e}")
    
    def store_query(self, query: str, response, session_id: str = None, response_time: float = None) -> str:
        """Store a query with its response"""
        try:
            query_id = f"q_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            timestamp = datetime.datetime.now().isoformat()
            
            # Extract constitutional articles
            constitutional_articles = []
            if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                constitutional_articles = [f"Article {art.get('article_number', 'N/A')}" 
                                        for art in response.constitutional_articles[:3]]
            
            stored_query = StoredQuery(
                query_id=query_id,
                timestamp=timestamp,
                user_query=query,
                domain=response.domain,
                confidence=response.confidence,
                legal_route=getattr(response, 'legal_route', ''),
                timeline=getattr(response, 'timeline', ''),
                success_rate=getattr(response, 'success_rate', 'N/A'),
                constitutional_articles=constitutional_articles,
                session_id=session_id,
                response_time=response_time
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO queries (
                    query_id, timestamp, user_query, domain, confidence,
                    legal_route, timeline, success_rate, constitutional_articles,
                    session_id, response_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                stored_query.query_id,
                stored_query.timestamp,
                stored_query.user_query,
                stored_query.domain,
                stored_query.confidence,
                stored_query.legal_route,
                stored_query.timeline,
                stored_query.success_rate,
                json.dumps(stored_query.constitutional_articles),
                stored_query.session_id,
                stored_query.response_time
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored query: {query_id}")
            return query_id
            
        except Exception as e:
            logger.error(f"Error storing query: {e}")
            return None
    
    def update_feedback(self, query_id: str, feedback: str, feedback_type: str):
        """Update feedback for a stored query"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE queries 
                SET feedback = ?, feedback_type = ?
                WHERE query_id = ?
            ''', (feedback, feedback_type, query_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Updated feedback for query: {query_id}")
            
        except Exception as e:
            logger.error(f"Error updating feedback: {e}")
    
    def get_recent_queries(self, limit: int = 10) -> List[StoredQuery]:
        """Get recent queries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM queries 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            queries = []
            for row in rows:
                constitutional_articles = json.loads(row[8]) if row[8] else []
                query = StoredQuery(
                    query_id=row[0],
                    timestamp=row[1],
                    user_query=row[2],
                    domain=row[3],
                    confidence=row[4],
                    legal_route=row[5],
                    timeline=row[6],
                    success_rate=row[7],
                    constitutional_articles=constitutional_articles,
                    feedback=row[9],
                    feedback_type=row[10],
                    session_id=row[11],
                    response_time=row[12]
                )
                queries.append(query)
            
            return queries
            
        except Exception as e:
            logger.error(f"Error getting recent queries: {e}")
            return []
    
    def get_queries_by_domain(self, domain: str, limit: int = 10) -> List[StoredQuery]:
        """Get queries by domain"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM queries 
                WHERE domain = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (domain, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            queries = []
            for row in rows:
                constitutional_articles = json.loads(row[8]) if row[8] else []
                query = StoredQuery(
                    query_id=row[0],
                    timestamp=row[1],
                    user_query=row[2],
                    domain=row[3],
                    confidence=row[4],
                    legal_route=row[5],
                    timeline=row[6],
                    success_rate=row[7],
                    constitutional_articles=constitutional_articles,
                    feedback=row[9],
                    feedback_type=row[10],
                    session_id=row[11],
                    response_time=row[12]
                )
                queries.append(query)
            
            return queries
            
        except Exception as e:
            logger.error(f"Error getting queries by domain: {e}")
            return []
    
    def search_queries(self, search_term: str, limit: int = 10) -> List[StoredQuery]:
        """Search queries by term"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM queries 
                WHERE user_query LIKE ?
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (f'%{search_term}%', limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            queries = []
            for row in rows:
                constitutional_articles = json.loads(row[8]) if row[8] else []
                query = StoredQuery(
                    query_id=row[0],
                    timestamp=row[1],
                    user_query=row[2],
                    domain=row[3],
                    confidence=row[4],
                    legal_route=row[5],
                    timeline=row[6],
                    success_rate=row[7],
                    constitutional_articles=constitutional_articles,
                    feedback=row[9],
                    feedback_type=row[10],
                    session_id=row[11],
                    response_time=row[12]
                )
                queries.append(query)
            
            return queries
            
        except Exception as e:
            logger.error(f"Error searching queries: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get query statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total queries
            cursor.execute('SELECT COUNT(*) FROM queries')
            total_queries = cursor.fetchone()[0]
            
            # Queries by domain
            cursor.execute('''
                SELECT domain, COUNT(*) 
                FROM queries 
                GROUP BY domain 
                ORDER BY COUNT(*) DESC
            ''')
            domain_stats = cursor.fetchall()
            
            # Average confidence by domain
            cursor.execute('''
                SELECT domain, AVG(confidence) 
                FROM queries 
                GROUP BY domain
            ''')
            confidence_stats = cursor.fetchall()
            
            # Feedback stats
            cursor.execute('''
                SELECT feedback_type, COUNT(*) 
                FROM queries 
                WHERE feedback_type IS NOT NULL
                GROUP BY feedback_type
            ''')
            feedback_stats = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_queries': total_queries,
                'domain_distribution': dict(domain_stats),
                'average_confidence_by_domain': dict(confidence_stats),
                'feedback_distribution': dict(feedback_stats)
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}


def create_query_storage(db_path: str = "query_storage.db") -> QueryStorage:
    """Factory function to create query storage instance"""
    return QueryStorage(db_path)


if __name__ == "__main__":
    # Test the query storage system
    storage = create_query_storage()
    
    # Test storing a dummy query
    class DummyResponse:
        def __init__(self):
            self.domain = "employment_law"
            self.confidence = 0.85
            self.legal_route = "File complaint with Labour Court"
            self.timeline = "6-12 months"
            self.success_rate = "75%"
            self.constitutional_articles = [
                {"article_number": "19", "title": "Freedom of profession"},
                {"article_number": "21", "title": "Right to life"}
            ]
    
    query_id = storage.store_query(
        "My boss is not paying overtime wages",
        DummyResponse(),
        "test_session",
        0.05
    )
    
    print(f"Stored query with ID: {query_id}")
    
    # Test getting recent queries
    recent = storage.get_recent_queries(5)
    print(f"Recent queries: {len(recent)}")
    
    # Test statistics
    stats = storage.get_statistics()
    print(f"Statistics: {stats}")