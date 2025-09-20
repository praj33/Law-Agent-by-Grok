#!/usr/bin/env python3
"""
Simple Legal Agent Web Interface
===============================

A clean, simple, and extremely user-friendly web interface for legal guidance.
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid
import json
import os
import traceback

# Import the legal agent
try:
    from ultimate_legal_agent import create_ultimate_legal_agent
    AGENT_AVAILABLE = True
except ImportError:
    try:
        from ultimate_legal_agent import UltimateLegalAgent
        AGENT_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Legal agent not available: {e}")
        AGENT_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'simple_legal_agent_2025'

# Global agent instance
legal_agent = None

def initialize_agent():
    """Initialize the legal agent"""
    global legal_agent
    if legal_agent is None and AGENT_AVAILABLE:
        try:
            if 'create_ultimate_legal_agent' in globals():
                legal_agent = create_ultimate_legal_agent()
            else:
                legal_agent = UltimateLegalAgent()
            print("✅ Legal Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            traceback.print_exc()
            return False
    return legal_agent is not None

@app.route('/')
def index():
    """Main page"""
    return render_template('simple_index.html')

@app.route('/api/ask', methods=['POST'])
def ask_legal_question():
    """Process legal questions"""
    try:
        if not initialize_agent():
            return jsonify({
                'error': 'Legal system unavailable',
                'success': False,
                'message': 'The legal guidance system is currently unavailable. Please try again later.'
            }), 500
        
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Question cannot be empty',
                'success': False,
                'message': 'Please enter a legal question to get guidance.'
            }), 400
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        print(f"🔍 Processing question: {question[:50]}...")
        
        # Process question with legal agent
        if hasattr(legal_agent, 'process_ultimate_query'):
            response = legal_agent.process_ultimate_query(question)
        else:
            # Fallback method name
            response = legal_agent.process_query(question)
        
        # Simplify response for easy understanding
        simplified_response = {
            'success': True,
            'question': question,
            'answer': response.get('formatted_response', ''),
            
            # Classification (simplified)
            'type': response.get('domain', 'General Legal').replace('_', ' ').title(),
            'specific_area': response.get('subdomain', 'General').replace('_', ' ').title(),
            'confidence': f"{response.get('domain_confidence', 0.5):.0%}",
            
            # Legal sections (simplified)
            'total_laws': response.get('total_sections', 0),
            'bns_count': len(response.get('bns_sections', [])),
            'ipc_count': len(response.get('ipc_sections', [])),
            'crpc_count': len(response.get('crpc_sections', [])),
            
            # Detailed sections for display
            'bns_sections': response.get('bns_sections', []),
            'ipc_sections': response.get('ipc_sections', []),
            'crpc_sections': response.get('crpc_sections', []),
            'legal_guidance': response.get('legal_guidance', {}),
            
            'timestamp': datetime.now().strftime('%I:%M %p'),
            'session_id': session['session_id']
        }
        
        # Store in session history (keep last 10)
        if 'history' not in session:
            session['history'] = []
        
        session['history'].append({
            'question': question,
            'type': simplified_response['type'],
            'confidence': simplified_response['confidence'],
            'timestamp': simplified_response['timestamp'],
            'total_laws': simplified_response['total_laws']
        })
        
        # Keep only last 10 questions
        session['history'] = session['history'][-10:]
        
        print(f"✅ Question processed successfully")
        
        return jsonify(simplified_response)
        
    except Exception as e:
        print(f"❌ Failed to process question: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Processing failed: {str(e)}',
            'success': False,
            'message': 'An error occurred while processing your question. Please try again.'
        }), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        rating = data.get('rating', 0)
        comment = data.get('comment', '').strip()
        
        # Store feedback in session
        if 'feedback' not in session:
            session['feedback'] = []
        
        session['feedback'].append({
            'rating': rating,
            'comment': comment,
            'timestamp': datetime.now().strftime('%I:%M %p')
        })
        
        # Keep only last 20 feedback entries
        session['feedback'] = session['feedback'][-20:]
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback! It helps us improve our service.'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Feedback submission failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/history')
def get_history():
    """Get question history"""
    try:
        history = session.get('history', [])
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
    except Exception as e:
        return jsonify({
            'error': f'History retrieval failed: {str(e)}',
            'success': False
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Page not found',
        'success': False
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
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 STARTING SIMPLE LEGAL AGENT WEB INTERFACE")
    print("=" * 60)
    print("✅ Clean and simple design")
    print("✅ Easy to use interface")
    print("✅ Complete legal guidance")
    print("✅ No complex features - just what you need")
    print("=" * 60)
    
    if initialize_agent():
        print("✅ Legal Agent ready!")
        print("🌐 Starting web server...")
        print("📱 Access URL: http://localhost:5000")
        print("=" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to start - Legal Agent initialization failed")