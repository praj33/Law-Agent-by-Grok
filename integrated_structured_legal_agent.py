"""
Integrated Structured Legal Agent - Complete System
==================================================

This module integrates the existing legal agent with the new structured response format.
It provides both the original comprehensive response and the new structured format:

1. Constitutional Articles
2. IPC Sections (Indian Penal Code, 1860)  
3. CrPC Sections (Code of Criminal Procedure, 1973)
4. Special Acts (if applicable)

Author: Legal Agent Team
Version: 3.0.0 - Integrated Structured Response
Date: 2025-01-XX
"""

import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Import existing components
from legal_agent import LegalAgent, LegalQueryInput, LegalAgentResponse, create_legal_agent
from enhanced_structured_legal_agent import EnhancedStructuredLegalAgent, StructuredLegalResponse, create_structured_legal_agent

@dataclass
class IntegratedLegalResponse:
    """Integrated response containing both original and structured formats"""
    
    # Original comprehensive response
    original_response: LegalAgentResponse
    
    # New structured response
    structured_response: StructuredLegalResponse
    
    # Integration metadata
    integration_timestamp: str
    response_format: str = "integrated"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "original_response": self.original_response.to_dict(),
            "structured_response": asdict(self.structured_response),
            "integration_timestamp": self.integration_timestamp,
            "response_format": self.response_format
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def get_original_formatted(self) -> str:
        """Get original formatted response"""
        return self._format_original_response()
    
    def get_structured_formatted(self) -> str:
        """Get structured formatted response"""
        return self.structured_response.to_formatted_response()
    
    def get_combined_formatted(self) -> str:
        """Get combined formatted response with both formats"""
        parts = []
        
        parts.append("=" * 80)
        parts.append("⚖️ COMPREHENSIVE LEGAL AI ASSISTANT - INTEGRATED RESPONSE")
        parts.append("=" * 80)
        parts.append("")
        
        # Structured Response Section
        parts.append("📋 STRUCTURED LEGAL ANALYSIS")
        parts.append("=" * 40)
        parts.append(self.get_structured_formatted())
        parts.append("")
        
        # Original Comprehensive Response Section
        parts.append("📊 COMPREHENSIVE LEGAL GUIDANCE")
        parts.append("=" * 40)
        parts.append(self.get_original_formatted())
        
        parts.append("=" * 80)
        parts.append(f"Integration Timestamp: {self.integration_timestamp}")
        parts.append("⚖️ This response combines structured legal provisions with comprehensive guidance")
        parts.append("=" * 80)
        
        return "\n".join(parts)
    
    def _format_original_response(self) -> str:
        """Format the original response for display"""
        resp = self.original_response
        parts = []
        
        parts.append(f"🎯 DOMAIN CLASSIFICATION:")
        parts.append(f"   Domain: {resp.domain.title()}")
        parts.append(f"   Confidence: {resp.confidence:.2f}")
        parts.append("")
        
        parts.append(f"⚖️ LEGAL ROUTE:")
        parts.append(f"   {resp.legal_route}")
        parts.append("")
        
        parts.append(f"⏰ TIMELINE:")
        parts.append(f"   {resp.timeline}")
        parts.append("")
        
        parts.append(f"🎯 EXPECTED OUTCOME:")
        parts.append(f"   {resp.outcome}")
        parts.append("")
        
        if resp.process_steps:
            parts.append(f"📋 PROCESS STEPS:")
            for step in resp.process_steps:
                parts.append(f"   {step}")
            parts.append("")
        
        if resp.constitutional_backing:
            parts.append(f"🏛️ CONSTITUTIONAL BACKING:")
            parts.append(f"   {resp.constitutional_backing}")
            parts.append("")
        
        if resp.glossary:
            parts.append(f"📚 LEGAL GLOSSARY:")
            for term, definition in list(resp.glossary.items())[:3]:
                parts.append(f"   • {term.title()}: {definition}")
            parts.append("")
        
        if resp.data_driven_advice:
            parts.append(f"📊 DATA-DRIVEN INSIGHTS:")
            parts.append(f"   {resp.data_driven_advice}")
            parts.append("")
        
        return "\n".join(parts)


