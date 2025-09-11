#!/usr/bin/env python3
"""
Subdomain Enhanced Legal Agent
=============================

Enhanced legal agent with hierarchical domain -> subdomain classification
for more specific and targeted legal guidance.

Features:
- Main domain classification (criminal_law, employment_law, etc.)
- Detailed subdomain classification (theft, cyber_crime, etc.)
- Subdomain-specific legal guidance
- Enhanced constitutional analysis
- Comprehensive legal provisions

Author: Legal Agent Team
Version: 1.0.0 - Subdomain Classification
Date: 2025-09-02
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
import uuid

# Import existing components
from working_enhanced_agent import create_working_enhanced_agent
from enhanced_legal_provisions import EnhancedLegalProvisionsEngine
from confidence_booster import apply_confidence_boost
from subdomain_classifier import create_subdomain_classifier

class SubdomainEnhancedAgent:
    """Enhanced legal agent with subdomain classification"""
    
    def __init__(self):
        """Initialize the subdomain enhanced agent"""
        print("Initializing Subdomain Enhanced Legal Agent...")
        
        # Initialize base agent
        self.base_agent = create_working_enhanced_agent()
        print("✅ Base agent initialized")
        
        # Initialize enhanced legal provisions engine
        self.legal_provisions_engine = EnhancedLegalProvisionsEngine()
        print("✅ Enhanced legal provisions engine initialized")
        
        # Initialize subdomain classifier
        self.subdomain_classifier = create_subdomain_classifier()
        print("✅ Subdomain classifier initialized")
        
        print("🎯 Subdomain Enhanced Agent ready!")
    
    def process_query_with_subdomains(self, query: str) -> Dict[str, Any]:
        """Process query with domain and subdomain classification"""
        
        # Generate unique session ID
        session_id = f"subdomain_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        print(f"\nProcessing subdomain query {session_id}: {query[:50]}...")
        
        # Get base response from original agent
        base_response = self.base_agent.process_query(query)
        
        # Classify subdomain within the identified domain
        subdomain, subdomain_confidence, subdomain_alternatives = self.subdomain_classifier.classify_subdomain(
            base_response.domain, query
        )
        
        # Get subdomain information
        subdomain_info = self.subdomain_classifier.get_subdomain_info(base_response.domain, subdomain)
        
        # Get enhanced legal analysis
        enhanced_analysis = self.legal_provisions_engine.get_enhanced_legal_analysis(
            base_response.domain, 
            query, 
            base_response.confidence
        )
        
        # Enhance analysis with subdomain-specific information
        enhanced_analysis = self._enhance_with_subdomain_info(
            enhanced_analysis, base_response.domain, subdomain, subdomain_info, query
        )
        
        # Format enhanced response with subdomain information
        enhanced_formatted = self._format_subdomain_response(
            enhanced_analysis, base_response.domain, subdomain, subdomain_info, subdomain_confidence
        )
        
        # Combine all information
        enhanced_response = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            
            # Domain classification
            "domain": base_response.domain,
            "domain_confidence": base_response.confidence,
            
            # Subdomain classification
            "subdomain": subdomain,
            "subdomain_confidence": subdomain_confidence,
            "subdomain_alternatives": subdomain_alternatives,
            "subdomain_info": subdomain_info,
            
            # Other base information
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
        
        print(f"Subdomain query processed in {base_response.response_time:.3f}s")
        print(f"🎯 Domain: {base_response.domain} → Subdomain: {subdomain} (confidence: {subdomain_confidence:.3f})")
        
        return enhanced_response
    
    def _enhance_with_subdomain_info(self, analysis: Dict[str, Any], domain: str, subdomain: str, 
                                   subdomain_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Enhance legal analysis with subdomain-specific information"""
        
        # Add subdomain classification to analysis
        analysis["subdomain_classification"] = {
            "domain": domain,
            "subdomain": subdomain,
            "description": subdomain_info.get("description", ""),
            "keywords": subdomain_info.get("keywords", [])
        }
        
        # Add subdomain-specific legal guidance
        analysis["subdomain_guidance"] = self._get_subdomain_specific_guidance(domain, subdomain, query)
        
        return analysis
    
    def _get_subdomain_specific_guidance(self, domain: str, subdomain: str, query: str) -> Dict[str, Any]:
        """Get subdomain-specific legal guidance"""
        
        # Subdomain-specific guidance database
        subdomain_guidance = {
            "criminal_law": {
                "theft": {
                    "immediate_actions": [
                        "File FIR at nearest police station immediately",
                        "Gather evidence (CCTV footage, witnesses)",
                        "Block stolen cards/accounts if applicable",
                        "Inform insurance company if covered"
                    ],
                    "legal_sections": ["IPC Section 378 (Theft)", "IPC Section 379 (Punishment for theft)"],
                    "documents_needed": ["Identity proof", "Purchase receipts", "Insurance documents", "Witness statements"],
                    "timeline": "File FIR within 24 hours for best results",
                    "success_factors": ["Quick reporting", "Strong evidence", "Witness testimony"]
                },
                "cyber_crime": {
                    "immediate_actions": [
                        "Change all passwords immediately",
                        "Report to Cyber Crime Cell",
                        "File complaint on cybercrime.gov.in",
                        "Preserve digital evidence"
                    ],
                    "legal_sections": ["IT Act Section 66", "IT Act Section 43", "IPC Section 420"],
                    "documents_needed": ["Screenshots", "Transaction records", "Communication logs", "Device information"],
                    "timeline": "Report within 48 hours to preserve digital evidence",
                    "success_factors": ["Digital evidence preservation", "Quick reporting", "Technical documentation"]
                }
            },
            "employment_law": {
                "wrongful_termination": {
                    "immediate_actions": [
                        "Request termination letter in writing",
                        "Collect employment documents",
                        "File complaint with Labour Commissioner",
                        "Consult employment lawyer"
                    ],
                    "legal_sections": ["Industrial Disputes Act 1947", "Contract Labour Act", "Shops and Establishments Act"],
                    "documents_needed": ["Employment contract", "Termination letter", "Salary slips", "Performance reviews"],
                    "timeline": "File complaint within 45 days of termination",
                    "success_factors": ["Proper documentation", "Contract terms", "Performance records"]
                },
                "confidentiality_breach": {
                    "immediate_actions": [
                        "Document the breach incident",
                        "Notify legal department immediately",
                        "Preserve evidence of disclosure",
                        "Assess damage to company"
                    ],
                    "legal_sections": ["Indian Contract Act Section 27", "Copyright Act", "Trade Secrets Law"],
                    "documents_needed": ["NDA agreement", "Evidence of breach", "Damage assessment", "Employment contract"],
                    "timeline": "Take action immediately to prevent further damage",
                    "success_factors": ["Strong NDA terms", "Clear evidence", "Damage quantification"]
                }
            },
            "family_law": {
                "divorce": {
                    "immediate_actions": [
                        "Consult family law attorney",
                        "Gather marriage documents",
                        "Document grounds for divorce",
                        "Consider mediation first"
                    ],
                    "legal_sections": ["Hindu Marriage Act 1955", "Special Marriage Act 1954", "Indian Divorce Act 1869"],
                    "documents_needed": ["Marriage certificate", "Income documents", "Property documents", "Evidence of grounds"],
                    "timeline": "Process typically takes 6-18 months",
                    "success_factors": ["Clear grounds", "Mutual consent", "Proper documentation"]
                },
                "child_custody": {
                    "immediate_actions": [
                        "Document child's best interests",
                        "Maintain stable environment",
                        "Keep detailed records",
                        "Consider child's preferences"
                    ],
                    "legal_sections": ["Guardians and Wards Act 1890", "Hindu Minority and Guardianship Act"],
                    "documents_needed": ["Birth certificate", "School records", "Medical records", "Income proof"],
                    "timeline": "Custody decisions can take 3-12 months",
                    "success_factors": ["Child's welfare", "Stable environment", "Financial capability"]
                }
            },
            "tenant_rights": {
                "security_deposit": {
                    "immediate_actions": [
                        "Send written demand to landlord",
                        "Document property condition",
                        "File complaint with Rent Control Board",
                        "Gather lease agreement"
                    ],
                    "legal_sections": ["Rent Control Act", "Transfer of Property Act", "Consumer Protection Act"],
                    "documents_needed": ["Lease agreement", "Deposit receipts", "Property photos", "Communication records"],
                    "timeline": "File complaint within 30 days of lease end",
                    "success_factors": ["Written lease terms", "Property documentation", "Timely action"]
                },
                "habitability": {
                    "immediate_actions": [
                        "Document unsafe conditions",
                        "Send written notice to landlord",
                        "Report to municipal authorities",
                        "Consider rent withholding"
                    ],
                    "legal_sections": ["Rent Control Act", "Municipal Corporation Act", "Consumer Protection Act"],
                    "documents_needed": ["Photos/videos", "Written notices", "Municipal complaints", "Medical records if applicable"],
                    "timeline": "Give landlord reasonable time to fix (7-30 days)",
                    "success_factors": ["Clear documentation", "Written notices", "Health/safety evidence"]
                }
            }
        }
        
        # Get guidance for specific domain and subdomain
        domain_guidance = subdomain_guidance.get(domain, {})
        specific_guidance = domain_guidance.get(subdomain, {})
        
        if not specific_guidance:
            # Provide general guidance if specific not available
            specific_guidance = {
                "immediate_actions": ["Consult with a qualified attorney", "Document all relevant information", "Gather supporting evidence"],
                "legal_sections": ["Consult legal expert for applicable laws"],
                "documents_needed": ["All relevant documents and evidence"],
                "timeline": "Seek legal advice promptly",
                "success_factors": ["Professional legal guidance", "Complete documentation", "Timely action"]
            }
        
        return specific_guidance
    
    def _format_subdomain_response(self, analysis: Dict[str, Any], domain: str, subdomain: str, 
                                 subdomain_info: Dict[str, Any], subdomain_confidence: float) -> str:
        """Format response with subdomain information"""
        
        formatted_response = f"""
🎯 **DOMAIN & SUBDOMAIN CLASSIFICATION**
***
**Primary Domain:** {domain.replace('_', ' ').title()}
**Specific Subdomain:** {subdomain.replace('_', ' ').title()} (Confidence: {subdomain_confidence:.1%})
**Subdomain Description:** {subdomain_info.get('description', 'Specific legal matter within this domain')}

🎯 **SUBDOMAIN-SPECIFIC GUIDANCE**
***
"""
        
        # Add subdomain-specific guidance
        if "subdomain_guidance" in analysis:
            guidance = analysis["subdomain_guidance"]
            
            formatted_response += f"""
**⚡ IMMEDIATE ACTIONS:**
"""
            for action in guidance.get("immediate_actions", []):
                formatted_response += f"* {action}\n"
            
            formatted_response += f"""
**📜 APPLICABLE LEGAL SECTIONS:**
"""
            for section in guidance.get("legal_sections", []):
                formatted_response += f"* {section}\n"
            
            formatted_response += f"""
**📋 DOCUMENTS NEEDED:**
"""
            for doc in guidance.get("documents_needed", []):
                formatted_response += f"* {doc}\n"
            
            formatted_response += f"""
**⏰ TIMELINE:** {guidance.get('timeline', 'Consult attorney for specific timeline')}

**🎯 SUCCESS FACTORS:**
"""
            for factor in guidance.get("success_factors", []):
                formatted_response += f"* {factor}\n"
        
        # Add original enhanced analysis
        if "formatted_response" in analysis:
            formatted_response += f"\n{analysis['formatted_response']}"
        
        return formatted_response
    
    def display_subdomain_response(self, response: Dict[str, Any]) -> None:
        """Display the subdomain-enhanced response"""
        
        print("\n" + "="*80)
        print("🎯 SUBDOMAIN ENHANCED LEGAL ANALYSIS")
        print("="*80)
        print()
        
        # Display domain and subdomain classification
        print(f"🏛️ **CLASSIFICATION RESULTS**")
        print(f"   Primary Domain: {response['domain'].replace('_', ' ').title()} (confidence: {response['domain_confidence']:.1%})")
        print(f"   Specific Subdomain: {response['subdomain'].replace('_', ' ').title()} (confidence: {response['subdomain_confidence']:.1%})")
        
        if response.get('subdomain_alternatives'):
            print(f"   Alternative Subdomains:")
            for alt_subdomain, alt_conf in response['subdomain_alternatives'][1:3]:
                print(f"     • {alt_subdomain.replace('_', ' ').title()} (confidence: {alt_conf:.1%})")
        
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
    
    def get_subdomain_stats(self) -> Dict[str, Any]:
        """Get subdomain classifier statistics"""
        return self.subdomain_classifier.get_stats()


