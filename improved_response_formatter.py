"""
Improved Response Formatter
===========================

Enhanced response formatter that includes legal frameworks and 
avoids irrelevant constitutional articles for corporate queries.

Features:
- Legal framework integration
- Smart constitutional article filtering
- Corporate law specific responses
- Reduced noise from irrelevant articles

Author: Legal Agent Team
Version: 2.0.0 - Enhanced Formatting
Date: 2025-08-29
"""

import logging
from typing import Dict, List, Optional, Any
from legal_agent import LegalAgentResponse

logger = logging.getLogger(__name__)


class ImprovedResponseFormatter:
    """Enhanced response formatter with legal frameworks"""
    
    def __init__(self):
        self.domain_descriptions = {
            'tenant_rights': 'Property/Rental Law (Tenant Rights)',
            'employment_law': 'Employment/Labor Law', 
            'corporate_law': 'Corporate Law / Employment Law',  # NEW
            'cyber_crime': 'Cyber Crime (Digital Security)',
            'family_law': 'Family Law (Marriage/Divorce/Child)',
            'criminal_law': 'Criminal Law (Offenses/Punishment)',
            'consumer_complaint': 'Consumer Protection Law',
            'contract_dispute': 'Contract/Agreement Law',
            'property_law': 'Property/Real Estate Law',
            'constitutional_law': 'Constitutional/Fundamental Rights',
            'tax_law': 'Tax/Revenue Law'
        }
        
        # Enhanced legal frameworks
        self.legal_frameworks = {
            'corporate_law': {
                'primary': ['Indian Contract Act, 1872', 'Companies Act, 2013', 'IT Act, 2000 (Section 72)'],
                'secondary': ['Trade Secrets Act', 'Indian Penal Code (Section 405, 408)', 'Copyright Act, 1957']
            },
            'employment_law': {
                'primary': ['Industrial Disputes Act, 1947', 'Payment of Wages Act, 1936', 'Indian Contract Act, 1872'],
                'secondary': ['IT Act, 2000 (Section 72)', 'Indian Penal Code (Section 405)', 'Labour Laws']
            },
            'cyber_crime': {
                'primary': ['IT Act, 2000', 'Indian Penal Code (Section 66, 419, 420)'],
                'secondary': ['Data Protection Laws', 'Privacy Laws']
            },
            'tenant_rights': {
                'primary': ['Rent Control Act', 'Transfer of Property Act, 1882'],
                'secondary': ['Consumer Protection Act, 2019']
            }
        }
    
    def format_enhanced_response(self, query: str, response: LegalAgentResponse, 
                               ml_confidence: float = None) -> str:
        """Format response with enhanced legal frameworks and smart filtering"""
        
        domain = response.domain
        confidence = response.confidence
        
        # Get improved constitutional analysis
        constitutional_analysis = None
        try:
            from improved_constitutional_matcher import get_improved_constitutional_analysis
            constitutional_analysis = get_improved_constitutional_analysis(query, domain)
        except ImportError:
            # Fallback to original
            try:
                from constitutional_article_matcher import get_constitutional_articles_with_confidence
                constitutional_analysis = get_constitutional_articles_with_confidence(query)
            except Exception as e:
                logger.warning(f"Could not get constitutional analysis: {e}")
        
        # Step 1: Domain Classification
        step1 = f"""🔹 Step 1: Domain Classification

Query detected: "{query}"
Domain classifier output: {domain}
Subcategory: {self._get_enhanced_subcategory(domain, query)}"""
        
        # Step 2: ML Classification Output
        ml_conf = ml_confidence or confidence
        step2 = f"""🔹 Step 2: ML Classification Output (internal logs style)

(this is what your agent generates internally, but may or may not show to user)

Enhanced analysis: {domain} + ML suggestion: {domain}
ML Classification: {domain} (confidence ~{ml_conf:.2f})
Dataset Route: {self._get_route_type(domain)}
Success rate (estimated): {self._estimate_success_rate(domain)}%"""
        
        # Step 3: Enhanced User-Friendly Answer
        domain_desc = self.domain_descriptions.get(domain, domain.title())
        
        # Enhanced constitutional section with legal frameworks
        constitutional_section = ""
        legal_framework_section = ""
        
        if constitutional_analysis and constitutional_analysis.get('matching_articles', 0) > 0:
            constitutional_section = f"\n\n🏛️ RELEVANT CONSTITUTIONAL ARTICLES:\n"
            
            recommendations = constitutional_analysis.get('recommendations', [])
            for i, rec in enumerate(recommendations[:3], 1):
                confidence_icon = "🟢" if rec['confidence_percentage'] >= 70 else "🟡" if rec['confidence_percentage'] >= 40 else "🔴"
                constitutional_section += f"""
{confidence_icon} Article {rec['article_number']} - {rec['confidence_percentage']}% Confidence
   📖 {rec['title']}
   🔍 Keywords: {', '.join(rec['matching_keywords'][:3])}
   💡 {rec['match_reasons'][0] if rec['match_reasons'] else 'Relevant to query'}"""
            
            # Add legal frameworks section
            frameworks = constitutional_analysis.get('legal_frameworks', [])
            if frameworks and domain in self.legal_frameworks:
                legal_framework_section = f"\n\n⚖️ APPLICABLE LEGAL FRAMEWORK:\n"
                primary_laws = self.legal_frameworks[domain]['primary']
                for law in primary_laws[:3]:
                    legal_framework_section += f"   📜 {law}\n"
                
                if domain == 'corporate_law':
                    legal_framework_section += f"""
   🔍 Specific Sections:
   • Section 72 (IT Act, 2000) → Punishment for disclosure of information
   • Section 405 (IPC) → Criminal breach of trust
   • Contract Act → Breach of confidentiality clause"""
        
        step3 = f"""🔹 Step 3: User-Friendly Answer (final output to user)

📋 Domain Identified: {domain_desc}

🛑 Issue: {self._get_enhanced_issue_description(domain, query)}

✅ Legal Route (What you should do):

{self._format_enhanced_legal_steps(domain, response, query)}{constitutional_section}{legal_framework_section}

⚖️ Constitutional Backing:

{self._get_constitutional_backing(domain)}

⏱️ Timeline:

{response.timeline or self._get_default_timeline(domain)}

📊 Success Rate: {self._estimate_success_rate(domain)}% {self._get_success_factors(domain)}"""
        
        # Step 4: Enhanced Final Summary
        step4 = f"""🔹 Step 4: Example Final Response (human-readable)

{self._generate_enhanced_final_summary(domain, query, response, constitutional_analysis)}"""
        
        return f"{step1}\n\n{step2}\n\n{step3}\n\n{step4}"
    
    def _get_enhanced_subcategory(self, domain: str, query: str) -> str:
        """Get enhanced subcategory based on domain and query"""
        query_lower = query.lower()
        
        subcategories = {
            'corporate_law': 'confidentiality_breach / trade_secrets' if any(term in query_lower for term in ['confidential', 'secrets', 'disclosure']) else 'corporate_governance',
            'employment_law': 'workplace_confidentiality / employee_duties' if any(term in query_lower for term in ['confidential', 'secrets', 'disclosure']) else 'workplace_rights',
            'cyber_crime': 'data_breach / hacking' if any(term in query_lower for term in ['hack', 'breach', 'data']) else 'cyber_security',
            'tenant_rights': 'rental_disputes / deposit_issues',
            'family_law': 'marriage / divorce / custody',
            'criminal_law': 'offenses / legal_proceedings',
            'consumer_complaint': 'product_defects / service_disputes'
        }
        return subcategories.get(domain, 'general_legal_matter')
    
    def _get_route_type(self, domain: str) -> str:
        """Get enhanced route type for domain"""
        routes = {
            'corporate_law': 'civil_court / labour_court (confidentiality breach)',
            'employment_law': 'labour_court / civil_court (employment disputes)',
            'cyber_crime': 'police_station (cyber cell)',
            'tenant_rights': 'rent_tribunal / housing_court',
            'family_law': 'family_court / mediation',
            'criminal_law': 'police_station / magistrate',
            'consumer_complaint': 'consumer_forum / district_court'
        }
        return routes.get(domain, 'appropriate_court / legal_authority')
    
    def _estimate_success_rate(self, domain: str) -> int:
        """Estimate success rate based on domain"""
        rates = {
            'corporate_law': 75,  # High success rate for contract breaches
            'employment_law': 70,  # Good success rate with proper documentation
            'cyber_crime': 60,     # Moderate due to investigation challenges
            'tenant_rights': 75,
            'family_law': 60,
            'criminal_law': 80,
            'consumer_complaint': 85
        }
        return rates.get(domain, 70)
    
    def _get_enhanced_issue_description(self, domain: str, query: str) -> str:
        """Get enhanced issue description"""
        query_lower = query.lower()
        
        if domain == 'corporate_law' and any(term in query_lower for term in ['employee', 'confidential', 'secrets']):
            return 'Breach of confidentiality and company secrets disclosure, which violates employment contract terms and may constitute criminal breach of trust under Indian Penal Code.'
        
        descriptions = {
            'corporate_law': 'Corporate governance issue involving company law compliance, director duties, or business operations under Companies Act, 2013.',
            'employment_law': 'Workplace-related issue involving employer-employee rights, confidentiality agreements, or working conditions under various Labour Laws.',
            'cyber_crime': 'Unauthorized access or control of digital devices/accounts, punishable under Information Technology Act, 2000 and Indian Penal Code.',
            'tenant_rights': 'Landlord-tenant dispute involving rental agreements, deposits, or housing rights, governed by state Rent Control Acts.',
            'family_law': 'Family-related legal matter involving marriage, divorce, custody, or domestic relations under personal laws.',
            'criminal_law': 'Criminal offense or legal proceeding under the Indian Penal Code and Criminal Procedure Code.',
            'consumer_complaint': 'Consumer dispute involving defective products or inadequate services under Consumer Protection Act, 2019.'
        }
        return descriptions.get(domain, 'Legal matter requiring appropriate legal remedy under relevant Indian laws.')
    
    def _format_enhanced_legal_steps(self, domain: str, response: LegalAgentResponse, query: str) -> str:
        """Format enhanced legal steps with specific guidance"""
        
        query_lower = query.lower()
        
        # Corporate law specific steps for confidentiality breach
        if domain == 'corporate_law' and any(term in query_lower for term in ['employee', 'confidential', 'secrets', 'disclosure']):
            return """1. Check employee's employment agreement (confidentiality/NDA clause)
   • Review signed confidentiality agreements
   • Identify specific clauses violated
   • Gather evidence of breach

2. Document the breach comprehensively
   • What information was disclosed
   • To whom it was disclosed
   • When and how the disclosure occurred
   • Potential damage to company

3. File civil suit for breach of contract
   • Under Indian Contract Act, 1872
   • Seek injunction to prevent further disclosure
   • Claim damages for breach

4. Consider criminal complaint if applicable
   • Under IT Act, 2000 (Section 72) if digital data involved
   • Under IPC Section 405 (Criminal breach of trust)
   • File FIR at nearest police station

5. Seek immediate legal remedies
   • Temporary injunction from civil court
   • Restraining order against employee
   • Asset freezing if financial loss involved

6. Approach appropriate court
   • Civil court for contract breach and damages
   • Labour court if employment dispute involved
   • Criminal court if criminal charges filed"""
        
        # Use existing process steps if available
        if hasattr(response, 'process_steps') and response.process_steps:
            return '\n'.join([f"{i+1}. {step}" for i, step in enumerate(response.process_steps)])
        
        # Default enhanced steps by domain
        default_steps = {
            'employment_law': """1. Review employment contract and confidentiality agreements
2. Document all evidence of breach or violation
3. Send legal notice to employer/employee
4. File complaint with appropriate authority (Labour Commissioner/Court)
5. Attend conciliation proceedings if required
6. Present case with evidence and witnesses
7. Seek appropriate remedy (reinstatement/compensation/injunction)""",
            
            'cyber_crime': """1. Preserve all digital evidence immediately
2. Change all passwords and secure accounts
3. File complaint with Cyber Crime Cell
4. Register FIR under IT Act, 2000
5. Cooperate with investigation
6. Seek compensation for damages"""
        }
        
        return default_steps.get(domain, "Consult with appropriate legal authority for specific guidance.")
    
    def _get_constitutional_backing(self, domain: str) -> str:
        """Get constitutional backing"""
        backing = {
            'corporate_law': "Article 19(1)(g) → Freedom to practice profession → subject to reasonable restrictions including confidentiality obligations.\nArticle 21 → Right to fair legal remedy → ensures access to justice for contract breaches.",
            'employment_law': "Article 14 → Equality in employment opportunities.\nArticle 16 → Equal opportunity in employment.\nArticle 21 → Right to livelihood and fair treatment at workplace.",
            'cyber_crime': "Article 21 → Right to life and personal liberty → includes right to privacy & security of communication.\nArticle 14 → Equality before law → ensures fair treatment in investigation.",
            'tenant_rights': "Article 19(1)(e) → Right to reside and settle → protects housing rights.\nArticle 21 → Right to shelter → fundamental aspect of right to life.",
            'family_law': "Article 14 → Equality before law in family matters.\nArticle 15 → Prohibition of discrimination.\nArticle 21 → Right to live with dignity in family relationships.",
            'criminal_law': "Article 20 → Protection against self-incrimination and double jeopardy.\nArticle 21 → Right to fair trial and legal representation.\nArticle 22 → Right against arbitrary arrest and detention."
        }
        return backing.get(domain, "Article 14 → Equality before law → ensures fair legal treatment.\nArticle 21 → Right to life and liberty → includes access to justice.")
    
    def _get_default_timeline(self, domain: str) -> str:
        """Get default timeline for domain"""
        timelines = {
            'corporate_law': "Civil suit filing: Immediate.\nInjunction hearing: 1-2 weeks.\nFinal judgment: 6-18 months.\nCriminal complaint (if applicable): 3-12 months.",
            'employment_law': "Legal notice: 15-30 days.\nConciliation: 15-45 days.\nLabour court filing: After failed conciliation.\nHearing: 3-8 months.\nJudgment: 6-18 months.",
            'cyber_crime': "FIR registration: Immediate (same day).\nInvestigation: 1–6 months depending on complexity.\nCourt trial (if needed): 6 months–2 years.",
            'tenant_rights': "Notice period: 15-30 days.\nTribunal filing: Immediate after notice.\nHearing: 2-6 months.\nResolution: 3-12 months."
        }
        return timelines.get(domain, "Initial filing: Immediate.\nProceedings: 3-12 months.\nResolution: Variable based on complexity.")
    
    def _get_success_factors(self, domain: str) -> str:
        """Get factors affecting success rate"""
        factors = {
            'corporate_law': "(depends on employment contract terms & evidence of breach)",
            'employment_law': "(depends on employment records & witness testimony)",
            'cyber_crime': "(depends on evidence & tracing ability of cyber police)",
            'tenant_rights': "(depends on documentation & rental agreement terms)",
            'family_law': "(depends on mutual consent & evidence presented)"
        }
        return factors.get(domain, "(depends on evidence quality & legal representation)")
    
    def _generate_enhanced_final_summary(self, domain: str, query: str, response: LegalAgentResponse, 
                                       constitutional_analysis: Dict = None) -> str:
        """Generate enhanced final summary"""
        
        query_lower = query.lower()
        
        # Corporate law specific summary
        if domain == 'corporate_law' and any(term in query_lower for term in ['employee', 'confidential', 'secrets']):
            action = "a corporate law matter involving breach of confidentiality. You should immediately review the employment contract, document the breach, and file civil suit under Indian Contract Act, 1872. If digital data was involved, also consider criminal complaint under IT Act, 2000."
        else:
            domain_actions = {
                'corporate_law': "a corporate law matter. You should review relevant agreements and approach civil court for resolution.",
                'employment_law': "an employment law matter. You should gather employment records and approach the labour department or court.",
                'cyber_crime': "a cyber crime. You should immediately secure your accounts, collect evidence, and file a complaint with the cyber cell.",
                'tenant_rights': "a tenant rights issue. You should document everything, send formal notice to landlord, and approach the rent tribunal if needed.",
                'family_law': "a family law issue. You should consider mediation first, then approach family court if needed."
            }
            action = domain_actions.get(domain, f"a {domain} matter requiring appropriate legal action.")
        
        # Add constitutional backing
        constitutional_ref = "Your fundamental rights are protected by the Constitution of India."
        if constitutional_analysis and constitutional_analysis.get('recommendations'):
            top_article = constitutional_analysis['recommendations'][0]
            constitutional_ref = f"Your fundamental rights are protected by Article {top_article['article_number']} ({top_article['confidence_percentage']}% confidence) and other constitutional provisions."
        
        return f"Your query about '{query}' is {action} {constitutional_ref}"


# Global instance
improved_formatter = ImprovedResponseFormatter()


def format_improved_response(query: str, response: LegalAgentResponse, ml_confidence: float = None) -> str:
    """Format response with improved legal frameworks"""
    return improved_formatter.format_enhanced_response(query, response, ml_confidence)


if __name__ == "__main__":
    print("✅ Improved Response Formatter ready!")
    print("Features: Enhanced legal frameworks, smart constitutional filtering, corporate law support")