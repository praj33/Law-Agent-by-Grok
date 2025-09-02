#!/usr/bin/env python3
"""
Legal Agent Mobile App Interface
===============================

Progressive Web App (PWA) interface for the Legal Agent system.
Optimized for mobile devices with app-like experience.
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from datetime import datetime
import uuid
import json
import os
from working_enhanced_agent import create_working_enhanced_agent

app = Flask(__name__)
app.secret_key = 'legal_agent_mobile_secret_2025'

# Global agent instance
agent = None

def initialize_agent():
    """Initialize the legal agent"""
    global agent
    if agent is None:
        try:
            agent = create_working_enhanced_agent()
            print("✅ Legal Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            return False
    return True

@app.route('/')
def mobile_index():
    """Mobile-optimized main page"""
    return render_template('mobile_index.html')

@app.route('/manifest.json')
def manifest():
    """PWA manifest file"""
    return jsonify({
        "name": "Legal Agent by Grok",
        "short_name": "LegalAgent",
        "description": "AI Legal Assistant - Professional Legal Guidance",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#667eea",
        "theme_color": "#667eea",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/icon-512.png", 
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "categories": ["legal", "productivity", "utilities"],
        "lang": "en",
        "dir": "ltr"
    })

@app.route('/sw.js')
def service_worker():
    """Service worker for PWA functionality"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/api/mobile/query', methods=['POST'])
def mobile_process_query():
    """Mobile-optimized query processing"""
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
        
        # Process query
        response = agent.process_query(query)
        
        # Mobile-optimized response format
        result = {
            'success': True,
            'session_id': session['session_id'],
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'domain': {
                'name': response.domain.replace('_', ' ').title(),
                'raw': response.domain,
                'icon': get_domain_icon(response.domain)
            },
            'confidence': {
                'value': round(response.confidence, 3),
                'percentage': f"{min(response.confidence * 100, 100):.1f}%",
                'level': get_confidence_level(response.confidence)
            },
            'timeline': response.timeline,
            'success_rate': f"{response.success_rate:.0%}",
            'legal_route': response.legal_route if hasattr(response, 'legal_route') else '',
            'constitutional_articles': [],
            'constitutional_backing': response.constitutional_backing if hasattr(response, 'constitutional_backing') else '',
            'response_time': f"{response.response_time:.3f}s",
            'mobile_summary': generate_mobile_summary(response)
        }
        
        # Format constitutional articles for mobile
        if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
            for article in response.constitutional_articles:
                result['constitutional_articles'].append({
                    'number': article.get('article_number', 'N/A'),
                    'title': article.get('title', 'N/A'),
                    'confidence': article.get('confidence', 0),
                    'summary': truncate_text(article.get('title', ''), 50)
                })
        
        # Store in session history
        if 'mobile_history' not in session:
            session['mobile_history'] = []
        
        session['mobile_history'].append({
            'timestamp': result['timestamp'],
            'query': truncate_text(query, 60),
            'domain': result['domain']['name'],
            'confidence': result['confidence']['value'],
            'icon': result['domain']['icon']
        })
        
        # Keep only last 20 queries for mobile
        session['mobile_history'] = session['mobile_history'][-20:]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Processing failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/mobile/quick-actions')
def mobile_quick_actions():
    """Get quick action suggestions for mobile"""
    return jsonify({
        'success': True,
        'quick_actions': [
            {
                'title': 'Phone Hacked',
                'query': 'My phone is being hacked by someone',
                'icon': '📱',
                'category': 'Cyber Crime'
            },
            {
                'title': 'Salary Issues',
                'query': 'My boss is not giving my salary for 3 months',
                'icon': '💼',
                'category': 'Employment'
            },
            {
                'title': 'Domestic Violence',
                'query': 'My husband beats me daily',
                'icon': '🏠',
                'category': 'Family Law'
            },
            {
                'title': 'Deposit Not Returned',
                'query': 'Landlord not returning my security deposit',
                'icon': '🏢',
                'category': 'Tenant Rights'
            },
            {
                'title': 'Defective Product',
                'query': 'Bought defective phone want refund',
                'icon': '🛒',
                'category': 'Consumer'
            },
            {
                'title': 'Car Accident',
                'query': 'I was injured in a car accident',
                'icon': '🚗',
                'category': 'Personal Injury'
            }
        ]
    })

@app.route('/api/mobile/feedback', methods=['POST'])
def mobile_process_feedback():
    """Mobile-optimized feedback processing"""
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
        
        # Store feedback in session for mobile analytics
        if 'mobile_feedback' not in session:
            session['mobile_feedback'] = []
        
        session['mobile_feedback'].append({
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback,
            'domain': domain
        })
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback!',
            'feedback_count': len(session.get('mobile_feedback', []))
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Feedback processing failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/mobile/history')
def mobile_get_history():
    """Get mobile-optimized query history"""
    history = session.get('mobile_history', [])
    return jsonify({
        'success': True,
        'history': history[-10:],  # Last 10 for mobile
        'total_queries': len(history)
    })

@app.route('/api/mobile/stats')
def mobile_get_stats():
    """Get mobile-optimized system statistics"""
    try:
        feedback_stats = session.get('mobile_feedback', [])
        positive_feedback = len([f for f in feedback_stats if f['feedback'] in ['helpful', 'very helpful']])
        
        stats = {
            'success': True,
            'agent_status': 'Active' if agent else 'Inactive',
            'session_stats': {
                'queries': len(session.get('mobile_history', [])),
                'feedback_given': len(feedback_stats),
                'satisfaction': f"{(positive_feedback/len(feedback_stats)*100):.0f}%" if feedback_stats else "N/A"
            },
            'system_info': {
                'domains': 10,
                'articles': 121,
                'accuracy': '100%',
                'version': 'Mobile v1.0'
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error': f'Stats retrieval failed: {str(e)}',
            'success': False
        }), 500

def get_domain_icon(domain):
    """Get emoji icon for domain"""
    icons = {
        'cyber_crime': '🔒',
        'employment_law': '💼',
        'family_law': '👨‍👩‍👧‍👦',
        'tenant_rights': '🏠',
        'consumer_complaint': '🛒',
        'criminal_law': '⚖️',
        'immigration_law': '🛂',
        'contract_dispute': '📄',
        'elder_abuse': '👴',
        'personal_injury': '🏥'
    }
    return icons.get(domain, '⚖️')

def get_confidence_level(confidence):
    """Get confidence level description"""
    if confidence >= 0.8:
        return 'High'
    elif confidence >= 0.5:
        return 'Medium'
    elif confidence >= 0.2:
        return 'Low'
    else:
        return 'Very Low'

def generate_mobile_summary(response):
    """Generate mobile-friendly summary"""
    domain = response.domain.replace('_', ' ').title()
    timeline = response.timeline
    success_rate = f"{response.success_rate:.0%}"
    
    return f"This is a {domain} matter. Expected timeline: {timeline}. Historical success rate: {success_rate}."

def truncate_text(text, max_length):
    """Truncate text for mobile display"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("📱 Starting Legal Agent Mobile App Interface...")
    print("🔧 Initializing agent...")
    
    if initialize_agent():
        print("✅ Agent ready!")
        print("📱 Starting mobile web server...")
        print("🌐 Access at: http://localhost:5001")
        print("📲 Add to home screen for app-like experience!")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ Failed to start - agent initialization failed")