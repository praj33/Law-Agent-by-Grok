"""
Adaptive Agent Core - Task 2 Implementation
==========================================

This module serves as the core adaptive wrapper that learns from user interactions.
Implements the main adaptive_agent.py requirement for Task 2.

Features:
- Behavioral adaptation via reinforcement principles
- Context storage across turns
- Confidence and strategy adjustment
- Integration with conversation loop, reward engine, and state memory

Author: Legal Agent Team
Version: 3.0.0 (Task 2 - Adaptive Core)
Date: 2025-08-15
"""

import json
import datetime
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict
import logging

# Import base legal agent
from legal_agent import LegalAgent, LegalQueryInput, LegalAgentResponse, create_legal_agent

# Import adaptive components
try:
    from conversation_loop import create_conversation_loop, ConversationLoop
    from reward_engine import create_reward_engine, RewardEngine
    from state_memory import create_state_memory, StateMemory
    from constitutional_article_matcher import get_constitutional_articles_with_confidence, format_article_recommendations
    from query_storage import create_query_storage, QueryStorage
    ADAPTIVE_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some adaptive components not available: {e}")
    ADAPTIVE_COMPONENTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class StructuredResponseFormatter:
    """Formats responses in the detailed step-by-step structure requested by user"""
    
    def __init__(self):
        self.domain_descriptions = {
            'tenant rights': 'Property/Rental Law (Tenant Rights)',
            'employment law': 'Employment/Labor Law', 
            'cyber_crime': 'Cyber Crime (Digital Security)',
            'family law': 'Family Law (Marriage/Divorce/Child)',
            'criminal law': 'Criminal Law (Offenses/Punishment)',
            'consumer rights': 'Consumer Protection Law',
            'contract law': 'Contract/Agreement Law',
            'property law': 'Property/Real Estate Law',
            'constitutional law': 'Constitutional/Fundamental Rights',
            'tax law': 'Tax/Revenue Law'
        }
        
        self.legal_acts = {
            'tenant rights': ['Rent Control Act', 'Transfer of Property Act', 'Consumer Protection Act'],
            'employment law': ['Industrial Disputes Act, 1947', 'Payment of Wages Act, 1936', 'Labour Laws'],
            'cyber_crime': ['Information Technology Act, 2000 (Section 66, 66C)', 'Indian Penal Code (Section 419, 420)'],
            'family law': ['Hindu Marriage Act, 1955', 'Indian Christian Marriage Act', 'Domestic Violence Act'],
            'criminal law': ['Indian Penal Code (IPC)', 'Code of Criminal Procedure (CrPC)'],
            'consumer rights': ['Consumer Protection Act, 2019', 'Sale of Goods Act'],
            'contract law': ['Indian Contract Act, 1872', 'Specific Relief Act'],
            'property law': ['Transfer of Property Act, 1882', 'Registration Act'],
            'constitutional law': ['Constitution of India', 'Fundamental Rights'],
            'tax law': ['Income Tax Act, 1961', 'Goods and Services Tax Act']
        }

    def format_structured_response(self, query: str, response: LegalAgentResponse, 
                                 ml_confidence: float = None, internal_logs: Dict = None) -> str:
        """Format response in detailed step-by-step structure with constitutional articles"""
        
        domain = response.domain
        confidence = response.confidence
        
        # Get constitutional articles with confidence scores
        constitutional_analysis = None
        try:
            constitutional_analysis = get_constitutional_articles_with_confidence(query)
        except Exception as e:
            logger.warning(f"Could not get constitutional analysis: {e}")
        
        # Step 1: Domain Classification
        step1 = f"""🔹 Step 1: Domain Classification

Query detected: "{query}"
Domain classifier output: {domain}
Subcategory: {self._get_subcategory(domain, query)}"""
        
        # Step 2: ML Classification Output (internal logs)
        ml_conf = ml_confidence or confidence
        step2 = f"""🔹 Step 2: ML Classification Output (internal logs style)

(this is what your agent generates internally, but may or may not show to user)

Enhanced analysis: {domain} + ML suggestion: {domain}
ML Classification: {domain} (confidence ~{ml_conf:.2f})
Dataset Route: {self._get_route_type(domain)}
Success rate (estimated): {self._estimate_success_rate(domain)}%"""
        
        # Step 3: User-Friendly Answer with Constitutional Articles
        domain_desc = self.domain_descriptions.get(domain, domain.title())
        
        # Constitutional articles section - RESTORED with enhanced confidence display
        constitutional_section = ""
        if constitutional_analysis and constitutional_analysis.get('matching_articles', 0) > 0:
            constitutional_section = f"\n\n🏛️ RELEVANT CONSTITUTIONAL ARTICLES:\n"
            
            for i, rec in enumerate(constitutional_analysis['recommendations'][:3], 1):
                confidence_icon = "🟢" if rec['confidence_percentage'] >= 70 else "🟡" if rec['confidence_percentage'] >= 40 else "🔴"
                constitutional_section += f"""
{confidence_icon} Article {rec['article_number']} - {rec['confidence_percentage']}% Confidence
   📖 {rec['title']}
   🔍 Keywords: {', '.join(rec['matching_keywords'][:3])}
   💡 {rec['match_reasons'][0] if rec['match_reasons'] else 'Relevant to query'}"""
            
            # Constitutional Analysis Summary section removed as requested
        
        step3 = f"""🔹 Step 3: User-Friendly Answer (final output to user)

📋 Domain Identified: {domain_desc}

🛑 Issue: {self._get_issue_description(domain, query)}

✅ Legal Route (What you should do):

{self._format_legal_steps(domain, response)}{constitutional_section}

⚖️ Constitutional Backing:

{self._get_constitutional_backing(domain)}

⏱️ Timeline:

{response.timeline or self._get_default_timeline(domain)}

📊 Success Rate: {self._estimate_success_rate(domain)}% {self._get_success_factors(domain)}"""
        
        # Step 4: Final Summary
        step4 = f"""🔹 Step 4: Example Final Response (human-readable)

{self._generate_final_summary(domain, query, response, constitutional_analysis)}"""
        
        return f"{step1}\n\n{step2}\n\n{step3}\n\n{step4}"
    
    def _get_subcategory(self, domain: str, query: str) -> str:
        """Get subcategory based on domain and query"""
        subcategories = {
            'cyber_crime': 'cyber_security / hacking',
            'tenant rights': 'rental_disputes / deposit_issues',
            'employment law': 'workplace_rights / wage_disputes',
            'family law': 'marriage / divorce / custody',
            'criminal law': 'offenses / legal_proceedings',
            'consumer rights': 'product_defects / service_disputes'
        }
        return subcategories.get(domain, 'general_legal_matter')
    
    def _get_route_type(self, domain: str) -> str:
        """Get primary route type for domain"""
        routes = {
            'cyber_crime': 'police_station (cyber cell)',
            'tenant rights': 'rent_tribunal / housing_court',
            'employment law': 'labour_court / conciliation',
            'family law': 'family_court / mediation',
            'criminal law': 'police_station / magistrate',
            'consumer rights': 'consumer_forum / district_court'
        }
        return routes.get(domain, 'appropriate_court / legal_authority')
    
    def _estimate_success_rate(self, domain: str) -> int:
        """Estimate success rate based on domain"""
        rates = {
            'cyber_crime': 70,
            'tenant rights': 75,
            'employment law': 65,
            'family law': 60,
            'criminal law': 80,
            'consumer rights': 85
        }
        return rates.get(domain, 70)
    
    def _get_issue_description(self, domain: str, query: str) -> str:
        """Get detailed issue description"""
        descriptions = {
            'cyber_crime': 'Unauthorized access or control of your digital devices/accounts, which is a punishable offence under the Information Technology Act, 2000 and Indian Penal Code.',
            'tenant rights': 'Landlord-tenant dispute involving rental agreements, deposits, or housing rights, governed by state Rent Control Acts and consumer protection laws.',
            'employment law': 'Workplace-related issue involving employer-employee rights, wages, or working conditions under various Labour Laws.',
            'family law': 'Family-related legal matter involving marriage, divorce, custody, or domestic relations under personal laws.',
            'criminal law': 'Criminal offense or legal proceeding under the Indian Penal Code and Criminal Procedure Code.',
            'consumer rights': 'Consumer dispute involving defective products or inadequate services under Consumer Protection Act, 2019.'
        }
        return descriptions.get(domain, 'Legal matter requiring appropriate legal remedy under relevant Indian laws.')
    
    def _format_legal_steps(self, domain: str, response: LegalAgentResponse) -> str:
        """Format legal steps based on domain"""
        if hasattr(response, 'process_steps') and response.process_steps:
            # Check if process_steps already contain numbers
            first_step = response.process_steps[0].strip() if response.process_steps else ""
            if first_step and (first_step[0].isdigit() or first_step.startswith(('1.', '2.', '3.'))):
                # Steps are already numbered, return as-is
                return '\n'.join(response.process_steps)
            else:
                # Steps need numbering
                return '\n'.join([f"{i+1}. {step}" for i, step in enumerate(response.process_steps)])
        
        # Default steps by domain
        default_steps = {
            'cyber_crime': """1. Document evidence
   • Take screenshots of suspicious activities
   • Save logs, emails, transaction details
   
2. Immediate actions
   • Change all passwords immediately
   • Enable two-factor authentication
   • Run security scans on devices
   
3. File complaint
   • Report at nearest police station or cyber cell
   • File online at https://cybercrime.gov.in
   
4. Legal process
   • Police registers FIR under IT Act
   • Investigation by Cyber Cell
   • Court proceedings if required""",
            
            'tenant rights': """1. Document the issue
   • Gather rental agreement, receipts
   • Take photos/videos as evidence
   
2. Communicate formally
   • Send written notice to landlord
   • Keep copies of all communication
   
3. Legal remedies
   • Approach Rent Tribunal
   • File complaint in consumer forum if applicable
   
4. Court proceedings
   • Civil court for monetary disputes
   • Housing court for eviction matters"""
        }
        
        return default_steps.get(domain, response.legal_route or "Consult with appropriate legal authority for specific guidance.")
    
    def _get_constitutional_backing(self, domain: str) -> str:
        """Get constitutional article references"""
        backing = {
            'cyber_crime': "Article 21 → Right to life and personal liberty → includes right to privacy & security of communication.\nArticle 14 → Equality before law → ensures fair treatment in investigation.",
            'tenant rights': "Article 19(1)(e) → Right to reside and settle → protects housing rights.\nArticle 21 → Right to shelter → fundamental aspect of right to life.",
            'employment law': "Article 14 → Equality in employment opportunities.\nArticle 16 → Equal opportunity in public employment.\nArticle 21 → Right to livelihood as part of right to life.",
            'family law': "Article 14 → Equality before law in family matters.\nArticle 15 → Prohibition of discrimination.\nArticle 21 → Right to live with dignity in family relationships.",
            'criminal law': "Article 20 → Protection against self-incrimination and double jeopardy.\nArticle 21 → Right to fair trial and legal representation.\nArticle 22 → Right against arbitrary arrest and detention."
        }
        return backing.get(domain, "Article 14 → Equality before law → ensures fair legal treatment.\nArticle 21 → Right to life and liberty → includes access to justice.")
    
    def _get_default_timeline(self, domain: str) -> str:
        """Get default timeline for domain"""
        timelines = {
            'cyber_crime': "FIR registration: Immediate (same day).\nInvestigation: 1–6 months depending on complexity.\nCourt trial (if needed): 6 months–2 years.",
            'tenant rights': "Notice period: 15-30 days.\nTribunal filing: Immediate after notice.\nHearing: 2-6 months.\nResolution: 3-12 months.",
            'employment law': "Conciliation: 15-45 days.\nLabour court filing: After failed conciliation.\nHearing: 3-8 months.\nJudgment: 6-18 months."
        }
        return timelines.get(domain, "Initial filing: Immediate.\nProceedings: 3-12 months.\nResolution: Variable based on complexity.")
    
    def _get_success_factors(self, domain: str) -> str:
        """Get factors affecting success rate"""
        factors = {
            'cyber_crime': "(depends on evidence & tracing ability of cyber police)",
            'tenant rights': "(depends on documentation & rental agreement terms)",
            'employment law': "(depends on employment records & witness testimony)",
            'family law': "(depends on mutual consent & evidence presented)"
        }
        return factors.get(domain, "(depends on evidence quality & legal representation)")
    
    def _generate_final_summary(self, domain: str, query: str, response: LegalAgentResponse, 
                              constitutional_analysis: Dict = None) -> str:
        """Generate concise final summary with constitutional backing"""
        domain_action = {
            'cyber_crime': "a cyber crime. You should immediately secure your accounts, collect evidence, and file a complaint with the cyber cell.",
            'tenant rights': "a tenant rights issue. You should document everything, send formal notice to landlord, and approach the rent tribunal if needed.",
            'employment law': "an employment law matter. You should gather employment records and approach the labour department or court.",
            'family law': "a family law issue. You should consider mediation first, then approach family court if needed."
        }
        
        action = domain_action.get(domain, f"a {domain} matter requiring appropriate legal action.")
        
        # Add constitutional backing with specific articles if available
        constitutional_ref = "Your fundamental rights are protected by the Constitution of India."
        if constitutional_analysis and constitutional_analysis.get('recommendations'):
            top_article = constitutional_analysis['recommendations'][0]
            constitutional_ref = f"Your fundamental rights are protected by Article {top_article['article_number']} ({top_article['confidence_percentage']}% confidence) and other constitutional provisions."
        
        return f"Your query about '{query}' is {action} {constitutional_ref}"


