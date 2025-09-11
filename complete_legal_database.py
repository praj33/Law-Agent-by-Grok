#!/usr/bin/env python3
"""
Complete Legal Database - ALL Sections for ANY Query Type
========================================================
"""

from typing import Dict, List, Tuple, Optional, Any
import json
import os
from datetime import datetime


class CompleteLegalDatabase:
    """Complete legal database with ALL sections for ANY query type"""
    
    def __init__(self):
        self.bns_sections = self._init_all_bns()
        self.ipc_sections = self._init_all_ipc()
        self.crpc_sections = self._init_all_crpc()
        self.keyword_mappings = self._init_keywords()
        self.feedback_data = self._load_feedback()
    
    def _init_all_bns(self):
        # Import the complete BNS database
        from bharatiya_nyaya_sanhita import create_bns_database
        bns_db = create_bns_database()
        return bns_db.bns_sections
    
    def _init_all_ipc(self):
        # Import the complete IPC database
        from complete_ipc_sections_full import create_complete_ipc_database
        ipc_db = create_complete_ipc_database()
        return ipc_db
    
    def _init_all_crpc(self):
        # Import the complete CrPC database
        from complete_crpc_sections_full import create_complete_crpc_database
        crpc_db = create_complete_crpc_database()
        return crpc_db
    
    def _init_keywords(self):
        return {
            # Violence & Murder
            "murder": {"bns": ["100", "101", "103"], "ipc": ["302"], "crpc": ["154", "156"]},
            "kill": {"bns": ["100", "101", "103"], "ipc": ["302"], "crpc": ["154", "156"]},
            "death": {"bns": ["100", "101", "103"], "ipc": ["302", "304"], "crpc": ["154", "156"]},
            "kidnap": {"bns": ["137", "141", "143"], "ipc": ["363", "364A"], "crpc": ["154", "156"]},
            "hurt": {"bns": ["115", "116", "117", "118"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            
            # Drug Crimes
            "drug": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "drugs": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "narcotic": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "cocaine": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "heroin": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "cannabis": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "marijuana": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "smuggling": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173"]},
            "airport": {"bns": ["319", "320", "322"], "ipc": ["420", "406"], "crpc": ["154", "156", "161", "173", "41", "57"]},
            "assault": {"bns": ["115", "116", "117", "118"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            "beat": {"bns": ["115", "116"], "ipc": ["323"], "crpc": ["154", "156"]},
            "attack": {"bns": ["115", "116"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            
            # Sexual Crimes
            "rape": {"bns": ["63", "64", "70"], "ipc": ["375", "376"], "crpc": ["154", "164"]},
            "sexual": {"bns": ["63", "74", "75"], "ipc": ["354", "375"], "crpc": ["154", "156"]},
            "harassment": {"bns": ["75", "76", "351"], "ipc": ["354A", "506"], "crpc": ["154", "156"]},
            "modesty": {"bns": ["74", "79"], "ipc": ["354", "509"], "crpc": ["154", "156"]},
            "stalking": {"bns": ["80", "81"], "ipc": ["354D"], "crpc": ["154", "156"]},
            
            # Property Crimes
            "theft": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            "steal": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "stolen": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "rob": {"bns": ["315", "317"], "ipc": ["392"], "crpc": ["154", "156"]},
            "robbery": {"bns": ["315", "317"], "ipc": ["392", "393"], "crpc": ["154", "156"]},
            "cheat": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "fraud": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "extortion": {"bns": ["309", "310"], "ipc": ["383", "384"], "crpc": ["154", "156"]},
            "blackmail": {"bns": ["309", "310"], "ipc": ["383", "384"], "crpc": ["154", "156"]},
            
            # Document Crimes
            "forgery": {"bns": ["336", "337"], "ipc": ["463", "465"], "crpc": ["154", "156"]},
            "fake": {"bns": ["336", "337"], "ipc": ["463", "465"], "crpc": ["154", "156"]},
            
            # Intimidation
            "threat": {"bns": ["351", "352"], "ipc": ["503", "506"], "crpc": ["154", "156"]},
            "intimidation": {"bns": ["351", "352"], "ipc": ["503", "506"], "crpc": ["154", "156"]},
            "defamation": {"bns": ["356", "357"], "ipc": ["499", "500"], "crpc": ["200", "202"]},
            
            # Family
            "husband": {"bns": ["86", "87"], "ipc": ["498A"], "crpc": ["154", "156"]},
            "wife": {"bns": ["86", "87"], "ipc": ["498A"], "crpc": ["154", "156"]},
            "domestic": {"bns": ["86", "87"], "ipc": ["498A"], "crpc": ["154", "156"]},
            "cruelty": {"bns": ["86", "87"], "ipc": ["498A"], "crpc": ["154", "156"]},
            "bigamy": {"bns": ["82"], "ipc": ["494"], "crpc": ["200", "202"]},
            
            # Common Objects
            "phone": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "mobile": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "computer": {"bns": ["303", "304"], "ipc": ["378", "420"], "crpc": ["154", "156"]},
            "money": {"bns": ["303", "304", "319", "320"], "ipc": ["378", "420"], "crpc": ["154", "156"]},
            "car": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "bike": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            
            # Cyber
            "hack": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "cyber": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "online": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "internet": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            
            # Employment
            "job": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            "work": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            "boss": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            "fire": {"bns": ["351", "352"], "ipc": ["506"], "crpc": ["200", "202"]},
            
            # Age groups
            "child": {"bns": ["137", "63"], "ipc": ["363", "376"], "crpc": ["154", "164"]},
            "minor": {"bns": ["137", "63"], "ipc": ["363", "376"], "crpc": ["154", "164"]},
            "elderly": {"bns": ["115", "323"], "ipc": ["323", "403"], "crpc": ["154", "156"]},
            
            # Places
            "house": {"bns": ["305"], "ipc": ["380"], "crpc": ["154", "156"]},
            "school": {"bns": ["74", "75"], "ipc": ["354"], "crpc": ["154", "156"]},
            "office": {"bns": ["74", "75"], "ipc": ["354A"], "crpc": ["154", "156"]},
            
            # Transport
            "bus": {"bns": ["74", "303"], "ipc": ["354", "378"], "crpc": ["154", "156"]},
            "train": {"bns": ["74", "303"], "ipc": ["354", "378"], "crpc": ["154", "156"]},
            "taxi": {"bns": ["303", "315"], "ipc": ["378", "392"], "crpc": ["154", "156"]},
            
            # Add comprehensive keyword mappings for all expanded domains
            # Cyber Crime
            "hacking": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "phishing": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "malware": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "data breach": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "identity theft": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            "cyberbullying": {"bns": ["319", "320"], "ipc": ["420"], "crpc": ["154", "156"]},
            
            # Employment Law
            "employment": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            "termination": {"bns": ["351", "352"], "ipc": ["506"], "crpc": ["200", "202"]},
            "discrimination": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            "salary": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            "wage": {"bns": ["75", "76"], "ipc": ["354A"], "crpc": ["154", "156"]},
            
            # Family Law
            "family": {"bns": ["86", "87"], "ipc": ["498A"], "crpc": ["154", "156"]},
            "divorce": {"bns": ["82", "86"], "ipc": ["494", "498A"], "crpc": ["200", "202"]},
            "custody": {"bns": ["86", "87"], "ipc": ["498A"], "crpc": ["154", "156"]},
            
            # Financial Crimes
            "embezzlement": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "money laundering": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "tax evasion": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "insider trading": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "bribery": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "corruption": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            
            # Consumer Protection
            "defective": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "product": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "warranty": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "refund": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            "consumer": {"bns": ["303", "304"], "ipc": ["378", "379"], "crpc": ["154", "156"]},
            
            # Medical Law
            "medical": {"bns": ["115", "116", "117"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            "doctor": {"bns": ["115", "116", "117"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            "hospital": {"bns": ["115", "116", "117"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            "malpractice": {"bns": ["115", "116", "117"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            "negligence": {"bns": ["115", "116", "117"], "ipc": ["323", "325"], "crpc": ["154", "156"]},
            
            # Real Estate Law
            "property": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            "land": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            "building": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            "construction": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            "builder": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            
            # Contract Law
            "contract": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "breach": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "agreement": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            
            # Intellectual Property
            "patent": {"bns": ["336", "337"], "ipc": ["463", "465"], "crpc": ["154", "156"]},
            "trademark": {"bns": ["336", "337"], "ipc": ["463", "465"], "crpc": ["154", "156"]},
            "copyright": {"bns": ["336", "337"], "ipc": ["463", "465"], "crpc": ["154", "156"]},
            "infringement": {"bns": ["336", "337"], "ipc": ["463", "465"], "crpc": ["154", "156"]},
            
            # Environmental Law
            "pollution": {"bns": ["125"], "ipc": ["278", "279"], "crpc": ["154", "156"]},
            "environment": {"bns": ["125"], "ipc": ["278", "279"], "crpc": ["154", "156"]},
            "waste": {"bns": ["125"], "ipc": ["278", "279"], "crpc": ["154", "156"]},
            
            # Tax Law
            "tax": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "gst": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "income tax": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            
            # Immigration Law
            "visa": {"bns": ["151", "152"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "passport": {"bns": ["151", "152"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "immigration": {"bns": ["151", "152"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            
            # Corporate Law
            "company": {"bns": ["111", "112"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "corporate": {"bns": ["111", "112"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "shareholder": {"bns": ["111", "112"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            
            # Banking Law
            "bank": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "loan": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "cheque": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            
            # Insurance Law
            "insurance": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "policy": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "claim": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            
            # Education Law
            "education": {"bns": ["74", "75"], "ipc": ["354", "354A"], "crpc": ["154", "156"]},
            "student": {"bns": ["74", "75"], "ipc": ["354", "354A"], "crpc": ["154", "156"]},
            
            # Transport Law
            "vehicle": {"bns": ["303", "304", "315"], "ipc": ["378", "379", "392"], "crpc": ["154", "156"]},
            "traffic": {"bns": ["303", "304", "315"], "ipc": ["378", "379", "392"], "crpc": ["154", "156"]},
            "driving": {"bns": ["303", "304", "315"], "ipc": ["378", "379", "392"], "crpc": ["154", "156"]},
            
            # Sports Law
            "sports": {"bns": ["111", "112"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "gambling": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            "betting": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": ["154", "156"]},
            
            # Media Law
            "media": {"bns": ["356", "357"], "ipc": ["499", "500"], "crpc": ["200", "202"]},
            "press": {"bns": ["356", "357"], "ipc": ["499", "500"], "crpc": ["200", "202"]},
            
            # Human Rights
            "human rights": {"bns": ["14", "15", "21"], "ipc": ["14", "15", "21"], "crpc": ["154", "156"]},
            "fundamental rights": {"bns": ["14", "15", "21"], "ipc": ["14", "15", "21"], "crpc": ["154", "156"]},
            
            # Administrative Law
            "government": {"bns": ["147", "148"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "public service": {"bns": ["147", "148"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            
            # Constitutional Law
            "constitution": {"bns": ["14", "15", "21"], "ipc": ["14", "15", "21"], "crpc": ["154", "156"]},
            "constitutional": {"bns": ["14", "15", "21"], "ipc": ["14", "15", "21"], "crpc": ["154", "156"]},
            
            # Election Law
            "election": {"bns": ["147", "148"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            "voting": {"bns": ["147", "148"], "ipc": ["121", "122"], "crpc": ["154", "156"]},
            
            # International Law
            "international": {"bns": ["153", "154"], "ipc": ["123", "124"], "crpc": ["154", "156"]},
            "treaty": {"bns": ["153", "154"], "ipc": ["123", "124"], "crpc": ["154", "156"]},
            
            # Additional keywords for comprehensive coverage
            "sedition": {"bns": ["152"], "ipc": ["124A"], "crpc": []},
            "cheating": {"bns": ["319", "320", "321", "322"], "ipc": ["415", "420"], "crpc": []},
            "criminal breach of trust": {"bns": ["319", "320", "321", "322"], "ipc": ["405", "406", "409"], "crpc": []},
            "dacoity": {"bns": ["315", "317"], "ipc": ["395", "396"], "crpc": []},
            "extortion": {"bns": ["309", "310"], "ipc": ["383", "384"], "crpc": []},
            "kidnapping": {"bns": ["137", "138", "140"], "ipc": ["363", "364", "364A", "365"], "crpc": []},
            "assault": {"bns": ["128", "129", "130"], "ipc": ["351", "352", "354", "354A"], "crpc": []},
            "hurt": {"bns": ["114", "115", "116", "117", "118"], "ipc": ["323", "324", "325", "326"], "crpc": []},
            
            # Personal Injury / Motor Vehicle Accident
            "accident": {"bns": ["114", "115", "116", "117", "118", "303", "304", "315"], "ipc": ["323", "324", "325", "326", "378", "379", "392"], "crpc": ["154", "156", "304"]},
            "car accident": {"bns": ["114", "115", "116", "117", "118", "303", "304", "315"], "ipc": ["323", "324", "325", "326", "378", "379", "392"], "crpc": ["154", "156", "304"]},
            "vehicle accident": {"bns": ["114", "115", "116", "117", "118", "303", "304", "315"], "ipc": ["323", "324", "325", "326", "378", "379", "392"], "crpc": ["154", "156", "304"]},
            "motor vehicle": {"bns": ["114", "115", "116", "117", "118", "303", "304", "315"], "ipc": ["323", "324", "325", "326", "378", "379", "392"], "crpc": ["154", "156", "304"]},
            
            # Medical Malpractice
            "medical malpractice": {"bns": ["114", "115", "116", "117", "118"], "ipc": ["323", "324", "325", "326"], "crpc": ["154", "156"]},
            "malpractice": {"bns": ["114", "115", "116", "117", "118"], "ipc": ["323", "324", "325", "326"], "crpc": ["154", "156"]}
        }
    
    def _load_feedback(self):
        try:
            if os.path.exists("feedback_data.json"):
                with open("feedback_data.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"adjustments": {}, "history": []}
    
    def get_all_sections_for_query(self, domain: str, subdomain: str, query: str) -> Dict[str, List[Dict]]:
        """Get ALL sections for ANY query type"""
        
        query_lower = query.lower()
        bns_sections = []
        ipc_sections = []
        crpc_sections = []
        
        # Get keyword-based sections
        for keyword, sections in self.keyword_mappings.items():
            if keyword in query_lower:
                bns_sections.extend(sections.get("bns", []))
                ipc_sections.extend(sections.get("ipc", []))
                crpc_sections.extend(sections.get("crpc", []))
        
        # If no keywords matched, return all sections (this ensures we get all stored sections)
        if not bns_sections and not ipc_sections and not crpc_sections:
            # Return all sections when no specific keywords match
            bns_sections = list(self.bns_sections.keys())
            ipc_sections = list(self.ipc_sections.keys())
            crpc_sections = list(self.crpc_sections.keys())
        
        # Remove duplicates while preserving order
        seen_bns = set()
        unique_bns = []
        for sec in bns_sections:
            if sec not in seen_bns:
                seen_bns.add(sec)
                unique_bns.append(sec)
        bns_sections = unique_bns
        
        seen_ipc = set()
        unique_ipc = []
        for sec in ipc_sections:
            if sec not in seen_ipc:
                seen_ipc.add(sec)
                unique_ipc.append(sec)
        ipc_sections = unique_ipc
        
        seen_crpc = set()
        unique_crpc = []
        for sec in crpc_sections:
            if sec not in seen_crpc:
                seen_crpc.add(sec)
                unique_crpc.append(sec)
        crpc_sections = unique_crpc
        
        # Format sections - NO LIMIT on number of sections returned
        result = {
            "bns_sections": [
                {
                    "section_number": sec,
                    "title": self.bns_sections[sec]["title"],
                    "description": self.bns_sections[sec]["description"]
                }
                for sec in bns_sections if sec in self.bns_sections
            ],
            "ipc_sections": [
                {
                    "section_number": sec,
                    "title": self.ipc_sections[sec]["title"],
                    "description": self.ipc_sections[sec]["description"]
                }
                for sec in ipc_sections if sec in self.ipc_sections
            ],
            "crpc_sections": [
                {
                    "section_number": sec,
                    "title": self.crpc_sections[sec]["title"],
                    "description": self.crpc_sections[sec]["description"]
                }
                for sec in crpc_sections if sec in self.crpc_sections
            ]
        }
        
        return result
    
    def process_feedback(self, query: str, domain: str, subdomain: str, confidence: float, feedback: str, rating: int = 0):
        """Process feedback and adjust confidence"""
        
        key = f"{domain}_{subdomain}"
        adjustment = 0
        
        # Rating-based adjustment
        if rating >= 4:
            adjustment = 0.1
        elif rating <= 2:
            adjustment = -0.1
        
        # Keyword-based adjustment
        feedback_lower = feedback.lower()
        if any(word in feedback_lower for word in ["good", "helpful", "correct", "accurate"]):
            adjustment += 0.05
        elif any(word in feedback_lower for word in ["bad", "wrong", "incorrect", "useless"]):
            adjustment -= 0.05
        
        # Store adjustment
        if key not in self.feedback_data["adjustments"]:
            self.feedback_data["adjustments"][key] = 0
        self.feedback_data["adjustments"][key] += adjustment
        
        # Store feedback history
        self.feedback_data["history"].append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "domain": domain,
            "subdomain": subdomain,
            "feedback": feedback,
            "rating": rating,
            "adjustment": adjustment
        })
        
        # Save to file
        try:
            with open("feedback_data.json", 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except:
            pass
        
        return adjustment
    
    def get_adjusted_confidence(self, domain: str, subdomain: str, original_confidence: float) -> float:
        """Get confidence adjusted based on feedback"""
        key = f"{domain}_{subdomain}"
        adjustment = self.feedback_data["adjustments"].get(key, 0)
        adjusted = original_confidence + adjustment
        return max(0.1, min(1.0, adjusted))
    
    def get_query_history(self) -> List[Dict]:
        """Get stored query history"""
        return self.feedback_data.get("history", [])
    
    def get_stats(self):
        return {
            "total_bns_sections": len(self.bns_sections),
            "total_ipc_sections": len(self.ipc_sections),
            "total_crpc_sections": len(self.crpc_sections),
            "total_sections": len(self.bns_sections) + len(self.ipc_sections) + len(self.crpc_sections),
            "keyword_mappings": len(self.keyword_mappings),
            "feedback_entries": len(self.feedback_data.get("history", []))
        }


def create_complete_legal_database():
    return CompleteLegalDatabase()


if __name__ == "__main__":
    db = create_complete_legal_database()
    stats = db.get_stats()
    print(f"📚 Complete Legal Database Ready!")
    print(f"   BNS: {stats['total_bns_sections']}, IPC: {stats['total_ipc_sections']}, CrPC: {stats['total_crpc_sections']}")
    print(f"   Total: {stats['total_sections']} sections")
    print(f"   Keywords: {stats['keyword_mappings']}")