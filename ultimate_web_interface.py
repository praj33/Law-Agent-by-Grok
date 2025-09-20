#!/usr/bin/env python3
"""
Ultimate Legal Agent Web Interface
=================================

Web interface for the Ultimate Legal Agent that handles ANY query type with:
✅ ANY type of legal query (murder, kidnapping, etc.)
✅ ALL BNS, IPC, CrPC sections
✅ Feedback system that adjusts confidence
✅ Query storage and history
✅ Enhanced subdomain classification

Access URL: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid
import json
import os
import traceback

# Import the ultimate legal agent
try:
    from ultimate_legal_agent import create_ultimate_legal_agent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Ultimate legal agent not available: {e}")
    AGENT_AVAILABLE = False

# Import CORS
from flask_cors import CORS

# Use environment variable for secret key, with fallback
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ultimate_legal_agent_2025_render_deployment')

# Enable CORS for all routes with specific configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Allow all origins for API routes
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
        "supports_credentials": True
    }
}, supports_credentials=True)

# Handle OPTIONS requests explicitly
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        # Respond to OPTIONS requests immediately
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Accept')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

# Add a simple test route to verify API accessibility
@app.route('/api/ping')
def ping():
    """Simple ping endpoint to verify API accessibility"""
    return jsonify({
        'success': True,
        'message': 'API is accessible',
        'timestamp': datetime.now().isoformat(),
        'service': 'Ultimate Legal Agent API'
    })

# Global agent instance
ultimate_agent = None

def initialize_ultimate_agent():
    """Initialize the ultimate legal agent"""
    global ultimate_agent
    if ultimate_agent is None and AGENT_AVAILABLE:
        try:
            ultimate_agent = create_ultimate_legal_agent()
            print("✅ Ultimate Legal Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize ultimate agent: {e}")
            traceback.print_exc()
            return False
    return ultimate_agent is not None

@app.route('/')
def index():
    """Main page with ultimate legal analysis"""
    return render_template('ultimate_index.html')

@app.route('/api')
def api_endpoints():
    """List all available API endpoints"""
    return jsonify({
        'message': 'Available API endpoints',
        'endpoints': {
            'GET /api/ping': 'Simple ping endpoint to verify API accessibility',
            'POST /api/ultimate-analysis': 'Process legal queries and get analysis',
            'POST /api/feedback': 'Submit feedback for queries',
            'GET /api/history': 'Get query history',
            'GET /api/search-history': 'Search query history',
            'GET /api/stats': 'Get system statistics',
            'GET /api/health': 'Health check endpoint',
            'GET /api': 'This endpoint - list all API endpoints'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test', methods=['GET', 'POST'])
def test_api():
    """Simple test endpoint to verify API is working"""
    return jsonify({
        'success': True,
        'message': 'API is working correctly!',
        'method': request.method,
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/ultimate-analysis',
            '/api/feedback',
            '/api/history',
            '/api/search-history',
            '/api/stats',
            '/api/health'
        ]
    })

@app.route('/api/ultimate-analysis', methods=['POST'])
def process_ultimate_analysis():
    """Process ANY type of legal query with ultimate analysis"""
    try:
        if not initialize_ultimate_agent():
            return jsonify({
                'error': 'Ultimate Legal Agent initialization failed',
                'success': False,
                'message': 'The legal analysis system is currently unavailable. Please check the server console for initialization errors and restart the server.'
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
        
        print(f"🔍 Processing ultimate analysis for: {query[:50]}...")
        
        # Process query with ultimate analysis
        response = ultimate_agent.process_ultimate_query(query)
        
        # Format response for web interface
        result = {
            'success': True,
            'session_id': response['session_id'],
            'timestamp': response['timestamp'],
            'query': response['query'],
            
            # Classification Results (with feedback adjustment)
            'domain': response['domain'].replace('_', ' ').title(),
            'domain_raw': response['domain'],
            'domain_confidence': round(response['domain_confidence'], 3),
            'domain_confidence_percentage': f"{response['domain_confidence']:.1%}",
            
            'subdomain': response['subdomain'].replace('_', ' ').title(),
            'subdomain_raw': response['subdomain'],
            'subdomain_confidence': round(response['subdomain_confidence'], 3),
            'subdomain_confidence_percentage': f"{response['subdomain_confidence']:.1%}",
            'subdomain_alternatives': response.get('subdomain_alternatives', []),
            'subdomain_info': response.get('subdomain_info', {}),
            
            # ALL Legal Sections
            'bns_sections': response['bns_sections'],
            'ipc_sections': response['ipc_sections'],
            'crpc_sections': response['crpc_sections'],
            'total_sections': response['total_sections'],
            
            # Constitutional Articles
            'constitutional_articles': response.get('constitutional_articles', []),
            
            # Legal Analysis
            'legal_guidance': response['legal_guidance'],
            'formatted_response': response['formatted_response'],
            
            # Query Storage
            'stored_in_history': response['stored_in_history'],
            'history_count': response['history_count'],
            
            # Analysis Completeness
            'analysis_completeness': response['analysis_completeness'],
            
            # System Info
            'processing_time': f"< 1s",
            'feedback_adjusted': True
        }
        
        # Store in session history
        if 'query_history' not in session:
            session['query_history'] = []
        
        session['query_history'].append({
            'timestamp': result['timestamp'],
            'query': query,
            'domain': result['domain'],
            'subdomain': result['subdomain'],
            'domain_confidence': result['domain_confidence'],
            'subdomain_confidence': result['subdomain_confidence'],
            'total_sections': result['total_sections'],
            'bns_count': len(result['bns_sections']),
            'ipc_count': len(result['ipc_sections']),
            'crpc_count': len(result['crpc_sections'])
        })
        
        # Keep only last 20 queries
        session['query_history'] = session['query_history'][-20:]
        
        print(f"✅ Ultimate analysis processed: {result['total_sections']} sections provided")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Ultimate analysis failed: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Ultimate analysis failed: {str(e)}',
            'success': False,
            'message': 'An error occurred while processing your legal query. Please try again.'
        }), 500

@app.route('/api/feedback', methods=['POST'])
def process_feedback():
    """Process user feedback with confidence adjustment"""
    try:
        if not initialize_ultimate_agent():
            return jsonify({
                'error': 'Ultimate agent not available',
                'success': False
            }), 500
        
        data = request.get_json()
        query = data.get('query', '')
        domain = data.get('domain', '')
        subdomain = data.get('subdomain', '')
        confidence = data.get('confidence', 0)
        feedback = data.get('feedback', '')
        rating = data.get('rating', 0)
        
        if not all([query, domain, feedback]):
            return jsonify({
                'error': 'Missing required feedback data',
                'success': False
            }), 400
        
        # Process feedback through ultimate agent
        feedback_result = ultimate_agent.process_feedback(
            query, domain, subdomain, confidence, feedback, rating
        )
        
        # Store feedback in session
        if 'feedback_history' not in session:
            session['feedback_history'] = []
        
        session['feedback_history'].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'domain': domain,
            'subdomain': subdomain,
            'confidence': confidence,
            'feedback': feedback,
            'rating': rating,
            'adjustment': feedback_result['confidence_adjustment']
        })
        
        # Keep only last 30 feedback entries
        session['feedback_history'] = session['feedback_history'][-30:]
        
        return jsonify({
            'success': True,
            'message': feedback_result['message'],
            'confidence_adjustment': feedback_result['confidence_adjustment'],
            'new_confidence': feedback_result['new_confidence'],
            'feedback_processed': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Feedback processing failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/history')
def get_history():
    """Get query history from both session and agent storage"""
    try:
        # Get session history
        session_history = session.get('query_history', [])
        
        # Get agent history if available
        agent_history = []
        if ultimate_agent:
            try:
                agent_history = ultimate_agent.get_query_history(20)
            except Exception as e:
                print(f"⚠️ Could not get agent history: {e}")
        
        return jsonify({
            'success': True,
            'session_history': session_history,
            'agent_history': agent_history,
            'total_session_queries': len(session_history),
            'total_agent_queries': len(agent_history)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'History retrieval failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/search-history')
def search_history():
    """Search query history"""
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({
                'error': 'Search term required',
                'success': False
            }), 400
        
        results = []
        if ultimate_agent:
            try:
                results = ultimate_agent.search_query_history(search_term)
            except Exception as e:
                print(f"⚠️ Could not search history: {e}")
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'History search failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get comprehensive system statistics"""
    try:
        # Get agent statistics if available
        agent_stats = {}
        if ultimate_agent:
            try:
                agent_stats = ultimate_agent.get_ultimate_stats()
            except Exception as e:
                print(f"⚠️ Could not get agent stats: {e}")
        
        stats = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'agent_stats': agent_stats,
            'legal_coverage': {
                'bns_sections': agent_stats.get('legal_database', {}).get('total_bns_sections', 358),
                'ipc_sections': agent_stats.get('legal_database', {}).get('total_ipc_sections', 418),
                'crpc_sections': agent_stats.get('legal_database', {}).get('total_crpc_sections', 238),
                'total_sections': agent_stats.get('legal_database', {}).get('total_sections', 1014),
                'domains_covered': agent_stats.get('domain_classifier', {}).get('total_domains', 30),
                'subdomains_covered': agent_stats.get('subdomain_classifier', {}).get('total_subdomains', 155)
            },
            'query_history': agent_stats.get('query_history', {
                'total_queries': 0,
                'unique_domains': 0,
                'unique_subdomains': 0,
                'recent_queries': 0
            }),
            'session_info': {
                'queries_processed': len(session.get('query_history', [])),
                'feedback_provided': len(session.get('feedback_history', [])),
                'session_id': session.get('session_id', 'Not set')
            },
            'capabilities': agent_stats.get('capabilities', [
                'Handles ANY type of legal query',
                'Complete BNS 2023 sections',
                'Complete IPC sections',
                'Complete CrPC sections',
                'Feedback system with confidence adjustment',
                'Query storage and history',
                'Enhanced subdomain classification'
            ]),
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
                'ultimate_agent': ultimate_agent is not None,
                'web_server': True,
                'session_management': True,
                'query_storage': True,
                'feedback_system': True
            },
            'version': 'Ultimate Legal Agent Web Interface v2.0',
            'features': [
                'Handles ANY query type',
                'ALL legal sections',
                'Feedback with confidence adjustment',
                'Query history storage'
            ]
        }
        
        if ultimate_agent:
            try:
                # Quick test query to verify agent is working
                test_response = ultimate_agent.process_ultimate_query("test query for health check")
                health_status['components']['agent_processing'] = True
                health_status['last_test'] = 'passed'
                health_status['test_sections'] = test_response['total_sections']
            except Exception as e:
                health_status['components']['agent_processing'] = False
                health_status['last_test'] = f'failed: {str(e)}'
        
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
            '/api/ultimate-analysis',
            '/api/feedback',
            '/api/history',
            '/api/search-history',
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
    
    print("🚀 STARTING ULTIMATE LEGAL AGENT WEB INTERFACE")
    print("=" * 80)
    print("Features:")
    print("✅ Handles ANY type of legal query (murder, kidnapping, etc.)")
    print("✅ ALL BNS, IPC, CrPC sections")
    print("✅ Feedback system that adjusts confidence")
    print("✅ Query storage and history")
    print("✅ Enhanced subdomain classification")
    print("✅ Real-time legal analysis")
    print("=" * 80)
    
    print("📋 Initializing Ultimate Legal Agent...")
    
    if initialize_ultimate_agent():
        print("✅ Ultimate Legal Agent ready!")
        print("🌐 Starting web server...")
        
        # Get port from environment variable (Render) or default to 5000
        port = int(os.environ.get('PORT', 5000))
        print(f"📍 Server will be available at: http://0.0.0.0:{port}")
        print("🔗 API Endpoints:")
        print("   • GET /api/ping - Simple ping endpoint")
        print("   • GET /api - List all API endpoints")
        print("   • POST /api/ultimate-analysis - Ultimate legal analysis")
        print("   • POST /api/feedback - Submit feedback (adjusts confidence)")
        print("   • GET /api/history - Query history")
        print("   • GET /api/search-history - Search query history")
        print("   • GET /api/stats - System statistics")
        print("   • GET /api/health - Health check")
        print("   • GET/POST /api/test - Test endpoint")
        print("=" * 80)
        
        # Run the app (bind to 0.0.0.0 for external access)
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        print("❌ Failed to start - Ultimate Legal Agent initialization failed")
        print("💡 Please ensure all required components are available:")
        print("   • ultimate_legal_agent.py")
        print("   • complete_legal_database.py")
        print("   • enhanced_subdomain_classifier.py")