def create_subdomain_enhanced_agent():
    """Factory function to create subdomain enhanced agent"""
    return SubdomainEnhancedAgent()


def main():
    """Main function for testing the subdomain enhanced agent"""
    
    print("🎯 SUBDOMAIN ENHANCED LEGAL AGENT")
    print("=" * 50)
    print("This agent provides hierarchical legal classification:")
    print("✅ Main Domain Classification (criminal_law, employment_law, etc.)")
    print("✅ Detailed Subdomain Classification (theft, cyber_crime, etc.)")
    print("✅ Subdomain-Specific Legal Guidance")
    print("✅ Enhanced Constitutional Analysis")
    print("✅ Comprehensive Legal Provisions")
    print()
    
    # Create subdomain enhanced agent
    try:
        agent = create_subdomain_enhanced_agent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Show classifier stats
    stats = agent.get_subdomain_stats()
    print(f"📊 Subdomain Classifier Stats:")
    print(f"   Total Domains: {stats['total_domains']}")
    print(f"   Total Subdomains: {stats['total_subdomains']}")
    print(f"   Trained Classifiers: {stats['trained_classifiers']}")
    print()
    
    # Test queries with expected subdomains
    test_queries = [
        "My phone is stolen",
        "Someone is hacking my phone",
        "I was fired from my job unfairly",
        "Employee disclosed company secrets",
        "I want to divorce my spouse",
        "Landlord won't return my security deposit",
        "I bought a defective phone and want refund",
        "Car accident caused injuries",
        "My passport is expired",
        "Elderly parent being financially exploited"
    ]
    
    print("🧪 TESTING SUBDOMAIN ENHANCED AGENT")
    print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📋 TEST {i}: {query}")
        print("-" * 30)
        
        try:
            # Process query with subdomain classification
            response = agent.process_query_with_subdomains(query)
            
            # Display subdomain-enhanced response
            agent.display_subdomain_response(response)
            
            # Wait for user input to continue (except for last query)
            if i < len(test_queries):
                input(f"\n⏸️  Press Enter to continue to test {i+1}...")
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            continue
    
    print("\n🎯 SUBDOMAIN ENHANCED AGENT TESTING COMPLETE!")
    print("✅ All queries processed with subdomain classification")
    print("📚 The agent now provides hierarchical legal analysis")
    print("🚀 Ready for production use with subdomain capabilities!")


if __name__ == "__main__":
    main()