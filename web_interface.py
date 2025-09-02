#!/usr/bin/env python3
"""
Legal Agent Web Interface
========================

Modern web-based interface for the Legal Agent system.
Provides a clean, professional UI for legal consultations.
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid
import json
import os
from enhanced_working_agent import create_enhanced_working_agent

app = Flask(__name__)
app.secret_key = 'legal_agent_secret_key_2025'

# Global agent instance
agent = None

def initialize_agent():
    """Initialize the enhanced legal agent"""
    global agent
    if agent is None:
        try:
            agent = create_enhanced_working_agent()
            print("✅ Enhanced Legal Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            return False
    return True

@app.route('/')
def index():
    """Main page with enhanced legal provisions"""
    return render_template('enhanced_index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process legal query via API"""
    try:
        if not initialize_agent():
            return jsonify({
                'error': 'Agent initialization failed',
                'success': False
            }), 500
        
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query cannot be empty',
                'success': False
            }), 400
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        # Process query with enhanced provisions
        response = agent.process_query_with_enhanced_provisions(query)
        
        # Format response for web interface
        result = {
            'success': True,
            'session_id': response['session_id'],
            'timestamp': response['timestamp'],
            'query': response['query'],
            'domain': response['domain'].replace('_', ' ').title(),
            'domain_raw': response['domain'],
            'confidence': round(response['confidence'], 3),
            'confidence_percentage': f"{min(response['confidence'] * 100, 100):.1f}%",
            'timeline': response['timeline'],
            'success_rate': response['success_rate'],
            'legal_route': response.get('legal_route', ''),
            'constitutional_articles': [],
            'constitutional_backing': response.get('constitutional_backing', ''),
            'response_time': response['response_time'],
            'enhanced_analysis': response['enhanced_analysis'],
            'formatted_response': response['formatted_response']
        }
        
        # Format constitutional articles from enhanced analysis
        if 'enhanced_analysis' in response and 'constitutional_articles' in response['enhanced_analysis']:
            for article in response['enhanced_analysis']['constitutional_articles']:
                result['constitutional_articles'].append({
                    'number': article.get('number', 'N/A'),
                    'title': article.get('title', 'N/A'),
                    'confidence': article.get('confidence', 0)
                })
        
        # Store in session history
        if 'query_history' not in session:
            session['query_history'] = []
        
        session['query_history'].append({
            'timestamp': result['timestamp'],
            'query': query,
            'domain': result['domain'],
            'confidence': result['confidence']
        })
        
        # Keep only last 10 queries
        session['query_history'] = session['query_history'][-10:]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Processing failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/feedback', methods=['POST'])
def process_feedback():
    """Process user feedback"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        domain = data.get('domain', '')
        confidence = data.get('confidence', 0)
        feedback = data.get('feedback', '')
        
        if not all([query, domain, feedback]):
            return jsonify({
                'error': 'Missing required feedback data',
                'success': False
            }), 400
        
        # Process feedback through agent
        if agent and hasattr(agent, 'process_feedback'):
            agent.process_feedback(query, domain, confidence, feedback)
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Feedback processing failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/history')
def get_history():
    """Get query history"""
    history = session.get('query_history', [])
    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        stats = {
            'success': True,
            'agent_status': 'Active' if agent else 'Inactive',
            'domains_supported': [
                'Criminal Law', 'Employment Law', 'Family Law', 
                'Tenant Rights', 'Consumer Complaints', 'Cyber Crime',
                'Immigration Law', 'Contract Disputes', 'Elder Abuse', 
                'Personal Injury'
            ],
            'constitutional_articles': 121,
            'training_examples': 244,
            'session_queries': len(session.get('query_history', [])),
            'system_version': 'Enhanced Legal Agent v5.0.0'
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error': f'Stats retrieval failed: {str(e)}',
            'success': False
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Starting Legal Agent Web Interface...")
    print("📋 Initializing agent...")
    
    if initialize_agent():
        print("✅ Agent ready!")
        print("🌐 Starting web server...")
        print("📱 Access at: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to start - agent initialization failed")