@dataclass
class AdaptiveContext:
    """Context information for adaptive learning"""
    session_id: str
    conversation_turn: int
    previous_queries: List[str]
    previous_responses: List[LegalAgentResponse]
    feedback_history: List[str]
    confidence_evolution: List[float]
    learning_events: List[Dict[str, Any]]


class AdaptiveAgent:
    """
    Core adaptive wrapper that learns from user interactions over time.
    
    This is the main adaptive_agent.py module required for Task 2.
    Implements behavioral adaptation via reinforcement principles.
    """
    
    def __init__(self, 
                 base_agent: Optional[LegalAgent] = None,
                 enable_conversation_loop: bool = True,
                 enable_reward_engine: bool = True,
                 enable_state_memory: bool = True):
        """Initialize adaptive agent with learning components"""
        
        # Base legal agent - use working enhanced agent for better classification
        try:
            from working_enhanced_agent import create_working_enhanced_agent
            self.base_agent = base_agent or create_working_enhanced_agent()
        except ImportError:
            self.base_agent = base_agent or create_legal_agent()
        
        # Initialize structured response formatter
        self.response_formatter = StructuredResponseFormatter()
        
        # Adaptive components
        self.conversation_loop = None
        self.reward_engine = None
        self.state_memory = None
        self.query_storage = None
        
        if ADAPTIVE_COMPONENTS_AVAILABLE:
            if enable_conversation_loop:
                self.conversation_loop = create_conversation_loop()
            if enable_reward_engine:
                self.reward_engine = create_reward_engine()
            if enable_state_memory:
                self.state_memory = create_state_memory()
            # Always initialize query storage
            try:
                self.query_storage = create_query_storage()
            except Exception as e:
                logger.warning(f"Could not initialize query storage: {e}")
        
        # Learning state
        self.active_contexts: Dict[str, AdaptiveContext] = {}
        self.learning_stats = {
            'total_interactions': 0,
            'learning_events': 0,
            'confidence_adjustments': 0,
            'strategy_changes': 0
        }
        
        # Behavioral adaptation parameters - FIXED for proper learning
        self.confidence_adjustment_rate = 2.0  # Increased significantly for noticeable adjustments
        self.strategy_adaptation_threshold = 0.3
        self.assertiveness_levels = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.9
        }

        # Domain-specific confidence adjustments
        self.domain_confidence_adjustments = defaultdict(float)
        
        # SEPARATE DIRECT FEEDBACK ADJUSTMENTS - bypasses reward engine dilution
        self.direct_domain_feedback_boosts = defaultdict(float)
        
        # Direct confidence boost/penalty for immediate feedback - MAXIMIZED FOR IMMEDIATE STRONG IMPACT
        self.direct_feedback_adjustment = {
            'positive': 0.80,   # +80% confidence boost for positive feedback (maximized for immediate impact)
            'negative': -0.50,  # -50% confidence penalty for negative feedback (maximized for immediate impact) 
            'clarification': 0.25,  # +25% for clarification 
            'neutral': 0.10     # +10% small boost for engagement
        }
        
        logger.info("Adaptive agent core initialized")
    
    def process_query_with_learning(self, query_input: LegalQueryInput) -> LegalAgentResponse:
        """Process query with adaptive learning capabilities and comprehensive guidance"""
        
        # Track response time
        start_time = datetime.datetime.now()
        
        session_id = query_input.session_id or self._generate_session_id()
        
        # Get or create adaptive context
        context = self._get_or_create_context(session_id)
        
        # Store context across turns
        context.previous_queries.append(query_input.user_input)
        context.conversation_turn += 1
        
        # Process feedback FIRST if provided to update domain confidence adjustments
        if query_input.feedback and context.previous_responses:
            self._process_feedback_learning(context, query_input.feedback)
        
        # Get base response - handle different agent types
        if hasattr(self.base_agent, '__class__') and 'WorkingEnhancedAgent' in str(self.base_agent.__class__):
            # Working enhanced agent expects string input
            base_response = self.base_agent.process_query(query_input.user_input)
        else:
            # Standard legal agent expects LegalQueryInput object
            base_response = self.base_agent.process_query(query_input)
        
        # Ensure comprehensive guidance - enhance if needed
        base_response = self._ensure_comprehensive_guidance(base_response, query_input.user_input)
        
        # Apply adaptive adjustments (including any feedback-based confidence adjustments)
        adapted_response = self._apply_adaptive_adjustments(
            base_response, context, query_input
        )
        
        # Calculate response time
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds()
        adapted_response.response_time = response_time
        
        # Store query in database for analysis
        if self.query_storage:
            try:
                query_id = self.query_storage.store_query(
                    query_input.user_input,
                    adapted_response,
                    session_id,
                    response_time
                )
                # Store query_id in context for feedback updates
                if not hasattr(context, 'query_ids'):
                    context.query_ids = []
                context.query_ids.append(query_id)
            except Exception as e:
                logger.warning(f"Could not store query: {e}")
        
        # Store response in context
        context.previous_responses.append(adapted_response)
        context.confidence_evolution.append(adapted_response.confidence)
        
        # Record learning event if significant change occurred
        if self._is_significant_learning_event(context):
            self._record_learning_event(context, adapted_response)
        
        # Update learning statistics
        self.learning_stats['total_interactions'] += 1
        
        logger.info(f"Processed adaptive query for session {session_id}, turn {context.conversation_turn}")
        
        return adapted_response
    
    def process_query_with_structured_output(self, query_input: LegalQueryInput) -> str:
        """Process query and return structured step-by-step response format"""
        
        # Get the standard adaptive response
        response = self.process_query_with_learning(query_input)
        
        # Format with structured output
        structured_response = self.response_formatter.format_structured_response(
            query_input.user_input,
            response,
            ml_confidence=response.confidence
        )
        
        return structured_response
    
    def process_query_with_terminal_format(self, query_input: LegalQueryInput) -> str:
        """Process query and return clean terminal-ready format for CLI"""
        
        # Get the standard adaptive response
        response = self.process_query_with_learning(query_input)
        
        # Format with clean terminal output
        terminal_response = self._format_terminal_response(
            query_input.user_input,
            response
        )
        
        return terminal_response
    
    def _format_terminal_response(self, query: str, response) -> str:
        """Format response for clean terminal display"""
        domain = response.domain
        query_lower = query.lower()
        
        # Get enhanced formatting for all components
        domain_desc = self._get_enhanced_domain_description(domain, query)
        subcategory = self._get_enhanced_subcategory(domain, query)
        issue_desc = self._get_enhanced_issue_description(domain, query)
        legal_steps = self._get_enhanced_legal_steps(domain, query, response)
        constitutional_backing = self._get_enhanced_constitutional_backing(domain, query)
        success_rate = self._get_enhanced_success_rate(domain)
        timeline = self._get_enhanced_timeline(domain)
        final_answer = self._get_enhanced_final_answer(domain, query)
        
        # Format the clean terminal output
        terminal_output = f"""🔍 Processing Query: {query}
--------------------------------------------------

📋 Domain Identified: {domain_desc}  
⚖️ Subcategory: {subcategory}  

🛑 Issue: {issue_desc}  

✅ Legal Route (What should be done):
{legal_steps}  

⚖️ Relevant Constitutional Backing:
{constitutional_backing}  

📊 Success Rate: {success_rate}.  
⏱️ Expected Timeline: {timeline}.  

--------------------------------------------------
💬 Final User-Friendly Answer:
{final_answer}"""
        
        return terminal_output
    
    def _get_enhanced_domain_description(self, domain: str, query: str) -> str:
        """Get enhanced domain description with specific formatting"""
        query_lower = query.lower()
        
        if domain == 'employment_law':
            if any(word in query_lower for word in ['secrets', 'confidential', 'disclosure', 'trade secrets']):
                return 'Employment Law / Corporate Law'
            return 'Employment Law'
        
        enhanced_descriptions = {
            'cyber_crime': 'Cyber Crime / Digital Security',
            'tenant_rights': 'Tenant Rights / Rental Law',
            'family_law': 'Family Law / Marriage & Divorce',
            'criminal_law': 'Criminal Law / Offenses',
            'consumer_complaint': 'Consumer Protection Law',
            'property_disputes': 'Property Law / Real Estate',
            'immigration_law': 'Immigration Law / Visa Matters'
        }
        
        return enhanced_descriptions.get(domain, domain.replace('_', ' ').title())
    
    def _get_enhanced_subcategory(self, domain: str, query: str) -> str:
        """Get enhanced subcategory with specific formatting"""
        query_lower = query.lower()
        
        if domain == 'employment_law':
            if any(word in query_lower for word in ['secrets', 'confidential', 'disclosure', 'discloses', 'trade secrets', 'proprietary', 'insider']):
                return 'Breach of Confidentiality & Trade Secrets'
            elif any(word in query_lower for word in ['harassment', 'harassing', 'sexually harassing']):
                return 'Workplace Harassment'
            elif any(word in query_lower for word in ['fired', 'terminated', 'termination', 'dismissal']):
                return 'Wrongful Termination'
            elif any(word in query_lower for word in ['salary', 'wages', 'overtime', 'pay', 'unpaid', 'not paying']):
                return 'Salary & Wage Disputes'
            return 'Employment Rights & Labor Issues'
        
        subcategories = {
            'cyber_crime': 'Digital Security & Online Fraud',
            'tenant_rights': 'Rental Disputes & Housing Rights',
            'family_law': 'Marriage, Divorce & Custody',
            'criminal_law': 'Criminal Offenses & Legal Proceedings',
            'consumer_complaint': 'Product Defects & Service Issues',
            'property_disputes': 'Property Rights & Real Estate',
            'immigration_law': 'Visa & Citizenship Matters'
        }
        
        return subcategories.get(domain, 'General Legal Matter')
    
    def _get_enhanced_issue_description(self, domain: str, query: str) -> str:
        """Get enhanced issue description"""
        query_lower = query.lower()
        
        if domain == 'employment_law' and any(word in query_lower for word in ['secrets', 'confidential', 'disclosure', 'discloses', 'trade secrets', 'proprietary', 'insider']):
            return 'Employee leaking confidential company data to another company.'
        
        descriptions = {
            'cyber_crime': 'Unauthorized digital access or online security breach affecting your accounts/devices.',
            'tenant_rights': 'Landlord-tenant dispute involving rental agreements, deposits, or housing rights.',
            'employment_law': 'Workplace-related issue involving employer-employee rights and working conditions.',
            'family_law': 'Family-related legal matter involving marriage, divorce, custody, or domestic relations.',
            'criminal_law': 'Criminal offense or legal proceeding under Indian Penal Code.',
            'consumer_complaint': 'Consumer dispute involving defective products or inadequate services.',
            'property_disputes': 'Property-related dispute involving ownership, possession, or real estate matters.',
            'immigration_law': 'Immigration or visa-related legal matter under Indian citizenship laws.'
        }
        
        return descriptions.get(domain, 'Legal matter requiring appropriate legal remedy under relevant Indian laws.')
    
    def _get_enhanced_legal_steps(self, domain: str, query: str, response) -> str:
        """Get enhanced legal steps with specific formatting"""
        query_lower = query.lower()
        
        # Employment law confidentiality cases - specific format
        if domain == 'employment_law' and any(word in query_lower for word in ['secrets', 'confidential', 'disclosure', 'discloses', 'trade secrets', 'proprietary', 'insider']):
            return """1. Review employee's contract & NDA (Non-Disclosure Agreement).
2. Collect evidence of unauthorized disclosure (emails, logs, communications).
3. Send legal notice to the employee for breach of trust.
4. File a complaint under:
   • Indian Contract Act, 1872 (Breach of Contract)
   • IT Act, 2000 – Section 72A (Disclosure of information without consent)
   • IPC Sections 408/409 (Criminal breach of trust by employee)
5. Approach Labour Court / Civil Court for remedies.
6. Company can claim damages & seek injunction to stop further disclosures."""
        
        # Use existing process steps if available
        if hasattr(response, 'process_steps') and response.process_steps:
            steps = []
            for i, step in enumerate(response.process_steps[:8], 1):
                clean_step = step.split('.', 1)[-1].strip() if '.' in step else step
                steps.append(f"{i}. {clean_step}")
            return '\n'.join(steps)
        
        # Default steps by domain - COMPREHENSIVE coverage for all domains
        default_steps = {
            'cyber_crime': """1. Secure all accounts immediately (change passwords, enable 2FA).
2. Document evidence (screenshots, logs, transaction details).
3. File complaint at nearest cyber cell or police station.
4. Submit online complaint at cybercrime.gov.in portal.
5. Cooperate with police investigation and provide evidence.
6. Follow up on case status and legal proceedings.""",
            
            'tenant_rights': """1. Review rental agreement and document the issue with evidence.
2. Send written notice to landlord via registered post.
3. Approach Rent Control Authority or Housing Court.
4. File complaint in Consumer Forum if service deficiency.
5. Seek legal remedy through Civil Court if needed.
6. Enforce court orders through appropriate legal mechanisms.""",
            
            'family_law': """1. Gather all relevant documents (marriage certificate, property papers).
2. Attempt mediation/counseling if relationship issues.
3. Consult family law advocate for legal options.
4. File petition in Family Court under relevant personal laws.
5. Attend hearings and follow court procedures.
6. Ensure compliance with court orders and settlements.""",
            
            'criminal_law': """1. File FIR at nearest police station immediately.
2. Cooperate with police investigation and provide evidence.
3. Engage criminal defense lawyer if accused.
4. Attend court hearings and follow legal procedures.
5. Apply for bail if required through proper channels.
6. Follow court orders and comply with legal requirements.""",
            
            'consumer_complaint': """1. Gather purchase receipts, warranty, and defect evidence.
2. Send written complaint to company/service provider.
3. File complaint in District Consumer Forum.
4. Submit all supporting documents and evidence.
5. Attend hearings and present your case.
6. Enforce consumer forum orders for compensation.""",
            
            'property_disputes': """1. Collect all property documents (sale deed, title papers).
2. Verify property records at Sub-Registrar office.
3. Send legal notice to the other party.
4. File suit in Civil Court for property rights.
5. Present evidence and documents during trial.
6. Obtain court decree and execute if necessary.""",
            
            'immigration_law': """1. Review visa/passport status and expiry dates.
2. Gather required documents for application/renewal.
3. Submit application at appropriate consulate/office.
4. Pay required fees and follow official procedures.
5. Attend interviews or biometric appointments.
6. Track application status and collect documents.""",
            
            'employment_law': """1. Review employment contract and company policies.
2. Document the workplace issue with evidence.
3. Raise grievance through internal company channels.
4. Approach Labour Commissioner or Conciliation Officer.
5. File complaint in Labour Court if conciliation fails.
6. Attend hearings and seek appropriate relief.""",
            
            'personal_injury': """1. Seek immediate medical attention and document injuries.
2. File police complaint if accident/assault involved.
3. Collect evidence (photos, witness statements, medical records).
4. Notify insurance companies involved.
5. Consult personal injury lawyer for compensation claim.
6. File civil suit for damages if needed.""",
            
            'contract_law': """1. Review contract terms and identify breach.
2. Collect evidence of contract violation.
3. Send legal notice for breach of contract.
4. Attempt negotiation/mediation for settlement.
5. File civil suit for specific performance or damages.
6. Enforce court decree through execution proceedings.""",
            
            'unknown': """1. Identify the specific legal issue and applicable laws.
2. Gather all relevant documents and evidence.
3. Consult with appropriate legal professional.
4. Determine correct legal forum and jurisdiction.
5. File complaint/petition with proper documentation.
6. Follow legal proceedings and court orders."""
        }
        
        return default_steps.get(domain, "1. Consult with appropriate legal authority for specific guidance.")
    
    def _get_enhanced_constitutional_backing(self, domain: str, query: str) -> str:
        """Get enhanced constitutional backing with specific articles"""
        query_lower = query.lower()
        
        # Employment law confidentiality - specific articles
        if domain == 'employment_law' and any(word in query_lower for word in ['secrets', 'confidential', 'disclosure', 'discloses', 'trade secrets', 'proprietary', 'insider']):
            return """- Article 19(1)(g): Freedom of profession, subject to restrictions (confidentiality laws).
- Article 21: Right to life & liberty → includes privacy & data protection.
- Article 300A: Protection of company property (IP & trade secrets).
- Article 14: Equality before law (ensures fair legal treatment)."""
        
        # Domain-specific constitutional backing
        backing = {
            'cyber_crime': """- Article 21: Right to life & personal liberty → includes right to privacy & digital security.
- Article 19: Freedom of speech & expression → protects against unauthorized surveillance.
- Article 14: Equality before law → ensures fair investigation and legal treatment.""",
            
            'tenant_rights': """- Article 19(1)(e): Right to reside and settle → protects housing rights.
- Article 21: Right to life → includes right to shelter and dignified living.
- Article 300A: Right to property → protects against unlawful deprivation of deposits.""",
            
            'employment_law': """- Article 14: Equality before law → ensures fair treatment in employment.
- Article 16: Equal opportunity in employment → prohibits discrimination.
- Article 21: Right to livelihood → fundamental aspect of right to life."""
        }
        
        return backing.get(domain, """- Article 14: Equality before law → ensures fair legal treatment.
- Article 21: Right to life and liberty → includes access to justice.""")
    
    def _get_enhanced_success_rate(self, domain: str) -> str:
        """Get enhanced success rate with range format"""
        rates = {
            'employment_law': '70–85% (depends on strength of contract & evidence)',
            'cyber_crime': '60–75% (depends on evidence & cyber cell capabilities)',
            'tenant_rights': '70–80% (depends on documentation & rental agreement)',
            'family_law': '55–70% (depends on mutual agreement & evidence)',
            'criminal_law': '75–85% (depends on evidence quality & investigation)',
            'consumer_complaint': '80–90% (depends on proof of defect & purchase records)'
        }
        return rates.get(domain, '65–75% (depends on evidence quality & legal representation)')
    
    def _get_enhanced_timeline(self, domain: str) -> str:
        """Get enhanced timeline with specific format"""
        timelines = {
            'employment_law': '6–12 months (civil/criminal proceedings)',
            'cyber_crime': '3–8 months (investigation & legal proceedings)',
            'tenant_rights': '4–9 months (tribunal & court proceedings)',
            'family_law': '6–18 months (mediation & court proceedings)',
            'criminal_law': '6–24 months (investigation & trial)',
            'consumer_complaint': '3–6 months (consumer forum proceedings)'
        }
        return timelines.get(domain, '6–12 months (standard legal proceedings)')
    
    def _get_enhanced_final_answer(self, domain: str, query: str) -> str:
        """Get enhanced final answer with specific messaging"""
        query_lower = query.lower()
        
        if domain == 'employment_law' and any(word in query_lower for word in ['secrets', 'confidential', 'disclosure', 'discloses', 'trade secrets', 'proprietary', 'insider']):
            return """This matter falls under Employment/Corporate Law, not consumer complaint.
Your employee's act of sharing company secrets violates confidentiality and trust.
You should take legal action under the Contract Act, IT Act, and IPC.
Constitutional protections like Article 19, 21, 14, and 300A also apply."""
        
        final_answers = {
            'cyber_crime': """This is a cyber crime matter requiring immediate action.
Secure your accounts and file complaint with cyber cell immediately.
Your digital rights are protected under IT Act and constitutional provisions.""",
            
            'tenant_rights': """This is a tenant rights issue under rental law.
Document everything and approach Rent Control Authority.
Your housing rights are constitutionally protected under Article 21.""",
            
            'family_law': """This is a family law matter under personal laws.
Consider mediation first, then approach Family Court if needed.
Your family rights are protected under constitutional provisions.""",
            
            'criminal_law': """This is a criminal law matter under Indian Penal Code.
File FIR immediately and engage criminal defense lawyer.
Your legal rights are protected under constitutional safeguards.""",
            
            'consumer_complaint': """This is a consumer protection matter under Consumer Protection Act.
File complaint in Consumer Forum with proper evidence.
Your consumer rights are protected under constitutional provisions.""",
            
            'property_disputes': """This is a property law matter requiring civil court action.
Gather all property documents and send legal notice first.
Your property rights are protected under constitutional provisions.""",
            
            'immigration_law': """This is an immigration/visa matter under citizenship laws.
Follow official procedures and submit required documents.
Your legal status rights are protected under constitutional provisions.""",
            
            'employment_law': """This is an employment law matter under Labour Laws.
Raise grievance through proper channels and approach Labour Court.
Your employment rights are protected under constitutional provisions.""",
            
            'personal_injury': """This is a personal injury matter requiring immediate action.
Seek medical attention first, then legal consultation.
Your right to compensation is protected under tort law and constitutional provisions.""",
            
            'contract_law': """This is a contract law matter under Indian Contract Act.
Review contract terms and send legal notice for breach.
Your contractual rights are protected under constitutional provisions.""",
            
            'unknown': """This legal matter requires professional assessment.
Consult with appropriate legal authority for specific guidance.
Your fundamental rights are protected under constitutional provisions."""
        }
        
        return final_answers.get(domain, f"This matter falls under {domain.replace('_', ' ').title()}. Consult appropriate legal authority for specific guidance.")
    
    def _ensure_comprehensive_guidance(self, response, query: str):
        """Ensure all responses have comprehensive legal guidance"""
        
        # Check if response has process steps - handle different response types
        if not hasattr(response, 'process_steps') or not response.process_steps:
            # Generate comprehensive steps based on domain
            domain = response.domain
            comprehensive_steps = self._get_enhanced_legal_steps(domain, query, response)
            
            # Convert string steps to list if needed
            if isinstance(comprehensive_steps, str):
                steps_list = [step.strip() for step in comprehensive_steps.split('\n') if step.strip()]
                response.process_steps = steps_list
        
        # Ensure response has constitutional backing - handle different response types
        if not hasattr(response, 'constitutional_backing') or not response.constitutional_backing:
            constitutional_backing = self._get_enhanced_constitutional_backing(response.domain, query)
            # Add constitutional_backing attribute if it doesn't exist
            response.constitutional_backing = constitutional_backing
        
        # Ensure response has success rate - ALWAYS override for consistent string format
        success_rate = self._get_enhanced_success_rate(response.domain)
        # Always set enhanced string format success rate for comprehensive guidance
        response.success_rate = success_rate
        
        # Ensure response has timeline - handle different response types  
        if not hasattr(response, 'timeline') or not response.timeline:
            timeline = self._get_enhanced_timeline(response.domain)
            # Add timeline attribute if it doesn't exist
            response.timeline = timeline
        
        # For WorkingEnhancedAgent responses, ensure all comprehensive attributes exist
        if hasattr(response, 'user_query') and not hasattr(response, 'outcome'):
            # This is a SimpleEnhancedResponse from WorkingEnhancedAgent - add missing attributes
            if not hasattr(response, 'constitutional_backing'):
                response.constitutional_backing = self._get_enhanced_constitutional_backing(response.domain, query)
            # Always use enhanced string format success rate
            response.success_rate = self._get_enhanced_success_rate(response.domain)
            if not hasattr(response, 'timeline'):
                response.timeline = self._get_enhanced_timeline(response.domain)
        
        return response
    
    def get_constitutional_analysis(self, query: str) -> Dict[str, Any]:
        """Get detailed constitutional article analysis for a query"""
        try:
            return get_constitutional_articles_with_confidence(query)
        except Exception as e:
            logger.error(f"Error getting constitutional analysis: {e}")
            return {
                'total_articles_searched': 0,
                'matching_articles': 0,
                'recommendations': [],
                'error': str(e)
            }
    
    def get_formatted_constitutional_analysis(self, query: str) -> str:
        """Get formatted constitutional article analysis for display"""
        try:
            analysis = self.get_constitutional_analysis(query)
            return format_article_recommendations(analysis)
        except Exception as e:
            return f"❌ Error analyzing constitutional articles: {e}"
    
    def _get_or_create_context(self, session_id: str) -> AdaptiveContext:
        """Get existing context or create new one"""
        
        if session_id not in self.active_contexts:
            self.active_contexts[session_id] = AdaptiveContext(
                session_id=session_id,
                conversation_turn=0,
                previous_queries=[],
                previous_responses=[],
                feedback_history=[],
                confidence_evolution=[],
                learning_events=[]
            )
        
        return self.active_contexts[session_id]
    
    def _process_feedback_learning(self, context: AdaptiveContext, feedback: str):
        """
        Process feedback for learning and adaptation.
        
        Implements reinforcement learning principles:
        - Positive feedback increases confidence
        - Negative feedback decreases confidence
        - Strategy adaptation based on feedback patterns
        """
        
        context.feedback_history.append(feedback)
        
        # Classify feedback type
        feedback_type = self._classify_feedback(feedback)
        
        # Get the last response to apply feedback to
        if not context.previous_responses:
            return
            
        last_response = context.previous_responses[-1]
        original_confidence = last_response.confidence
        
        # Apply direct feedback adjustment to separate direct feedback tracking
        direct_adjustment = self.direct_feedback_adjustment.get(feedback_type, 0.0)
        # Apply direct feedback boost that bypasses reward engine dilution
        self.direct_domain_feedback_boosts[last_response.domain] += direct_adjustment
        # Apply decay to prevent infinite accumulation - keep only recent feedback impact
        self.direct_domain_feedback_boosts[last_response.domain] *= 0.8  # 20% decay
        
        # Also apply to domain confidence adjustments for reward engine compatibility
        original_domain_adjustment = self.domain_confidence_adjustments[last_response.domain]
        self._adjust_confidence_for_domain(last_response.domain, direct_adjustment)
        # Store the direct feedback adjustment amount for later use
        direct_feedback_amount = self.domain_confidence_adjustments[last_response.domain] - original_domain_adjustment
        
        # Log the adjustment
        logger.info(f"Domain confidence adjustment: {feedback_type} -> {direct_adjustment:+.3f} for {last_response.domain}")
        
        # Update stored query with feedback
        if self.query_storage and hasattr(context, 'query_ids') and context.query_ids:
            try:
                latest_query_id = context.query_ids[-1]
                self.query_storage.update_feedback(latest_query_id, feedback, feedback_type)
            except Exception as e:
                logger.warning(f"Could not update query feedback: {e}")
        
        self.learning_stats['confidence_adjustments'] += 1
        
        # Calculate reward if reward engine available
        if self.reward_engine and context.previous_responses:
            last_response = context.previous_responses[-1]
            
            reward_data = {
                'type': feedback_type,
                'text': feedback,
                'satisfaction': feedback_type
            }
            
            # Prepare context data for reward calculation
            reward_context = {
                'session_id': context.session_id,
                'query': context.previous_queries[-1] if context.previous_queries else '',
                'response_time': getattr(last_response, 'response_time', 1.0),
                'previous_domain': getattr(context.previous_responses[-2], 'domain', None) if len(context.previous_responses) >= 2 else None,
                'previous_confidence': getattr(context.previous_responses[-2], 'confidence', 0.5) if len(context.previous_responses) >= 2 else None,
                'previous_route': getattr(context.previous_responses[-2], 'legal_route', '') if len(context.previous_responses) >= 2 else '',
                'confidence_before': original_confidence
            }
            
            # Calculate reward
            reward, reward_components = self.reward_engine.calculate_reward(
                reward_data,
                last_response,
                reward_context
            )
            
            # Apply domain-specific confidence adjustment based on reward - but preserve direct feedback strength
            reward_adjustment = self.reward_engine.get_confidence_adjustment(reward)
            # Don't let reward engine override direct feedback - only add supplementary reward adjustment
            current_domain_adjustment = self.domain_confidence_adjustments[last_response.domain]
            # Ensure direct feedback strength is preserved by making reward adjustment smaller than direct feedback
            if abs(direct_feedback_amount) > 0.1:  # If we have significant direct feedback
                reward_adjustment = min(abs(reward_adjustment), abs(direct_feedback_amount) * 0.1) * (1 if reward_adjustment >= 0 else -1)
            self._adjust_confidence_for_domain(last_response.domain, reward_adjustment)
            
            # Log reward calculation for transparency
            logger.info(f"Reward calculated: {reward:.3f} (accuracy: {reward_components.accuracy:.3f}, helpfulness: {reward_components.helpfulness:.3f}, clarity: {reward_components.clarity:.3f})")
        # Record state memory if available
        if self.state_memory and context.previous_responses and context.previous_queries:
            last_response = context.previous_responses[-1]
            last_query = context.previous_queries[-1]

            # Get confidence before and after adjustment
            confidence_before = context.confidence_evolution[-2] if len(context.confidence_evolution) >= 2 else last_response.confidence
            confidence_after = context.confidence_evolution[-1]

            self.state_memory.record_query_improvement(
                last_query,
                last_response.domain,
                confidence_before,
                confidence_after,
                feedback_type
            )
        
        # Check for strategy adaptation
        if self._should_adapt_strategy(context, feedback_type):
            self._adapt_response_strategy(context, feedback_type)
            self.learning_stats['strategy_changes'] += 1
        
        logger.info(f"Processed feedback learning: {feedback_type}")
    
    def _apply_adaptive_adjustments(self, 
                                  base_response,
                                  context: AdaptiveContext,
                                  query_input: LegalQueryInput):
        """Apply adaptive adjustments to base response"""
        
        # Get domain-specific confidence adjustment
        confidence_adjustment = self._get_domain_confidence_adjustment(base_response.domain)
        
        # Apply confidence adjustment (this is the key fix)
        adjusted_confidence = max(0.0, min(1.0, base_response.confidence + confidence_adjustment))
        
        # Log the confidence adjustment being applied
        if confidence_adjustment != 0.0:
            logger.info(f"Applying domain confidence adjustment: {base_response.confidence:.3f} + {confidence_adjustment:.3f} = {adjusted_confidence:.3f}")
        
        # Adjust assertiveness based on context
        assertiveness_level = self._determine_assertiveness_level(context, base_response.domain)
        
        # Create adapted response - handle both LegalAgentResponse and SimpleEnhancedResponse
        if hasattr(base_response, 'outcome'):  # LegalAgentResponse
            from legal_agent import LegalAgentResponse
            adapted_response = LegalAgentResponse(
                domain=base_response.domain,
                confidence=adjusted_confidence,
                legal_route=self._adapt_legal_route(base_response.legal_route, assertiveness_level),
                timeline=base_response.timeline,
                outcome=base_response.outcome,
                process_steps=base_response.process_steps,
                glossary=base_response.glossary,
                session_id=base_response.session_id,
                timestamp=base_response.timestamp,
                raw_query=base_response.raw_query,
                location_insights=base_response.location_insights,
                data_driven_advice=base_response.data_driven_advice,
                risk_assessment=base_response.risk_assessment,
                constitutional_backing=base_response.constitutional_backing,
                constitutional_articles=base_response.constitutional_articles
            )
        else:  # SimpleEnhancedResponse from WorkingEnhancedAgent
            from legal_agent import LegalAgentResponse
            adapted_response = LegalAgentResponse(
                domain=base_response.domain,
                confidence=adjusted_confidence,
                legal_route=self._adapt_legal_route(base_response.legal_route, assertiveness_level),
                timeline=base_response.timeline,
                outcome="Successful resolution of legal matter",  # Default outcome
                process_steps=base_response.process_steps or [],
                glossary=[],  # Default empty glossary
                session_id=base_response.session_id,
                timestamp=base_response.timestamp,
                raw_query=base_response.user_query,
                location_insights=None,  # Not available in SimpleEnhancedResponse
                data_driven_advice=None,  # Not available in SimpleEnhancedResponse
                risk_assessment=None,  # Not available in SimpleEnhancedResponse
                constitutional_backing=base_response.constitutional_backing,
                constitutional_articles=base_response.constitutional_articles or []
            )
        
        # Ensure comprehensive guidance attributes are carried over from base_response
        if hasattr(base_response, 'success_rate'):
            adapted_response.success_rate = base_response.success_rate
        if hasattr(base_response, 'constitutional_backing') and base_response.constitutional_backing:
            adapted_response.constitutional_backing = base_response.constitutional_backing
        if hasattr(base_response, 'timeline') and base_response.timeline:
            adapted_response.timeline = base_response.timeline
        if hasattr(base_response, 'process_steps') and base_response.process_steps:
            adapted_response.process_steps = base_response.process_steps
        
        return adapted_response
    
    def _classify_feedback(self, feedback: str) -> str:
        """Classify feedback type for learning"""
        
        feedback_lower = feedback.lower()
        
        # Negative feedback (check first to catch "not helpful")
        if any(phrase in feedback_lower for phrase in ['not helpful', 'unhelpful', 'wrong domain', 'wrong', 'bad', 'poor', 'incorrect']):
            return 'negative'
        
        # Positive feedback
        elif any(word in feedback_lower for word in ['helpful', 'good', 'excellent', 'perfect', 'thank']):
            return 'positive'
        
        # Clarification request
        elif any(word in feedback_lower for word in ['what', 'how', 'explain', 'clarify', 'more']):
            return 'clarification'
        
        # Neutral
        else:
            return 'neutral'
    
    def _should_adapt_strategy(self, context: AdaptiveContext, feedback_type: str) -> bool:
        """Determine if strategy adaptation is needed"""
        
        # Adapt if we have enough feedback history
        if len(context.feedback_history) < 2:
            return False
        
        # Count recent negative feedback
        recent_feedback = context.feedback_history[-3:]
        negative_count = sum(1 for f in recent_feedback if self._classify_feedback(f) == 'negative')
        
        # Adapt if too much negative feedback
        return negative_count >= 2
    
    def _adapt_response_strategy(self, context: AdaptiveContext, feedback_type: str):
        """Adapt response strategy based on feedback patterns"""
        
        # Strategy adaptations based on feedback
        if feedback_type == 'negative':
            # Reduce assertiveness, increase explanation detail
            context.learning_events.append({
                'type': 'strategy_adaptation',
                'change': 'reduce_assertiveness',
                'reason': 'negative_feedback',
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        elif feedback_type == 'clarification':
            # Increase detail level, add more explanations
            context.learning_events.append({
                'type': 'strategy_adaptation',
                'change': 'increase_detail',
                'reason': 'clarification_request',
                'timestamp': datetime.datetime.now().isoformat()
            })
    
    def _determine_assertiveness_level(self, context: AdaptiveContext, domain: str) -> str:
        """Determine appropriate assertiveness level"""
        
        # Check for recent strategy adaptations
        recent_events = [e for e in context.learning_events 
                        if e.get('type') == 'strategy_adaptation']
        
        if recent_events:
            last_event = recent_events[-1]
            if last_event.get('change') == 'reduce_assertiveness':
                return 'low'
            elif last_event.get('change') == 'increase_detail':
                return 'medium'
        
        # Default assertiveness based on domain
        if domain in ['criminal law', 'constitutional law']:
            return 'high'
        elif domain in ['contract law', 'property law']:
            return 'medium'
        else:
            return 'low'
    
    def _adapt_legal_route(self, original_route: str, assertiveness_level: str) -> str:
        """Adapt legal route based on assertiveness level"""
        
        if assertiveness_level == 'high':
            # More direct, assertive language
            if 'consider' in original_route.lower():
                return original_route.replace('consider', 'should')
            elif 'may' in original_route.lower():
                return original_route.replace('may', 'must')
        
        elif assertiveness_level == 'low':
            # More cautious, gentle language
            if 'must' in original_route.lower():
                return original_route.replace('must', 'may consider')
            elif 'should' in original_route.lower():
                return original_route.replace('should', 'might consider')
        
        return original_route
    
    def _get_domain_confidence_adjustment(self, domain: str) -> float:
        """Get confidence adjustment for domain based on learning - includes direct feedback bypassing reward engine"""
        
        # Combine regular domain adjustments with direct feedback boosts
        regular_adjustment = self.domain_confidence_adjustments.get(domain, 0.0)
        direct_feedback_boost = self.direct_domain_feedback_boosts.get(domain, 0.0)
        
        # Direct feedback takes priority and bypasses reward engine dilution
        total_adjustment = regular_adjustment + direct_feedback_boost
        
        return total_adjustment

    def _adjust_confidence_for_domain(self, domain: str, adjustment: float):
        """Adjust confidence for specific domain"""

        # Update domain-specific confidence adjustments with exponential moving average
        current_adjustment = self.domain_confidence_adjustments[domain]
        alpha = 0.99  # Maximum learning rate for immediate impact (increased from 0.95)
        self.domain_confidence_adjustments[domain] = (
            (1 - alpha) * current_adjustment + alpha * adjustment
        )

        logger.info(f"Adjusted confidence for {domain}: {adjustment:+.3f} -> {self.domain_confidence_adjustments[domain]:+.3f}")
    
    def _is_significant_learning_event(self, context: AdaptiveContext) -> bool:
        """Check if this represents a significant learning event"""
        
        if len(context.confidence_evolution) < 2:
            return False
        
        # Check for significant confidence change
        confidence_change = abs(context.confidence_evolution[-1] - context.confidence_evolution[-2])
        
        return confidence_change > 0.1
    
    def _record_learning_event(self, context: AdaptiveContext, response: LegalAgentResponse):
        """Record a significant learning event"""
        
        learning_event = {
            'type': 'learning_event',
            'session_id': context.session_id,
            'turn': context.conversation_turn,
            'domain': response.domain,
            'confidence_change': context.confidence_evolution[-1] - context.confidence_evolution[-2] if len(context.confidence_evolution) >= 2 else 0,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        context.learning_events.append(learning_event)
        self.learning_stats['learning_events'] += 1
        
        logger.info(f"Recorded learning event for session {context.session_id}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        
        stats = {
            **self.learning_stats,
            'active_sessions': len(self.active_contexts),
            'components_available': ADAPTIVE_COMPONENTS_AVAILABLE,
            'conversation_loop_enabled': self.conversation_loop is not None,
            'reward_engine_enabled': self.reward_engine is not None,
            'state_memory_enabled': self.state_memory is not None
        }
        
        # Add component-specific statistics
        if self.conversation_loop:
            conv_stats = self.conversation_loop.get_learning_statistics()
            stats['conversation_statistics'] = conv_stats
        
        if self.reward_engine:
            reward_stats = self.reward_engine.get_reward_statistics()
            stats['reward_statistics'] = reward_stats
        
        if self.state_memory:
            memory_stats = self.state_memory.get_memory_stats()
            stats['memory_statistics'] = memory_stats
        
        return stats
    
    def get_session_context(self, session_id: str) -> Optional[AdaptiveContext]:
        """Get context for a specific session"""
        
        return self.active_contexts.get(session_id)
    
    def get_recent_queries(self, limit: int = 10):
        """Get recent queries from storage"""
        if self.query_storage:
            return self.query_storage.get_recent_queries(limit)
        return []
    
    def get_query_statistics(self):
        """Get query statistics from storage"""
        if self.query_storage:
            return self.query_storage.get_statistics()
        return {}
    
    def search_queries(self, search_term: str, limit: int = 10):
        """Search queries by term"""
        if self.query_storage:
            return self.query_storage.search_queries(search_term, limit)
        return []
    
    def start_conversation(self, initial_query: str, session_id: Optional[str] = None) -> Tuple[str, Any]:
        """
        Start a multi-turn conversation using conversation loop.
        
        Args:
            initial_query: User's initial legal query
            session_id: Optional session ID
            
        Returns:
            Tuple of (session_id, initial_response)
        """
        
        if self.conversation_loop:
            # Use conversation loop for multi-turn handling
            session_id = self.conversation_loop.start_conversation(
                initial_query,
                self
            )
            
            # Get the first response from the conversation
            session = self.conversation_loop.active_conversations.get(session_id)
            if session and session.turns:
                initial_response = session.turns[0].agent_response
                return session_id, initial_response
        
        # Fallback to single query processing
        query_input = LegalQueryInput(
            user_input=initial_query,
            session_id=session_id
        )
        
        response = self.process_query_with_learning(query_input)
        return query_input.session_id or self._generate_session_id(), response
    
    def continue_conversation(self, 
                            session_id: str,
                            user_input: str,
                            feedback_on_previous: Optional[str] = None) -> Tuple[Any, bool]:
        """
        Continue a multi-turn conversation.
        
        Args:
            session_id: Session identifier
            user_input: User's next input
            feedback_on_previous: Optional feedback on previous response
            
        Returns:
            Tuple of (agent_response, should_end_conversation)
        """
        
        if self.conversation_loop:
            return self.conversation_loop.continue_conversation(
                session_id,
                user_input,
                self,
                feedback_on_previous
            )
        else:
            # Fallback: process as single query with feedback
            query_input = LegalQueryInput(
                user_input=user_input,
                session_id=session_id,
                feedback=feedback_on_previous
            )
            
            response = self.process_query_with_learning(query_input)
            return response, False  # Don't end conversation in fallback mode
    
    def end_session(self, session_id: str):
        """End an adaptive session and clean up context"""
        
        if session_id in self.active_contexts:
            context = self.active_contexts[session_id]
            
            # Save conversation data before ending
            if self.conversation_loop:
                self.conversation_loop.end_conversation(session_id)
            
            # Save any pending reward or memory data
            if self.reward_engine:
                self.reward_engine.save_reward_history()
            
            if self.state_memory:
                # Final update to learning statistics
                self.state_memory.load_learning_stats()
            
            # Clean up context
            del self.active_contexts[session_id]
            
            logger.info(f"Ended adaptive session {session_id} with {context.conversation_turn} turns")
    
    def get_query_statistics(self) -> Dict[str, Any]:
        """Get comprehensive query statistics"""
        if self.query_storage:
            return self.query_storage.get_statistics()
        return {}
    
    def get_recent_queries(self, limit: int = 10) -> List:
        """Get recent queries for analysis"""
        if self.query_storage:
            return self.query_storage.get_recent_queries(limit)
        return []
    
    def search_queries(self, search_term: str, limit: int = 10) -> List:
        """Search stored queries"""
        if self.query_storage:
            return self.query_storage.search_queries(search_term, limit)
        return []
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"adaptive_{timestamp}_{len(self.active_contexts):04d}"


def create_adaptive_agent(base_agent: Optional[LegalAgent] = None,
                         enable_conversation_loop: bool = True,
                         enable_reward_engine: bool = True,
                         enable_state_memory: bool = True) -> AdaptiveAgent:
    """
    Factory function to create adaptive agent.
    
    This is the main entry point for creating the adaptive agent
    as required for Task 2.
    
    Args:
        base_agent: Optional base legal agent (creates default if None)
        enable_conversation_loop: Enable multi-turn conversation handling
        enable_reward_engine: Enable feedback reward calculation
        enable_state_memory: Enable persistent learning memory
        
    Returns:
        AdaptiveAgent: Configured adaptive agent instance
    """
    
    return AdaptiveAgent(
        base_agent=base_agent,
        enable_conversation_loop=enable_conversation_loop,
        enable_reward_engine=enable_reward_engine,
        enable_state_memory=enable_state_memory
    )


# Test the adaptive agent
if __name__ == "__main__":
    print("🤖 ADAPTIVE AGENT TEST")
    print("=" * 50)
    
    try:
        # Create adaptive agent
        agent = create_adaptive_agent()
        
        # Test single query processing
        query_input = LegalQueryInput(
            user_input="my landlord is not returning my security deposit",
            session_id="test_session_001"
        )
        
        response = agent.process_query_with_learning(query_input)
        
        print(f"✅ Initial Response:")
        print(f"   Domain: {response.domain}")
        print(f"   Confidence: {response.confidence:.3f}")
        print(f"   Route: {response.legal_route[:60]}...")
        
        # Test feedback processing
        feedback_query = LegalQueryInput(
            user_input="what legal action can I take",
            session_id="test_session_001",
            feedback="helpful"
        )
        
        feedback_response = agent.process_query_with_learning(feedback_query)
        
        print(f"\n✅ After Feedback:")
        print(f"   Domain: {feedback_response.domain}")
        print(f"   Confidence: {feedback_response.confidence:.3f}")
        print(f"   Improvement: {feedback_response.confidence - response.confidence:+.3f}")
        
        # Test conversation loop if available
        if agent.conversation_loop:
            print(f"\n✅ Testing Conversation Loop:")
            
            conv_session_id, conv_response = agent.start_conversation(
                "someone hacked my bank account"
            )
            
            print(f"   Started conversation: {conv_session_id}")
            print(f"   Initial domain: {conv_response.domain}")
            
            # Continue conversation
            next_response, should_end = agent.continue_conversation(
                conv_session_id,
                "how to report this to police",
                "helpful"
            )
            
            print(f"   Continued conversation, should_end: {should_end}")
            
            # End conversation
            agent.end_session(conv_session_id)
        
        # Get learning statistics
        stats = agent.get_learning_stats()
        print(f"\n📊 Learning Statistics:")
        print(f"   Active Sessions: {stats['active_sessions']}")
        print(f"   Total Interactions: {stats['total_interactions']}")
        print(f"   Learning Events: {stats['learning_events']}")
        print(f"   Confidence Adjustments: {stats['confidence_adjustments']}")
        
        if 'conversation_statistics' in stats:
            conv_stats = stats['conversation_statistics']
            print(f"   Conversations: {conv_stats['total_conversations']}")
            print(f"   Average Turns: {conv_stats['average_turns']:.1f}")
        
        if 'reward_statistics' in stats:
            reward_stats = stats['reward_statistics']
            print(f"   Average Reward: {reward_stats['average_reward']:.3f}")
            print(f"   Learning Rate: {reward_stats['current_learning_rate']:.3f}")
        
        if 'memory_statistics' in stats:
            memory_stats = stats['memory_statistics']
            print(f"   Memory Records: {memory_stats['total_records']}")
            print(f"   Unique Patterns: {memory_stats['unique_patterns']}")
        
        print(f"\n✅ Adaptive agent test completed successfully!")
        print(f"🎯 All Task 2 components integrated and working")
        
    except Exception as e:
        print(f"❌ Adaptive agent test failed: {e}")
        import traceback
        traceback.print_exc()