class IntegratedStructuredLegalAgent:
    """Integrated Legal Agent providing both comprehensive and structured responses"""
    
    def __init__(self, feedback_file: str = 'feedback.csv'):
        """Initialize the integrated legal agent"""
        
        # Initialize both agents
        self.original_agent = create_legal_agent(feedback_file)
        self.structured_agent = create_structured_legal_agent()
        
        print("✅ Integrated Structured Legal Agent initialized")
        print("🔄 Both comprehensive and structured response formats available")
    
    def process_integrated_query(self, user_query: str, session_id: str = None) -> IntegratedLegalResponse:
        """Process query and return integrated response with both formats"""
        
        # Create query input for original agent
        query_input = LegalQueryInput(
            user_input=user_query,
            session_id=session_id
        )
        
        # Get original comprehensive response
        original_response = self.original_agent.process_query(query_input)
        
        # Get structured response
        structured_response = self.structured_agent.process_structured_query(
            user_query, 
            session_id or original_response.session_id
        )
        
        # Create integrated response
        integrated_response = IntegratedLegalResponse(
            original_response=original_response,
            structured_response=structured_response,
            integration_timestamp=datetime.datetime.now().isoformat()
        )
        
        return integrated_response
    
    def get_structured_only(self, user_query: str) -> str:
        """Get only structured response format"""
        response = self.structured_agent.get_formatted_response(user_query)
        return response
    
    def get_comprehensive_only(self, user_query: str) -> str:
        """Get only comprehensive response format"""
        query_input = LegalQueryInput(user_input=user_query)
        response = self.original_agent.process_query(query_input)
        return response.to_json()
    
    def get_combined_response(self, user_query: str) -> str:
        """Get combined formatted response"""
        integrated = self.process_integrated_query(user_query)
        return integrated.get_combined_formatted()
    
    def collect_feedback(self, query: str, feedback: str, session_id: str = None):
        """Collect feedback for both agents"""
        self.original_agent.feedback_system.collect_feedback(
            query, "integrated", feedback, session_id
        )
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        return self.original_agent.get_feedback_stats()


# Convenience functions
def create_integrated_legal_agent(feedback_file: str = 'feedback.csv') -> IntegratedStructuredLegalAgent:
    """Create and return integrated legal agent"""
    return IntegratedStructuredLegalAgent(feedback_file)


def get_structured_legal_response(user_query: str) -> str:
    """Quick function to get structured legal response"""
    agent = create_integrated_legal_agent()
    return agent.get_structured_only(user_query)


def get_comprehensive_legal_response(user_query: str) -> str:
    """Quick function to get comprehensive legal response"""
    agent = create_integrated_legal_agent()
    return agent.get_comprehensive_only(user_query)


def get_combined_legal_response(user_query: str) -> str:
    """Quick function to get combined legal response"""
    agent = create_integrated_legal_agent()
    return agent.get_combined_response(user_query)


# Test the integrated system
if __name__ == "__main__":
    print("🏛️ INTEGRATED STRUCTURED LEGAL AGENT TEST")
    print("=" * 60)
    
    # Create integrated agent
    agent = create_integrated_legal_agent()
    
    # Test query
    test_query = "My coworker is sexually harassing me at workplace and making inappropriate comments"
    
    print(f"\n📝 Test Query: \"{test_query}\"")
    print("=" * 60)
    
    # Test structured response only
    print(f"\n1️⃣ STRUCTURED RESPONSE ONLY:")
    print("-" * 40)
    structured_only = agent.get_structured_only(test_query)
    print(structured_only)
    
    input("\nPress Enter to see comprehensive response...")
    
    # Test comprehensive response only
    print(f"\n2️⃣ COMPREHENSIVE RESPONSE ONLY:")
    print("-" * 40)
    comprehensive_only = agent.get_comprehensive_only(test_query)
    print(comprehensive_only)
    
    input("\nPress Enter to see combined response...")
    
    # Test combined response
    print(f"\n3️⃣ COMBINED INTEGRATED RESPONSE:")
    print("-" * 40)
    combined = agent.get_combined_response(test_query)
    print(combined)
    
    print(f"\n✅ Integrated Structured Legal Agent is working perfectly!")
    print(f"🎊 All response formats are available and functional!")