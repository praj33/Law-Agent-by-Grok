"""
Web Interface for Query Classification System
============================================

This module provides a web interface for the query classification system
using Flask.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_classification_system import create_query_classification_system, format_classification_result


# Create Flask app
app = Flask(__name__, template_folder='templates')

# Initialize the classification system
classification_system = create_query_classification_system()


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('ultimate_index.html')


@app.route('/classify', methods=['POST'])
def classify_query():
    """Classify a legal query"""
    try:
        # Get the query from the request
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Classify the query
        result = classification_system.classify_query(user_query)
        
        # Format the result
        formatted_result = format_classification_result(result)
        
        # Return the result
        return jsonify({
            'success': True,
            'result': formatted_result,
            'session_id': result.session_id,
            'domain': result.domain,
            'subdomain': result.subdomain,
            'confidence': result.confidence_percentage
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ultimate-analysis', methods=['POST'])
def ultimate_analysis():
    """Provide ultimate analysis in the format expected by ultimate_index.html"""
    try:
        # Get the query from the request
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Classify the query
        result = classification_system.classify_query(user_query)
        
        # Prepare response in the format expected by the frontend
        response = {
            'success': True,
            'query': user_query,
            'domain': result.domain.replace('_', ' ').title(),
            'subdomain': result.subdomain.replace('_', ' ').title(),
            'domain_raw': result.domain,
            'subdomain_raw': result.subdomain,
            'domain_confidence': result.confidence,
            'subdomain_confidence': result.confidence,
            'domain_confidence_percentage': f"{result.confidence_percentage}%",
            'subdomain_confidence_percentage': f"{result.confidence_percentage}%",
            'total_sections': len(result.bns_sections) + len(result.ipc_sections) + len(result.crpc_sections),
            'bns_sections': result.bns_sections,
            'ipc_sections': result.ipc_sections,
            'crpc_sections': result.crpc_sections,
            'constitutional_articles': [
                {
                    'article_number': article.get('article_number', ''),
                    'title': article.get('title', ''),
                    'description': article.get('content_preview', article.get('description', '')),
                    'confidence_percentage': article.get('confidence_percentage', 0),
                    'matching_keywords': article.get('matching_keywords', [])
                }
                for article in result.constitutional_articles
            ],
            'legal_guidance': {
                'legal_procedures': result.legal_process,
                'required_documents': result.notes_and_safeguards,
                'immediate_actions': result.emergency_contacts,
                'timeline': 'Depends on case complexity and court schedule',
                'cost_estimates': 'Varies based on legal representation and case complexity'
            },
            'feedback_adjusted': False,
            'session_id': result.session_id,
            'timestamp': result.timestamp
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Handle feedback submission"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', '')
        feedback = data.get('feedback', '')
        rating = data.get('rating', 0)
        
        # Process feedback (in a real implementation, this would update confidence scores)
        success = classification_system.process_feedback(session_id, feedback, rating)
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully',
            'confidence_adjustment': 0.05 if rating >= 4 else (-0.05 if rating <= 2 else 0)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history')
def get_history():
    """Get query history"""
    try:
        history = classification_system.get_query_history(limit=10)
        
        # Format history for the frontend
        formatted_history = []
        for item in history:
            formatted_history.append({
                'query': item['user_query'],
                'domain': item['domain'].replace('_', ' ').title(),
                'subdomain': 'N/A',  # Subdomain not stored in current implementation
                'total_sections': 0,  # Not stored in current implementation
                'timestamp': item['timestamp']
            })
        
        return jsonify({
            'success': True,
            'session_history': formatted_history
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        stats = classification_system.get_system_stats()
        
        # Format stats for the frontend
        legal_coverage = {
            'bns_sections': stats.get('legal_database_stats', {}).get('total_bns_sections', 358),
            'ipc_sections': stats.get('legal_database_stats', {}).get('total_ipc_sections', 418),
            'crpc_sections': stats.get('legal_database_stats', {}).get('total_crpc_sections', 238),
            'domains_covered': stats.get('subdomain_classifier_stats', {}).get('total_domains', 10),
            'subdomains_covered': stats.get('subdomain_classifier_stats', {}).get('total_subdomains', 85)
        }
        
        session_info = {
            'queries_processed': stats.get('queries_processed', 0)
        }
        
        return jsonify({
            'success': True,
            'legal_coverage': legal_coverage,
            'session_info': session_info
        })
    except Exception as e:
        # Return fallback stats
        return jsonify({
            'success': True,
            'legal_coverage': {
                'bns_sections': 358,
                'ipc_sections': 418,
                'crpc_sections': 238,
                'domains_covered': 10,
                'subdomains_covered': 85
            },
            'session_info': {
                'queries_processed': 0
            }
        })


if __name__ == '__main__':
    print("🚀 Starting Query Classification Web Interface...")
    print("Open your browser to http://localhost:5000")
    app.run(host='localhost', port=5000, debug=True)