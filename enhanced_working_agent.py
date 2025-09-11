#!/usr/bin/env python3
"""
Enhanced Working Agent with Detailed Legal Provisions
====================================================

Integrates the enhanced legal provisions engine with the main agent system
to provide comprehensive legal analysis with IPC sections, CrPC sections,
and detailed legal processes.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

# Import existing components
from working_enhanced_agent import create_working_enhanced_agent
from enhanced_legal_provisions import EnhancedLegalProvisionsEngine
from confidence_booster import apply_confidence_boost
from subdomain_classifier import create_subdomain_classifier

class EnhancedWorkingAgent:
    """Enhanced working agent with detailed legal provisions"""
    
    def __init__(self):
        """Initialize the enhanced working agent"""
        print("Initializing Enhanced Working Agent with Detailed Legal Provisions...")
        
        # Initialize base agent
        self.base_agent = create_working_enhanced_agent()
        print("✅ Base agent initialized")
        
        # Initialize enhanced legal provisions engine
        self.legal_provisions_engine = EnhancedLegalProvisionsEngine()
        print("✅ Enhanced legal provisions engine initialized")
        
        print("🎉 Enhanced Working Agent ready!")
    
    def process_query_with_enhanced_provisions(self, query: str) -> Dict[str, Any]:
        """Process query with enhanced legal provisions"""
        
        # Generate unique session ID
        session_id = f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        print(f"\nProcessing enhanced query {session_id}: {query[:50]}...")
        
        # Get base response from original agent
        base_response = self.base_agent.process_query(query)
        
        # Get enhanced legal analysis
        enhanced_analysis = self.legal_provisions_engine.get_enhanced_legal_analysis(
            base_response.domain, 
            query, 
            base_response.confidence
        )
        
        # Format enhanced response
        enhanced_formatted = self.legal_provisions_engine.format_enhanced_response(enhanced_analysis)
        
        # Combine all information
        enhanced_response = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "domain": base_response.domain,
            "confidence": base_response.confidence,
            "timeline": base_response.timeline,
            "success_rate": base_response.success_rate,
            "response_time": base_response.response_time,
            
            # Enhanced provisions
            "enhanced_analysis": enhanced_analysis,
            "formatted_response": enhanced_formatted,
            
            # Original components (for compatibility)
            "legal_route": base_response.legal_route if hasattr(base_response, 'legal_route') else '',
            "constitutional_articles": base_response.constitutional_articles if hasattr(base_response, 'constitutional_articles') else [],
            "constitutional_backing": base_response.constitutional_backing if hasattr(base_response, 'constitutional_backing') else ''
        }
        
        print(f"Enhanced query processed in {base_response.response_time:.3f}s")
        return enhanced_response
    
    def display_enhanced_response(self, response: Dict[str, Any]) -> None:
        """Display the enhanced response in a formatted way"""
        
        print("\n" + "="*80)
        print("🏛️ ENHANCED LEGAL ANALYSIS")
        print("="*80)
        print()
        
        # Display the formatted enhanced response
        print(response["formatted_response"])
        
        print("\n" + "="*80)
        print(f"📊 Session: {response['session_id']}")
        print(f"⚡ Response Time: {response['response_time']:.3f}s")
        print(f"🕐 Timestamp: {datetime.fromisoformat(response['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def process_feedback(self, query: str, domain: str, confidence: float, feedback: str) -> bool:
        """Process user feedback (delegates to base agent)"""
        if hasattr(self.base_agent, 'process_feedback'):
            return self.base_agent.process_feedback(query, domain, confidence, feedback)
        return True

def create_enhanced_working_agent():
    """Factory function to create enhanced working agent"""
    return EnhancedWorkingAgent()

def main():
    """Main function for testing the enhanced agent"""
    
    print("🎉 ENHANCED WORKING AGENT - DETAILED LEGAL PROVISIONS")
    print("=" * 65)
    print("This agent provides comprehensive legal analysis with:")
    print("✅ IPC Sections with detailed descriptions")
    print("✅ CrPC Sections for procedural guidance")
    print("✅ Constitutional Articles with relevance")
    print("✅ Step-by-step legal processes")
    print("✅ Timeline and success rate analysis")
    print("✅ Emergency contacts and important notes")
    print()
    
    # Create enhanced agent
    try:
        agent = create_enhanced_working_agent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Test queries
    test_queries = [
        "My phone is stolen",
        "My phone is being hacked by someone",
        "My boss is not giving my salary for 3 months",
        "My husband beats me daily",
        "Landlord not returning my security deposit",
        "I bought a defective phone and want refund"
    ]
    
    print("🧪 TESTING ENHANCED AGENT WITH SAMPLE QUERIES")
    print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📋 TEST {i}: {query}")
        print("-" * 30)
        
        try:
            # Process query with enhanced provisions
            response = agent.process_query_with_enhanced_provisions(query)
            
            # Display enhanced response
            agent.display_enhanced_response(response)
            
            # Wait for user input to continue (except for last query)
            if i < len(test_queries):
                input(f"\n⏸️  Press Enter to continue to test {i+1}...")
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            continue
    
    print("\n🎉 ENHANCED AGENT TESTING COMPLETE!")
    print("✅ All queries processed with detailed legal provisions")
    print("📚 The agent now provides comprehensive legal analysis")
    print("🚀 Ready for production use with enhanced capabilities!")

if __name__ == "__main__":
    main()