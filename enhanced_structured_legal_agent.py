"""
Enhanced Structured Legal Agent - Complete Legal Response System
===============================================================

This module provides a comprehensive legal assistant that generates structured responses
in the format requested:

1. Constitutional Articles
2. Relevant IPC Sections (Indian Penal Code, 1860)
3. Relevant CrPC Sections (Code of Criminal Procedure, 1973)
4. Relevant Special Acts (if applicable)

All sections are presented in simple words but in formal legal style.

Author: Legal Agent Team
Version: 2.0.0 - Structured Response Format
Date: 2025-01-XX
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import json
import datetime
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Import existing components
try:
    from legal_agent import DomainClassifier, LegalRouteEngine, ProcessExplainer, GlossaryEngine, FeedbackSystem
    from constitutional_integration import ConstitutionalAdvisor, create_constitutional_advisor
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False
    print("Warning: Some components not available. Running in basic mode.")


@dataclass
class StructuredLegalResponse:
    """Structured legal response with all required sections"""
    constitutional_articles: List[Dict[str, str]]
    ipc_sections: List[Dict[str, str]]
    crpc_sections: List[Dict[str, str]]
    special_acts: List[Dict[str, str]]
    domain: str
    confidence: float
    session_id: str
    timestamp: str
    raw_query: str
    
    def to_formatted_response(self) -> str:
        """Convert to formatted string response"""
        response_parts = []
        
        response_parts.append("=" * 60)
        response_parts.append("⚖️ LEGAL AI ASSISTANT - STRUCTURED RESPONSE")
        response_parts.append("=" * 60)
        response_parts.append("")
        
        # 1. Constitutional Articles
        response_parts.append("1. **Constitutional Articles**")
        response_parts.append("-" * 30)
        if self.constitutional_articles:
            for article in self.constitutional_articles:
                response_parts.append(f"• Article {article['number']} - {article['title']}")
                response_parts.append(f"  {article['explanation']}")
                response_parts.append("")
        else:
            response_parts.append("• No specific constitutional articles identified for this matter.")
            response_parts.append("")
        
        # 2. IPC Sections
        response_parts.append("2. **Relevant IPC Sections (Indian Penal Code, 1860)**")
        response_parts.append("-" * 50)
        if self.ipc_sections:
            for section in self.ipc_sections:
                response_parts.append(f"• Section {section['number']} – {section['title']}")
                response_parts.append(f"  {section['description']}")
                response_parts.append("")
        else:
            response_parts.append("• No specific IPC sections identified for this matter.")
            response_parts.append("")
        
        # 3. CrPC Sections
        response_parts.append("3. **Relevant CrPC Sections (Code of Criminal Procedure, 1973)**")
        response_parts.append("-" * 55)
        if self.crpc_sections:
            for section in self.crpc_sections:
                response_parts.append(f"• Section {section['number']} – {section['title']}")
                response_parts.append(f"  {section['description']}")
                response_parts.append("")
        else:
            response_parts.append("• No specific CrPC sections identified for this matter.")
            response_parts.append("")
        
        # 4. Special Acts
        response_parts.append("4. **Relevant Special Acts (if applicable)**")
        response_parts.append("-" * 40)
        if self.special_acts:
            for act in self.special_acts:
                response_parts.append(f"• {act['act_name']}")
                response_parts.append(f"  {act['description']}")
                if act.get('sections'):
                    response_parts.append(f"  Relevant Sections: {act['sections']}")
                response_parts.append("")
        else:
            response_parts.append("• No specific special acts identified for this matter.")
            response_parts.append("")
        
        response_parts.append("=" * 60)
        response_parts.append(f"Domain: {self.domain.title()} | Confidence: {self.confidence:.2f}")
        response_parts.append(f"Session: {self.session_id} | Time: {self.timestamp}")
        response_parts.append("=" * 60)
        
        return "\n".join(response_parts)


class LegalCodeDatabase:
    """Database containing IPC, CrPC sections and Special Acts"""
    
    def __init__(self):
        self.ipc_sections = self._initialize_ipc_sections()
        self.crpc_sections = self._initialize_crpc_sections()
        self.special_acts = self._initialize_special_acts()
        self.domain_mappings = self._create_domain_mappings()
    
    def _initialize_ipc_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize IPC sections database"""
        return {
            # Criminal Law - General
            "302": {
                "title": "Punishment for Murder",
                "description": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine."
            },
            "304": {
                "title": "Punishment for Culpable Homicide Not Amounting to Murder",
                "description": "Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life or imprisonment for a term up to ten years."
            },
            "307": {
                "title": "Attempt to Murder",
                "description": "Whoever does any act with intention or knowledge to cause death shall be punished with imprisonment up to ten years."
            },
            "323": {
                "title": "Punishment for Voluntarily Causing Hurt",
                "description": "Whoever voluntarily causes hurt shall be punished with imprisonment up to one year or fine up to one thousand rupees."
            },
            "324": {
                "title": "Voluntarily Causing Hurt by Dangerous Weapons",
                "description": "Whoever voluntarily causes hurt by dangerous weapons or means shall be punished with imprisonment up to three years."
            },
            "354": {
                "title": "Assault or Criminal Force to Woman with Intent to Outrage her Modesty",
                "description": "Whoever assaults or uses criminal force to any woman with intent to outrage her modesty shall be punished with imprisonment up to five years."
            },
            "354A": {
                "title": "Sexual Harassment",
                "description": "A man committing sexual harassment shall be punished with rigorous imprisonment up to three years or fine or both."
            },
            "354B": {
                "title": "Assault or Use of Criminal Force to Woman with Intent to Disrobe",
                "description": "Any man who assaults or uses criminal force to disrobe a woman shall be punished with imprisonment up to seven years."
            },
            "354C": {
                "title": "Voyeurism",
                "description": "Any man who watches or captures image of a woman in private act shall be punished with imprisonment up to seven years."
            },
            "354D": {
                "title": "Stalking",
                "description": "Any man who follows or contacts a woman despite clear indication of disinterest shall be punished with imprisonment up to five years."
            },
            "375": {
                "title": "Rape",
                "description": "A man is said to commit rape if he has sexual intercourse with a woman under circumstances falling under any of the six descriptions."
            },
            "376": {
                "title": "Punishment for Rape",
                "description": "Whoever commits rape shall be punished with rigorous imprisonment for not less than ten years which may extend to imprisonment for life."
            },
            
            # Property Crimes
            "378": {
                "title": "Theft",
                "description": "Whoever intends to take dishonestly any movable property out of possession of any person without consent shall be punished with imprisonment up to three years."
            },
            "379": {
                "title": "Punishment for Theft",
                "description": "Whoever commits theft shall be punished with imprisonment up to three years or fine or both."
            },
            "380": {
                "title": "Theft in Dwelling House",
                "description": "Whoever commits theft in any building used as human dwelling shall be punished with imprisonment up to seven years."
            },
            "392": {
                "title": "Punishment for Robbery",
                "description": "Whoever commits robbery shall be punished with rigorous imprisonment up to ten years and shall also be liable to fine."
            },
            "420": {
                "title": "Cheating and Dishonestly Inducing Delivery of Property",
                "description": "Whoever cheats and thereby dishonestly induces delivery of property shall be punished with imprisonment up to seven years."
            },
            "406": {
                "title": "Punishment for Criminal Breach of Trust",
                "description": "Whoever commits criminal breach of trust shall be punished with imprisonment up to three years or fine or both."
            },
            "409": {
                "title": "Criminal Breach of Trust by Public Servant or Banker",
                "description": "Whoever being a public servant or banker commits criminal breach of trust shall be punished with imprisonment for life or up to ten years."
            },
            
            # Family/Domestic Violence
            "498A": {
                "title": "Husband or Relative of Husband Subjecting Woman to Cruelty",
                "description": "Whoever subjects any woman to cruelty shall be punished with imprisonment up to three years and shall also be liable to fine."
            },
            "494": {
                "title": "Marrying Again During Lifetime of Husband or Wife",
                "description": "Whoever having a husband or wife living marries again shall be punished with imprisonment up to seven years."
            },
            
            # Cyber Crimes
            "66": {
                "title": "Computer Related Offences (IT Act Reference)",
                "description": "Whoever dishonestly or fraudulently does any act referred to in section 43 shall be punished with imprisonment up to three years."
            },
            
            # Public Order
            "141": {
                "title": "Unlawful Assembly",
                "description": "An assembly of five or more persons is designated unlawful assembly if common object is to commit offence."
            },
            "147": {
                "title": "Punishment for Rioting",
                "description": "Whoever is guilty of rioting shall be punished with imprisonment up to two years or fine or both."
            },
            "506": {
                "title": "Punishment for Criminal Intimidation",
                "description": "Whoever commits criminal intimidation shall be punished with imprisonment up to two years or fine or both."
            },
            "509": {
                "title": "Word, Gesture or Act Intended to Insult Modesty of Woman",
                "description": "Whoever intends to insult modesty of any woman shall be punished with simple imprisonment up to three years."
            }
        }
    
    def _initialize_crpc_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize CrPC sections database"""
        return {
            # Arrest and Investigation
            "41": {
                "title": "When Police May Arrest Without Warrant",
                "description": "Any police officer may arrest without warrant any person who commits cognizable offence in his presence or is reasonably suspected of having committed cognizable offence."
            },
            "41A": {
                "title": "Notice of Appearance Before Police Officer",
                "description": "Police officer may issue notice to person to appear before him when arrest is not required for investigation."
            },
            "50": {
                "title": "Person Arrested to be Informed of Grounds of Arrest",
                "description": "Every person arrested shall be informed of grounds of arrest and right to bail if offence is bailable."
            },
            "54": {
                "title": "Examination of Arrested Person by Medical Officer",
                "description": "When person is arrested, he shall be examined by medical officer to record any injuries on his person."
            },
            "57": {
                "title": "Person Arrested Not to be Detained More Than 24 Hours",
                "description": "No police officer shall detain in custody a person arrested without warrant for longer period than 24 hours."
            },
            "60": {
                "title": "Police Officer's Power to Require Bond",
                "description": "Officer in charge of police station may require person to execute bond for keeping peace or good behaviour."
            },
            
            # Bail Provisions
            "436": {
                "title": "In What Cases Bail to be Taken",
                "description": "When any person is arrested or detained without warrant by officer in charge of police station, he shall be released on bail if offence is bailable."
            },
            "437": {
                "title": "When Bail May be Taken in Case of Non-Bailable Offence",
                "description": "When any person accused of non-bailable offence is arrested, officer may release him on bail if such person is under sixteen years of age."
            },
            "438": {
                "title": "Direction for Grant of Bail to Person Apprehending Arrest",
                "description": "When any person has reason to believe that he may be arrested on accusation of non-bailable offence, he may apply to High Court or Court of Session for anticipatory bail."
            },
            "439": {
                "title": "Special Powers of High Court or Court of Session Regarding Bail",
                "description": "High Court or Court of Session may direct that any person accused of any offence be released on bail."
            },
            
            # Investigation
            "154": {
                "title": "Information in Cognizable Cases",
                "description": "Every information relating to commission of cognizable offence shall be reduced to writing and read over to informant."
            },
            "156": {
                "title": "Police Officer's Power to Investigate Cognizable Case",
                "description": "Any officer in charge of police station may investigate any cognizable case without order of Magistrate."
            },
            "161": {
                "title": "Examination of Witnesses by Police",
                "description": "Any police officer making investigation may examine orally any person supposed to be acquainted with facts and circumstances of case."
            },
            "164": {
                "title": "Recording of Confessions and Statements",
                "description": "Any Metropolitan Magistrate or Judicial Magistrate may record any confession or statement made to him in course of investigation."
            },
            "173": {
                "title": "Report of Police Officer on Completion of Investigation",
                "description": "Every investigation shall be completed without unnecessary delay and officer shall submit report to Magistrate."
            },
            
            # Trial Procedures
            "207": {
                "title": "Supply of Copies of Charge and Other Documents to Accused",
                "description": "In any trial before Court of Session, copies of charge, police report and other documents shall be furnished to accused."
            },
            "227": {
                "title": "Discharge",
                "description": "If Judge considers that there is not sufficient ground for proceeding against accused, he shall discharge the accused."
            },
            "228": {
                "title": "Framing of Charge",
                "description": "If Judge is of opinion that there is ground for presuming that accused has committed offence, he shall frame charge against accused."
            },
            "313": {
                "title": "Power to Examine the Accused",
                "description": "Court may examine accused generally on case for purpose of enabling accused to explain any circumstances appearing in evidence against him."
            },
            
            # Complaints and Magistrate Powers
            "200": {
                "title": "Examination of Complainant",
                "description": "Magistrate taking cognizance of offence on complaint shall examine complainant and witnesses present on oath."
            },
            "202": {
                "title": "Postponement of Issue of Process",
                "description": "Magistrate may postpone issue of process against accused and direct investigation to be made by police officer or other person."
            },
            "204": {
                "title": "Issue of Process",
                "description": "If Magistrate is satisfied that there is sufficient ground for proceeding, he shall issue summons or warrant for causing accused to appear before him."
            }
        }
    
    def _initialize_special_acts(self) -> Dict[str, Dict[str, Any]]:
        """Initialize Special Acts database"""
        return {
            # Women Protection
            "POSH_2013": {
                "act_name": "Prevention of Sexual Harassment at Workplace Act, 2013",
                "description": "Provides protection against sexual harassment of women at workplace and for prevention and redressal of complaints.",
                "sections": "Sections 3, 4, 9, 11, 13",
                "applicability": ["employment_law", "workplace_harassment", "sexual_harassment"]
            },
            "DV_2005": {
                "act_name": "Protection of Women from Domestic Violence Act, 2005",
                "description": "Provides for more effective protection of rights of women guaranteed under Constitution who are victims of violence of any kind.",
                "sections": "Sections 3, 12, 18, 19, 20",
                "applicability": ["family_law", "domestic_violence", "women_protection"]
            },
            "DOWRY_1961": {
                "act_name": "Dowry Prohibition Act, 1961",
                "description": "Prohibits giving or taking of dowry and provides punishment for dowry-related offences.",
                "sections": "Sections 3, 4, 6",
                "applicability": ["family_law", "dowry", "marriage"]
            },
            
            # Consumer Protection
            "CONSUMER_2019": {
                "act_name": "Consumer Protection Act, 2019",
                "description": "Provides for protection of interests of consumers and establishes authorities for timely and effective administration.",
                "sections": "Sections 2, 35, 59, 87",
                "applicability": ["consumer_complaint", "defective_goods", "unfair_trade"]
            },
            
            # Property and Tenancy
            "RERA_2016": {
                "act_name": "Real Estate (Regulation and Development) Act, 2016",
                "description": "Establishes Real Estate Regulatory Authority for regulation and promotion of real estate sector.",
                "sections": "Sections 12, 18, 31, 43",
                "applicability": ["tenant_rights", "property_dispute", "real_estate"]
            },
            "RENT_CONTROL": {
                "act_name": "Rent Control Act (State-specific)",
                "description": "Regulates renting of residential and commercial premises and provides protection to tenants.",
                "sections": "Varies by State",
                "applicability": ["tenant_rights", "eviction", "rent_dispute"]
            },
            
            # Cyber Crime
            "IT_2000": {
                "act_name": "Information Technology Act, 2000",
                "description": "Provides legal framework for electronic governance and e-commerce and addresses cyber crimes.",
                "sections": "Sections 43, 66, 66A, 66B, 66C, 66D, 67, 72",
                "applicability": ["cyber_crime", "online_fraud", "hacking", "data_theft"]
            },
            
            # Employment
            "INDUSTRIAL_DISPUTES_1947": {
                "act_name": "Industrial Disputes Act, 1947",
                "description": "Provides machinery and procedure for investigation and settlement of industrial disputes.",
                "sections": "Sections 2A, 25F, 25G, 25N",
                "applicability": ["employment_law", "wrongful_termination", "industrial_dispute"]
            },
            "MINIMUM_WAGES_1948": {
                "act_name": "Minimum Wages Act, 1948",
                "description": "Provides for fixing minimum rates of wages in certain employments.",
                "sections": "Sections 3, 5, 22, 25",
                "applicability": ["employment_law", "wage_dispute", "salary_issues"]
            },
            "PAYMENT_WAGES_1936": {
                "act_name": "Payment of Wages Act, 1936",
                "description": "Regulates payment of wages to certain classes of persons employed in industry.",
                "sections": "Sections 5, 7, 15, 20",
                "applicability": ["employment_law", "salary_delay", "wage_deduction"]
            },
            
            # Senior Citizens
            "SENIOR_CITIZENS_2007": {
                "act_name": "Maintenance and Welfare of Parents and Senior Citizens Act, 2007",
                "description": "Provides for maintenance and welfare of parents and senior citizens and establishes old age homes.",
                "sections": "Sections 4, 5, 9, 23",
                "applicability": ["elder_abuse", "senior_citizen_rights", "maintenance"]
            },
            
            # Immigration
            "CITIZENSHIP_1955": {
                "act_name": "Citizenship Act, 1955",
                "description": "Provides for acquisition and determination of Indian citizenship.",
                "sections": "Sections 3, 4, 5, 6, 7",
                "applicability": ["immigration_law", "citizenship", "naturalization"]
            },
            "PASSPORT_1967": {
                "act_name": "Passport Act, 1967",
                "description": "Provides for issue of passports and travel documents and regulates departure from India.",
                "sections": "Sections 3, 6, 10, 12",
                "applicability": ["immigration_law", "passport", "travel_document"]
            },
            
            # Evidence and Procedure
            "EVIDENCE_1872": {
                "act_name": "Indian Evidence Act, 1872",
                "description": "Defines and amends law of evidence in India and provides rules for admissibility of evidence.",
                "sections": "Sections 3, 8, 32, 45, 65B",
                "applicability": ["criminal_law", "civil_law", "evidence", "proof"]
            },
            
            # Contract Law
            "CONTRACT_1872": {
                "act_name": "Indian Contract Act, 1872",
                "description": "Defines and amends certain parts of law relating to contracts.",
                "sections": "Sections 10, 19, 23, 73, 124",
                "applicability": ["contract_dispute", "breach_of_contract", "agreement"]
            }
        }
    
    def _create_domain_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        """Create mappings between domains and relevant legal sections"""
        return {
            "employment_law": {
                "ipc": ["354A", "354", "506", "323", "324"],
                "crpc": ["154", "156", "200", "202", "436"],
                "special_acts": ["POSH_2013", "INDUSTRIAL_DISPUTES_1947", "MINIMUM_WAGES_1948", "PAYMENT_WAGES_1936"]
            },
            "family_law": {
                "ipc": ["498A", "494", "323", "324", "506"],
                "crpc": ["154", "156", "200", "436", "438"],
                "special_acts": ["DV_2005", "DOWRY_1961"]
            },
            "criminal_law": {
                "ipc": ["302", "304", "307", "323", "324", "354", "375", "376", "378", "379", "392", "420"],
                "crpc": ["41", "50", "54", "57", "154", "156", "161", "173", "436", "437", "438"],
                "special_acts": ["EVIDENCE_1872"]
            },
            "cyber_crime": {
                "ipc": ["420", "406", "509"],
                "crpc": ["154", "156", "161", "173", "200"],
                "special_acts": ["IT_2000"]
            },
            "tenant_rights": {
                "ipc": ["406", "420", "506"],
                "crpc": ["200", "202", "204"],
                "special_acts": ["RENT_CONTROL", "RERA_2016", "CONTRACT_1872"]
            },
            "consumer_complaint": {
                "ipc": ["420", "406"],
                "crpc": ["200", "202", "204"],
                "special_acts": ["CONSUMER_2019", "CONTRACT_1872"]
            },
            "elder_abuse": {
                "ipc": ["323", "324", "406", "420", "506"],
                "crpc": ["154", "156", "200", "436"],
                "special_acts": ["SENIOR_CITIZENS_2007"]
            },
            "immigration_law": {
                "ipc": [],
                "crpc": ["200", "202"],
                "special_acts": ["CITIZENSHIP_1955", "PASSPORT_1967"]
            },
            "personal_injury": {
                "ipc": ["323", "324", "307", "279"],
                "crpc": ["154", "156", "161", "173"],
                "special_acts": ["EVIDENCE_1872"]
            },
            "contract_dispute": {
                "ipc": ["420", "406"],
                "crpc": ["200", "202", "204"],
                "special_acts": ["CONTRACT_1872", "EVIDENCE_1872"]
            }
        }
    
    def get_sections_for_domain(self, domain: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Get IPC, CrPC sections and Special Acts for a domain"""
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
        
        return ipc_sections, crpc_sections, special_acts
    
    def search_by_keywords(self, query: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Search sections by keywords in query"""
        query_lower = query.lower()
        
        # Keywords mapping for better search
        keyword_mappings = {
            "harassment": ["354A", "354", "509"],
            "sexual": ["354A", "354B", "354C", "375", "376"],
            "theft": ["378", "379", "380"],
            "fraud": ["420", "406"],
            "domestic violence": ["498A", "323", "324"],
            "murder": ["302", "304", "307"],
            "cyber": ["66"],
            "stalking": ["354D"],
            "rape": ["375", "376"],
            "dowry": ["498A"],
            "cheating": ["420"],
            "assault": ["323", "324", "354"]
        }
        
        relevant_ipc = set()
        for keyword, sections in keyword_mappings.items():
            if keyword in query_lower:
                relevant_ipc.update(sections)
        
        # Build response
        ipc_sections = []
        for section_num in relevant_ipc:
            if section_num in self.ipc_sections:
                ipc_sections.append({
                    "number": section_num,
                    "title": self.ipc_sections[section_num]["title"],
                    "description": self.ipc_sections[section_num]["description"]
                })
        
        # Default CrPC sections for investigation and procedure
        default_crpc = ["154", "156", "200", "436"] if relevant_ipc else []
        crpc_sections = []
        for section_num in default_crpc:
            if section_num in self.crpc_sections:
                crpc_sections.append({
                    "number": section_num,
                    "title": self.crpc_sections[section_num]["title"],
                    "description": self.crpc_sections[section_num]["description"]
                })
        
        # Special acts based on keywords
        special_acts = []
        if "harassment" in query_lower and ("work" in query_lower or "office" in query_lower):
            special_acts.append({
                "act_name": self.special_acts["POSH_2013"]["act_name"],
                "description": self.special_acts["POSH_2013"]["description"],
                "sections": self.special_acts["POSH_2013"]["sections"]
            })
        
        if "domestic" in query_lower and "violence" in query_lower:
            special_acts.append({
                "act_name": self.special_acts["DV_2005"]["act_name"],
                "description": self.special_acts["DV_2005"]["description"],
                "sections": self.special_acts["DV_2005"]["sections"]
            })
        
        return ipc_sections, crpc_sections, special_acts


class EnhancedStructuredLegalAgent:
    """Enhanced Legal Agent with structured response format"""
    
    def __init__(self, feedback_file: str = 'feedback.csv'):
        """Initialize the enhanced structured legal agent"""
        
        # Initialize legal code database
        self.legal_db = LegalCodeDatabase()
        
        # Initialize existing components if available
        if COMPONENTS_AVAILABLE:
            self.domain_classifier = DomainClassifier()
            self.constitutional_advisor = create_constitutional_advisor()
            self.feedback_system = FeedbackSystem(feedback_file)
            self.components_available = True
        else:
            self.components_available = False
            print("Running in basic mode without advanced components")
    
    def process_structured_query(self, user_query: str, session_id: str = None) -> StructuredLegalResponse:
        """Process query and return structured legal response"""
        
        # Generate session ID and timestamp
        if not session_id:
            session_id = self._generate_session_id()
        timestamp = datetime.datetime.now().isoformat()
        
        # Classify domain if components available
        if self.components_available:
            domain, confidence = self.domain_classifier.classify(user_query)
        else:
            domain, confidence = self._basic_domain_classification(user_query)
        
        # Get constitutional articles
        constitutional_articles = self._get_constitutional_articles(domain, user_query)
        
        # Get legal sections based on domain and query
        if domain != "unknown":
            ipc_sections, crpc_sections, special_acts = self.legal_db.get_sections_for_domain(domain)
        else:
            ipc_sections, crpc_sections, special_acts = self.legal_db.search_by_keywords(user_query)
        
        # Enhance with keyword-based search for better coverage
        keyword_ipc, keyword_crpc, keyword_special = self.legal_db.search_by_keywords(user_query)
        
        # Merge results (avoid duplicates)
        ipc_sections = self._merge_sections(ipc_sections, keyword_ipc)
        crpc_sections = self._merge_sections(crpc_sections, keyword_crpc)
        special_acts = self._merge_acts(special_acts, keyword_special)
        
        # Create structured response
        response = StructuredLegalResponse(
            constitutional_articles=constitutional_articles,
            ipc_sections=ipc_sections[:5],  # Limit to top 5
            crpc_sections=crpc_sections[:5],  # Limit to top 5
            special_acts=special_acts[:3],   # Limit to top 3
            domain=domain,
            confidence=confidence,
            session_id=session_id,
            timestamp=timestamp,
            raw_query=user_query
        )
        
        return response
    
    def _get_constitutional_articles(self, domain: str, query: str) -> List[Dict[str, str]]:
        """Get constitutional articles with explanations"""
        
        if not self.components_available:
            return self._basic_constitutional_articles(domain)
        
        try:
            constitutional_info = self.constitutional_advisor.get_constitutional_backing(domain, query)
            articles = []
            
            if constitutional_info.get('articles'):
                for article in constitutional_info['articles'][:3]:  # Limit to top 3
                    articles.append({
                        "number": article['article_number'],
                        "title": article['title'],
                        "explanation": article.get('content_summary', 'Constitutional provision relevant to this matter.')
                    })
            elif constitutional_info.get('relevant_articles'):
                for article in constitutional_info['relevant_articles'][:3]:
                    articles.append({
                        "number": article.article_number,
                        "title": article.clean_title,
                        "explanation": article.summary or 'Constitutional provision relevant to this matter.'
                    })
            
            return articles
            
        except Exception as e:
            print(f"Error getting constitutional articles: {e}")
            return self._basic_constitutional_articles(domain)
    
    def _basic_constitutional_articles(self, domain: str) -> List[Dict[str, str]]:
        """Basic constitutional articles mapping"""
        
        basic_mappings = {
            "employment_law": [
                {"number": "14", "title": "Right to Equality", "explanation": "Ensures equal treatment in employment matters without discrimination."},
                {"number": "19", "title": "Right to Freedom", "explanation": "Protects right to practice any profession or carry on any trade or business."},
                {"number": "21", "title": "Right to Life and Personal Liberty", "explanation": "Includes right to livelihood and dignified working conditions."}
            ],
            "family_law": [
                {"number": "14", "title": "Right to Equality", "explanation": "Ensures equal rights for all family members regardless of gender."},
                {"number": "15", "title": "Prohibition of Discrimination", "explanation": "Prohibits discrimination on grounds of sex in family matters."},
                {"number": "21", "title": "Right to Life and Personal Liberty", "explanation": "Protects personal liberty and dignity in family relationships."}
            ],
            "criminal_law": [
                {"number": "20", "title": "Protection in Respect of Conviction", "explanation": "Protects against double jeopardy and self-incrimination."},
                {"number": "21", "title": "Right to Life and Personal Liberty", "explanation": "Fundamental right to life and protection from arbitrary arrest."},
                {"number": "22", "title": "Protection Against Arrest", "explanation": "Right to be informed of grounds of arrest and right to legal representation."}
            ],
            "cyber_crime": [
                {"number": "19", "title": "Right to Freedom of Speech", "explanation": "Protects freedom of expression while preventing misuse in digital space."},
                {"number": "21", "title": "Right to Privacy", "explanation": "Protects personal data and privacy in digital communications."}
            ],
            "tenant_rights": [
                {"number": "19", "title": "Right to Freedom", "explanation": "Includes right to reside and settle in any part of India."},
                {"number": "21", "title": "Right to Life", "explanation": "Right to shelter as part of right to life with dignity."},
                {"number": "300A", "title": "Right to Property", "explanation": "No person shall be deprived of property save by authority of law."}
            ]
        }
        
        return basic_mappings.get(domain, [
            {"number": "14", "title": "Right to Equality", "explanation": "Fundamental right to equality before law and equal protection of laws."},
            {"number": "21", "title": "Right to Life and Personal Liberty", "explanation": "Most comprehensive fundamental right protecting life and personal liberty."}
        ])
    
    def _basic_domain_classification(self, query: str) -> Tuple[str, float]:
        """Basic domain classification without ML components"""
        
        query_lower = query.lower()
        
        domain_keywords = {
            "employment_law": ["work", "job", "office", "employer", "salary", "fired", "harassment", "workplace"],
            "family_law": ["divorce", "marriage", "husband", "wife", "domestic", "child", "custody"],
            "criminal_law": ["murder", "theft", "assault", "rape", "crime", "police", "arrest"],
            "cyber_crime": ["online", "internet", "hacking", "cyber", "digital", "computer", "phone"],
            "tenant_rights": ["landlord", "rent", "deposit", "eviction", "tenant", "house"],
            "consumer_complaint": ["product", "service", "defective", "warranty", "refund", "consumer"],
            "elder_abuse": ["elderly", "senior", "old", "parent", "abuse", "neglect"]
        }
        
        best_domain = "unknown"
        best_score = 0
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > best_score:
                best_score = score
                best_domain = domain
        
        confidence = min(best_score / 3.0, 1.0)  # Normalize confidence
        return best_domain, confidence
    
    def _merge_sections(self, list1: List[Dict], list2: List[Dict]) -> List[Dict]:
        """Merge two lists of sections avoiding duplicates"""
        
        seen_numbers = set()
        merged = []
        
        for section in list1 + list2:
            if section["number"] not in seen_numbers:
                merged.append(section)
                seen_numbers.add(section["number"])
        
        return merged
    
    def _merge_acts(self, list1: List[Dict], list2: List[Dict]) -> List[Dict]:
        """Merge two lists of acts avoiding duplicates"""
        
        seen_names = set()
        merged = []
        
        for act in list1 + list2:
            if act["act_name"] not in seen_names:
                merged.append(act)
                seen_names.add(act["act_name"])
        
        return merged
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = np.random.randint(1000, 9999)
        return f"structured_session_{timestamp}_{random_suffix}"
    
    def get_formatted_response(self, user_query: str) -> str:
        """Get formatted string response for user query"""
        
        response = self.process_structured_query(user_query)
        return response.to_formatted_response()


# Convenience functions
def create_structured_legal_agent() -> EnhancedStructuredLegalAgent:
    """Create and return structured legal agent"""
    return EnhancedStructuredLegalAgent()


def get_structured_legal_advice(user_query: str) -> str:
    """Quick function to get structured legal advice"""
    agent = create_structured_legal_agent()
    return agent.get_formatted_response(user_query)


# Test the system
if __name__ == "__main__":
    print("🏛️ ENHANCED STRUCTURED LEGAL AGENT")
    print("=" * 60)
    
    agent = create_structured_legal_agent()
    
    # Test cases
    test_queries = [
        "My coworker is sexually harassing me at workplace",
        "My landlord is not returning my security deposit",
        "I want to file for divorce from my husband",
        "Someone stole my phone and money",
        "My employer fired me without notice",
        "I received a defective product and want refund"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {query}")
        print('='*60)
        
        response = agent.get_formatted_response(query)
        print(response)
        
        if i < len(test_queries):
            input("\nPress Enter to continue to next test case...")
    
    print(f"\n✅ Enhanced Structured Legal Agent is ready!")
    print(f"📊 Database contains:")
    print(f"   • {len(agent.legal_db.ipc_sections)} IPC Sections")
    print(f"   • {len(agent.legal_db.crpc_sections)} CrPC Sections") 
    print(f"   • {len(agent.legal_db.special_acts)} Special Acts")
    print(f"   • {len(agent.legal_db.domain_mappings)} Legal Domains")