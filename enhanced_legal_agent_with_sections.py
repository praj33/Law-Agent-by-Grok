"""
Enhanced Legal Agent with IPC/CrPC/Special Acts Integration
==========================================================

This module enhances the existing legal agent to include structured sections:
- IPC Sections (Indian Penal Code, 1860)
- CrPC Sections (Code of Criminal Procedure, 1973)
- Special Acts (if applicable)

These are added to the existing response format without changing the core functionality.

Author: Legal Agent Team
Version: 2.0.0 - Enhanced with Legal Sections
Date: 2025-01-XX
"""

from legal_agent import LegalAgent, LegalQueryInput, LegalAgentResponse, create_legal_agent
from typing import Dict, List, Optional, Tuple, Any
import json

class EnhancedLegalAgent(LegalAgent):
    """Enhanced Legal Agent that adds IPC, CrPC, and Special Acts sections to responses"""
    
    def __init__(self, feedback_file: str = 'feedback.csv', enable_data_integration: bool = True):
        """Initialize the enhanced legal agent"""
        super().__init__(feedback_file, enable_data_integration)
        
        # Initialize legal sections database
        self.ipc_sections = self._initialize_ipc_sections()
        self.crpc_sections = self._initialize_crpc_sections()
        self.special_acts = self._initialize_special_acts()
        self.domain_mappings = self._create_domain_mappings()
    
    def _initialize_ipc_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize IPC sections database"""
        return {
            # Property Crimes
            "378": {
                "title": "Theft",
                "description": "Whoever intends to take dishonestly any movable property out of possession of any person without consent."
            },
            "379": {
                "title": "Punishment for Theft",
                "description": "Whoever commits theft shall be punished with imprisonment up to 3 years, fine, or both."
            },
            "380": {
                "title": "Theft in Dwelling House",
                "description": "Whoever commits theft in any building used as human dwelling shall be punished with imprisonment up to 7 years."
            },
            "392": {
                "title": "Punishment for Robbery",
                "description": "Whoever commits robbery shall be punished with rigorous imprisonment up to 10 years and shall also be liable to fine."
            },
            "403": {
                "title": "Dishonest Misappropriation of Property",
                "description": "Whoever dishonestly misappropriates or converts to his own use any movable property."
            },
            "411": {
                "title": "Dishonestly Receiving Stolen Property",
                "description": "Whoever dishonestly receives or retains any stolen property shall be punished with imprisonment up to 3 years or fine or both."
            },
            "420": {
                "title": "Cheating and Dishonestly Inducing Delivery of Property",
                "description": "Whoever cheats and thereby dishonestly induces delivery of property shall be punished with imprisonment up to 7 years."
            },
            "406": {
                "title": "Punishment for Criminal Breach of Trust",
                "description": "Whoever commits criminal breach of trust shall be punished with imprisonment up to 3 years or fine or both."
            },
            
            # Criminal Law - General
            "302": {
                "title": "Punishment for Murder",
                "description": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine."
            },
            "307": {
                "title": "Attempt to Murder",
                "description": "Whoever does any act with intention or knowledge to cause death shall be punished with imprisonment up to 10 years."
            },
            "323": {
                "title": "Punishment for Voluntarily Causing Hurt",
                "description": "Whoever voluntarily causes hurt shall be punished with imprisonment up to 1 year or fine up to 1000 rupees."
            },
            "324": {
                "title": "Voluntarily Causing Hurt by Dangerous Weapons",
                "description": "Whoever voluntarily causes hurt by dangerous weapons or means shall be punished with imprisonment up to 3 years."
            },
            
            # Women Protection
            "354": {
                "title": "Assault or Criminal Force to Woman with Intent to Outrage her Modesty",
                "description": "Whoever assaults or uses criminal force to any woman with intent to outrage her modesty shall be punished with imprisonment up to 5 years."
            },
            "354A": {
                "title": "Sexual Harassment",
                "description": "A man committing sexual harassment shall be punished with rigorous imprisonment up to 3 years or fine or both."
            },
            "498A": {
                "title": "Husband or Relative of Husband Subjecting Woman to Cruelty",
                "description": "Whoever subjects any woman to cruelty shall be punished with imprisonment up to 3 years and shall also be liable to fine."
            },
            "506": {
                "title": "Punishment for Criminal Intimidation",
                "description": "Whoever commits criminal intimidation shall be punished with imprisonment up to 2 years or fine or both."
            },
            "509": {
                "title": "Word, Gesture or Act Intended to Insult Modesty of Woman",
                "description": "Whoever intends to insult modesty of any woman shall be punished with simple imprisonment up to 3 years."
            }
        }
    
    def _initialize_crpc_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize CrPC sections database"""
        return {
            # Investigation and FIR
            "154": {
                "title": "Information in Cognizable Cases",
                "description": "FIR to be filed at nearest police station for cognizable offences."
            },
            "156": {
                "title": "Police Officer's Power to Investigate Cognizable Case",
                "description": "Police officer's power to investigate cognizable offence without magistrate's order."
            },
            "161": {
                "title": "Examination of Witnesses by Police",
                "description": "Police may examine any person supposed to be acquainted with facts and circumstances of case."
            },
            "173": {
                "title": "Report of Police Officer on Completion of Investigation",
                "description": "Submission of police report (chargesheet) after completion of investigation."
            },
            
            # Arrest and Bail
            "41": {
                "title": "When Police May Arrest Without Warrant",
                "description": "Police officer may arrest without warrant any person who commits cognizable offence in his presence."
            },
            "50": {
                "title": "Person Arrested to be Informed of Grounds of Arrest",
                "description": "Every person arrested shall be informed of grounds of arrest and right to bail if offence is bailable."
            },
            "436": {
                "title": "In What Cases Bail to be Taken",
                "description": "When any person is arrested without warrant, he shall be released on bail if offence is bailable."
            },
            "437": {
                "title": "When Bail May be Taken in Case of Non-Bailable Offence",
                "description": "Magistrate may release accused on bail in non-bailable offence under certain conditions."
            },
            "438": {
                "title": "Direction for Grant of Bail to Person Apprehending Arrest",
                "description": "Anticipatory bail may be granted by High Court or Court of Session."
            },
            
            # Complaints and Magistrate Powers
            "200": {
                "title": "Examination of Complainant",
                "description": "Magistrate taking cognizance of offence on complaint shall examine complainant and witnesses on oath."
            },
            "202": {
                "title": "Postponement of Issue of Process",
                "description": "Magistrate may postpone issue of process and direct investigation by police officer."
            },
            "204": {
                "title": "Issue of Process",
                "description": "If Magistrate is satisfied that there is sufficient ground for proceeding, he shall issue summons or warrant."
            }
        }
    
    def _initialize_special_acts(self) -> Dict[str, Dict[str, str]]:
        """Initialize Special Acts database"""
        return {
            "POSH_2013": {
                "act_name": "Prevention of Sexual Harassment at Workplace Act, 2013",
                "description": "Provides protection against sexual harassment of women at workplace and for prevention and redressal of complaints.",
                "sections": "Sections 3, 4, 9, 11, 13"
            },
            "DV_2005": {
                "act_name": "Protection of Women from Domestic Violence Act, 2005",
                "description": "Provides for more effective protection of rights of women guaranteed under Constitution who are victims of violence of any kind.",
                "sections": "Sections 3, 12, 18, 19, 20"
            },
            "CONSUMER_2019": {
                "act_name": "Consumer Protection Act, 2019",
                "description": "Provides for protection of interests of consumers and establishes authorities for timely and effective administration.",
                "sections": "Sections 2, 35, 59, 87"
            },
            "IT_2000": {
                "act_name": "Information Technology Act, 2000",
                "description": "Provides legal framework for electronic governance and e-commerce and addresses cyber crimes.",
                "sections": "Sections 43, 66, 66A, 66B, 66C, 66D, 67, 72"
            },
            "RENT_CONTROL": {
                "act_name": "Rent Control Act (State-specific)",
                "description": "Regulates renting of residential and commercial premises and provides protection to tenants.",
                "sections": "Varies by State"
            },
            "SENIOR_CITIZENS_2007": {
                "act_name": "Maintenance and Welfare of Parents and Senior Citizens Act, 2007",
                "description": "Provides for maintenance and welfare of parents and senior citizens and establishes old age homes.",
                "sections": "Sections 4, 5, 9, 23"
            },
            "INDUSTRIAL_DISPUTES_1947": {
                "act_name": "Industrial Disputes Act, 1947",
                "description": "Provides machinery and procedure for investigation and settlement of industrial disputes.",
                "sections": "Sections 2A, 25F, 25G, 25N"
            },
            "EVIDENCE_1872": {
                "act_name": "Indian Evidence Act, 1872",
                "description": "Defines and amends law of evidence in India and provides rules for admissibility of evidence.",
                "sections": "Sections 3, 8, 32, 45, 65B"
            }
        }
    
    def _create_domain_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        """Create mappings between domains and relevant legal sections"""
        return {
            "criminal law": {
                "ipc": ["378", "379", "380", "392", "403", "411", "302", "307", "323", "324"],
                "crpc": ["154", "156", "161", "173", "41", "50", "436", "437"],
                "special_acts": ["EVIDENCE_1872"]
            },
            "employment law": {
                "ipc": ["354A", "354", "506"],
                "crpc": ["154", "156", "200", "436"],
                "special_acts": ["POSH_2013", "INDUSTRIAL_DISPUTES_1947"]
            },
            "family law": {
                "ipc": ["498A", "323", "324", "506"],
                "crpc": ["154", "156", "200", "436"],
                "special_acts": ["DV_2005"]
            },
            "cyber crime": {
                "ipc": ["420", "406"],
                "crpc": ["154", "156", "161", "173"],
                "special_acts": ["IT_2000"]
            },
            "tenant rights": {
                "ipc": ["406", "420", "506"],
                "crpc": ["200", "202", "204"],
                "special_acts": ["RENT_CONTROL"]
            },
            "consumer complaint": {
                "ipc": ["420", "406"],
                "crpc": ["200", "202", "204"],
                "special_acts": ["CONSUMER_2019"]
            },
            "elder abuse": {
                "ipc": ["323", "324", "406", "420", "506"],
                "crpc": ["154", "156", "200", "436"],
                "special_acts": ["SENIOR_CITIZENS_2007"]
            }
        }
    
    def get_sections_for_domain(self, domain: str, query: str = "") -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Get IPC, CrPC sections and Special Acts for a domain and query"""
        
        # Get domain-based sections
        mapping = self.domain_mappings.get(domain, {"ipc": [], "crpc": [], "special_acts": []})
        
        # Get IPC sections
        ipc_sections = []
        for section_num in mapping.get("ipc", []):
            if section_num in self.ipc_sections:
                ipc_sections.append({
                    "number": section_num,
                    "title": self.ipc_sections[section_num]["title"],
                    "description": self.ipc_sections[section_num]["description"]
                })
        
        # Get CrPC sections
        crpc_sections = []
        for section_num in mapping.get("crpc", []):
            if section_num in self.crpc_sections:
                crpc_sections.append({
                    "number": section_num,
                    "title": self.crpc_sections[section_num]["title"],
                    "description": self.crpc_sections[section_num]["description"]
                })
        
        # Get Special Acts
        special_acts = []
        for act_key in mapping.get("special_acts", []):
            if act_key in self.special_acts:
                act = self.special_acts[act_key]
                special_acts.append({
                    "act_name": act["act_name"],
                    "description": act["description"],
                    "sections": act["sections"]
                })
        
        # Enhance with query-specific sections
        query_lower = query.lower()
        
        # Add specific sections based on query keywords
        if "stolen" in query_lower or "theft" in query_lower:
            if "378" not in [s["number"] for s in ipc_sections]:
                ipc_sections.append({
                    "number": "378",
                    "title": self.ipc_sections["378"]["title"],
                    "description": self.ipc_sections["378"]["description"]
                })
            if "379" not in [s["number"] for s in ipc_sections]:
                ipc_sections.append({
                    "number": "379", 
                    "title": self.ipc_sections["379"]["title"],
                    "description": self.ipc_sections["379"]["description"]
                })
            if "403" not in [s["number"] for s in ipc_sections]:
                ipc_sections.append({
                    "number": "403",
                    "title": self.ipc_sections["403"]["title"],
                    "description": self.ipc_sections["403"]["description"]
                })
            if "411" not in [s["number"] for s in ipc_sections]:
                ipc_sections.append({
                    "number": "411",
                    "title": self.ipc_sections["411"]["title"],
                    "description": self.ipc_sections["411"]["description"]
                })
        
        if "phone" in query_lower and ("stolen" in query_lower or "hacked" in query_lower):
            # Add IT Act for phone-related crimes
            it_act_found = any("Information Technology Act" in act["act_name"] for act in special_acts)
            if not it_act_found:
                special_acts.append({
                    "act_name": self.special_acts["IT_2000"]["act_name"],
                    "description": self.special_acts["IT_2000"]["description"],
                    "sections": "Section 66C – Identity theft (if SIM/phone data misused), Section 66D – Cheating by impersonation (fraud using stolen phone)"
                })
        
        return ipc_sections[:5], crpc_sections[:5], special_acts[:3]
    
    def process_query_with_sections(self, query_input: LegalQueryInput) -> Dict[str, Any]:
        """Process query and return response with IPC/CrPC/Special Acts sections"""
        
        # Get the original response
        original_response = super().process_query(query_input)
        
        # Get IPC, CrPC sections and Special Acts
        ipc_sections, crpc_sections, special_acts_sections = self.get_sections_for_domain(
            original_response.domain, 
            query_input.user_input
        )
        
        # Create enhanced response dictionary
        enhanced_response = original_response.to_dict()
        enhanced_response['ipc_sections'] = ipc_sections
        enhanced_response['crpc_sections'] = crpc_sections
        enhanced_response['special_acts'] = special_acts_sections
        
        return enhanced_response
    
    def format_enhanced_response(self, response_dict: Dict[str, Any]) -> str:
        """Format the enhanced response with IPC/CrPC/Special Acts sections"""
        
        parts = []
        
        # Original response information
        parts.append(f"📋 Domain: {response_dict['domain'].title()} (Confidence: {response_dict['confidence']:.3f})")
        parts.append(f"⏱️ Timeline: {response_dict['timeline']}")
        parts.append(f"📊 Success Rate: {response_dict.get('success_rate', 'N/A')}")
        parts.append(f"📝 Legal Route: {response_dict['legal_route']}")
        parts.append("")
        
        # Process steps
        if response_dict.get('process_steps'):
            parts.append("📋 Detailed Process Steps:")
            for step in response_dict['process_steps']:
                parts.append(f"{step}")
            parts.append("")
        
        # Constitutional backing
        if response_dict.get('constitutional_backing'):
            parts.append("🏛️ CONSTITUTIONAL & LEGAL BACKING:")
            parts.append(response_dict['constitutional_backing'])
            parts.append("")
        
        # Constitutional articles
        if response_dict.get('constitutional_articles'):
            parts.append("📜 RELEVANT CONSTITUTIONAL ARTICLES:")
            for article in response_dict['constitutional_articles']:
                parts.append(f"🟢 Article {article['article_number']}: {article['title']} ({article.get('relevance_type', 'RELEVANT')})")
                parts.append(f"Summary: {article.get('summary', 'Constitutional provision relevant to this matter')}")
            parts.append("")
        
        # NEW: IPC Sections
        if response_dict.get('ipc_sections'):
            parts.append("### 2. **Relevant IPC Sections (Indian Penal Code, 1860)**")
            parts.append("")
            for section in response_dict['ipc_sections']:
                parts.append(f"* **Section {section['number']}** – {section['title']}")
                parts.append(f"  {section['description']}")
                parts.append("")
        
        # NEW: CrPC Sections
        if response_dict.get('crpc_sections'):
            parts.append("### 3. **Relevant CrPC Sections (Code of Criminal Procedure, 1973)**")
            parts.append("")
            for section in response_dict['crpc_sections']:
                parts.append(f"* **Section {section['number']}** – {section['title']}")
                parts.append(f"  {section['description']}")
                parts.append("")
        
        # NEW: Special Acts
        if response_dict.get('special_acts'):
            parts.append("### 4. **Relevant Special Acts (if applicable)**")
            parts.append("")
            for act in response_dict['special_acts']:
                parts.append(f"* **{act['act_name']}**")
                parts.append(f"  {act['description']}")
                if act.get('sections'):
                    parts.append(f"  Relevant Sections: {act['sections']}")
                parts.append("")
        
        # Session information
        parts.append("* * *")
        parts.append(f"⚡ Response Time: {response_dict.get('response_time', 'N/A')}")
        parts.append(f"🔗 Session ID: {response_dict['session_id']}")
        parts.append("💬 Was this response helpful? You can simply type: 'helpful', 'not helpful', 'good', 'bad', etc.")
        parts.append("Or use: 'feedback <your rating>')")
        
        return "\n".join(parts)


def create_enhanced_legal_agent(feedback_file: str = 'feedback.csv') -> EnhancedLegalAgent:
    """Create and return an enhanced legal agent with IPC/CrPC/Special Acts sections"""
    return EnhancedLegalAgent(feedback_file)


def quick_enhanced_query(user_input: str, feedback: str = None) -> str:
    """Quick function to get enhanced legal response with sections"""
    agent = create_enhanced_legal_agent()
    query = LegalQueryInput(user_input=user_input, feedback=feedback)
    response_dict = agent.process_query_with_sections(query)
    return agent.format_enhanced_response(response_dict)


# Test the enhanced system
if __name__ == "__main__":
    print("🏛️ ENHANCED LEGAL AGENT WITH IPC/CrPC/SPECIAL ACTS")
    print("=" * 60)
    
    # Create enhanced agent
    agent = create_enhanced_legal_agent()
    
    # Test query - stolen phone
    test_query = LegalQueryInput(user_input="My phone is stolen")
    
    print(f"📝 Test Query: \"My phone is stolen\"")
    print("=" * 60)
    
    # Get enhanced response
    response_dict = agent.process_query_with_sections(test_query)
    formatted_response = agent.format_enhanced_response(response_dict)
    
    print(formatted_response)
    
    print(f"\n✅ Enhanced Legal Agent with IPC/CrPC/Special Acts is working!")
    print(f"🎊 All sections are properly integrated into the existing format!")