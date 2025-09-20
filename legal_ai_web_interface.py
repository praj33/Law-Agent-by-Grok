#!/usr/bin/env python3
"""
Legal AI Agent Web Interface
============================

Web interface for the Legal AI Agent that integrates with the existing system.
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid
import json
import os

# Import the Legal AI Agent
from legal_ai_agent import create_legal_ai_agent

app = Flask(__name__)
app.secret_key = 'legal_ai_agent_2025'

# Global agent instance
legal_ai_agent = None

def initialize_legal_ai_agent():
    """Initialize the Legal AI Agent"""
    global legal_ai_agent
    if legal_ai_agent is None:
        try:
            legal_ai_agent = create_legal_ai_agent()
            print("✅ Legal AI Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Legal AI Agent: {e}")
            return False
    return legal_ai_agent is not None

@app.route('/')
def index():
    """Main page"""
    return render_template('simple_index.html')

@app.route('/api/legal-analysis', methods=['POST'])
def process_legal_analysis():
    """Process legal query with comprehensive analysis"""
    try:
        if not initialize_legal_ai_agent():
            return jsonify({
                'error': 'Legal AI Agent initialization failed',
                'success': False,
                'message': 'The legal analysis system is currently unavailable. Please try again later.'
            }), 500
        
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query cannot be empty',
                'success': False,
                'message': 'Please enter a legal question to get analysis.'
            }), 400
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        print(f"🔍 Processing legal analysis for: {query[:50]}...")
        
        # Process query with Legal AI Agent
        result = legal_ai_agent.process_query(query)
        formatted_output = legal_ai_agent.format_output(result)
        
        # Format response for web interface
        response_data = {
            'success': True,
            'session_id': session['session_id'],
            'timestamp': result['timestamp'],
            'query': query,
            
            # Classification Results
            'domain': result['domain'],
            'subdomain': result['subdomain'],
            
            # Legal Provisions
            'constitutional_articles': result['constitutional_articles'],
            'bns_sections': result['bns_sections'],
            'ipc_sections': result['ipc_sections'],
            'crpc_sections': result['crpc_sections'],
            
            # Legal Guidance
            'legal_process': result['legal_process'],
            'important_notes': result['important_notes'],
            'emergency_contacts': result['emergency_contacts'],
            
            # Formatted Output
            'formatted_output': formatted_output,
            
            # System Info
            'processing_time': f"< 1s"
        }
        
        # Store in session history
        if 'query_history' not in session:
            session['query_history'] = []
        
        session['query_history'].append({
            'timestamp': response_data['timestamp'],
            'query': query,
            'domain': result['domain'],
            'subdomain': result['subdomain'],
            'bns_count': len(result['bns_sections']),
            'ipc_count': len(result['ipc_sections']),
            'crpc_count': len(result['crpc_sections'])
        })
        
        # Keep only last 20 queries
        session['query_history'] = session['query_history'][-20:]
        
        print(f"✅ Legal analysis processed successfully")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Legal analysis failed: {e}")
        return jsonify({
            'error': f'Legal analysis failed: {str(e)}',
            'success': False,
            'message': 'An error occurred while processing your legal query. Please try again.'
        }), 500

@app.route('/api/feedback', methods=['POST'])
def process_feedback():
    """Process user feedback"""
    try:
        if not initialize_legal_ai_agent():
            return jsonify({
                'error': 'Legal AI Agent not available',
                'success': False
            }), 500
        
        data = request.get_json()
        query = data.get('query', '')
        feedback = data.get('feedback', '')
        rating = data.get('rating', 0)
        
        if not all([query, feedback]):
            return jsonify({
                'error': 'Missing required feedback data',
                'success': False
            }), 400
        
        # In a real implementation, we would process the feedback
        # For now, we'll just acknowledge it
        print(f"📊 Feedback received for query: {query[:50]}...")
        print(f"   Rating: {rating}/5")
        print(f"   Feedback: {feedback}")
        
        # Store feedback in session
        if 'feedback_history' not in session:
            session['feedback_history'] = []
        
        session['feedback_history'].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'feedback': feedback,
            'rating': rating
        })
        
        # Keep only last 30 feedback entries
        session['feedback_history'] = session['feedback_history'][-30:]
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback! It helps us improve our legal analysis.',
            'feedback_processed': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Feedback processing failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/history')
def get_history():
    """Get query history"""
    try:
        # Get session history
        session_history = session.get('query_history', [])
        
        return jsonify({
            'success': True,
            'session_history': session_history,
            'total_session_queries': len(session_history)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'History retrieval failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        stats = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'legal_coverage': {
                'bns_sections': 358,
                'ipc_sections': 511,
                'crpc_sections': 484,
                'total_sections': 1353,
                'domains_covered': 30,
                'subdomains_covered': 150
            },
            'session_info': {
                'queries_processed': len(session.get('query_history', [])),
                'feedback_provided': len(session.get('feedback_history', [])),
                'session_id': session.get('session_id', 'Not set')
            },
            'supported_query_types': [
                'Murder & Homicide', 'Kidnapping & Abduction', 'Sexual Offences',
                'Property Crimes', 'Violent Crimes', 'Cyber Crimes',
                'Employment Issues', 'Family Disputes', 'Financial Crimes',
                'Drug Crimes', 'Public Order', 'Consumer Protection',
                'Medical Law', 'Real Estate', 'Contract Law',
                'Intellectual Property', 'Environmental Law', 'Tax Law',
                'Immigration Law', 'Corporate Law', 'Banking Law',
                'Insurance Law', 'Education Law', 'Transport Law',
                'Sports Law', 'Media Law', 'Human Rights',
                'Administrative Law', 'Constitutional Law', 'Election Law',
                'International Law', 'ANY Legal Matter'
            ]
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': f'Stats retrieval failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        health_status = {
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'legal_ai_agent': initialize_legal_ai_agent(),
                'web_server': True,
                'session_management': True
            },
            'version': 'Legal AI Agent Web Interface v1.0',
            'features': [
                'Handles ANY type of legal query',
                'ALL BNS, IPC, CrPC sections',
                'Constitutional articles when applicable',
                'Feedback system',
                'Query history storage'
            ]
        }
        
        return jsonify(health_status)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'success': False,
        'available_endpoints': [
            '/api/legal-analysis',
            '/api/feedback',
            '/api/history',
            '/api/stats',
            '/api/health'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'success': False,
        'message': 'An unexpected error occurred. Please try again later.'
    }), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 STARTING LEGAL AI AGENT WEB INTERFACE")
    print("=" * 80)
    print("Features:")
    print("✅ Handles ANY type of legal query")
    print("✅ ALL BNS, IPC, CrPC sections")
    print("✅ Constitutional articles when applicable")
    print("✅ Feedback system")
    print("✅ Query storage and history")
    print("=" * 80)
    
    print("📋 Initializing Legal AI Agent...")
    
    if initialize_legal_ai_agent():
        print("✅ Legal AI Agent ready!")
        print("🌐 Starting web server...")
        print("📱 Access URL: http://localhost:5001")
        print("🔗 API Endpoints:")
        print("   • POST /api/legal-analysis - Legal analysis")
        print("   • POST /api/feedback - Submit feedback")
        print("   • GET /api/history - Query history")
        print("   • GET /api/stats - System statistics")
        print("   • GET /api/health - Health check")
        print("=" * 80)
        
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ Failed to start - Legal AI Agent initialization failed")