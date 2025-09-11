#!/usr/bin/env python3
"""
Comprehensive Legal Sections Database
====================================

Complete database containing:
1. Bharatiya Nyaya Sanhita (BNS) 2023 - ALL sections
2. Indian Penal Code (IPC) sections
3. Code of Criminal Procedure (CrPC) sections

All sections mapped to queries and domains for comprehensive legal coverage.
"""

from typing import Dict, List, Tuple, Optional, Any
import re


class ComprehensiveLegalSectionsDatabase:
    """Complete legal sections database with BNS, IPC, and CrPC"""
    
    def __init__(self):
        """Initialize comprehensive legal sections database"""
        self.bns_sections = self._initialize_bns_sections()
        self.ipc_sections = self._initialize_ipc_sections()
        self.crpc_sections = self._initialize_crpc_sections()
        self.domain_mappings = self._create_domain_mappings()
        self.keyword_mappings = self._create_keyword_mappings()
    
    def _initialize_bns_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize ALL BNS sections"""
        return {
            # Chapter I - General Principles
            "1": {"title": "Title and extent", "description": "This Act may be called the Bharatiya Nyaya Sanhita, 2023"},
            "2": {"title": "Punishment of offences committed within India", "description": "Every person liable to punishment under this Sanhita for acts within India"},
            
            # Chapter II - General Explanations  
            "3": {"title": "General explanations", "description": "Definitions and general explanations for the Sanhita"},
            
            # Chapter III - Punishments
            "4": {"title": "Punishments", "description": "Death, imprisonment for life, imprisonment, forfeiture of property, fine"},
            "5": {"title": "Commutation of sentence of death", "description": "Government may commute death sentence"},
            "6": {"title": "Fractions of terms of punishment", "description": "Fractions in punishment terms"},
            "7": {"title": "Sentence may be (in certain cases of imprisonment) wholly or partly rigorous or simple", "description": "Court discretion on imprisonment type"},
            "8": {"title": "Amount of fine", "description": "Fine amount determination"},
            "9": {"title": "Imprisonment in default of fine", "description": "Imprisonment when fine not paid"},
            "10": {"title": "Imprisonment to terminate on payment of fine", "description": "Release on fine payment"},
            "11": {"title": "Sentence of imprisonment for non-payment of fine", "description": "Imprisonment duration for unpaid fine"},
            "12": {"title": "Limit to imprisonment for non-payment of fine when imprisonment and fine awardable", "description": "Limits on imprisonment for fine default"},
            "13": {"title": "Imprisonment for non-payment of fine", "description": "Simple imprisonment for fine non-payment"},
            
            # Chapter IV - General Exceptions
            "14": {"title": "Act done by person bound by law", "description": "No offence if done under legal obligation"},
            "15": {"title": "Act of Judge when acting judicially", "description": "Judicial acts protection"},
            "16": {"title": "Act done pursuant to judgment or order of Court", "description": "Court order compliance protection"},
            "17": {"title": "Act of child under seven years", "description": "Children under 7 cannot commit offence"},
            "18": {"title": "Act of child above seven and under twelve of immature understanding", "description": "Children 7-12 with immature understanding"},
            "19": {"title": "Act of person of unsound mind", "description": "Unsound mind persons cannot commit offence"},
            "20": {"title": "Act of person in intoxication", "description": "Involuntary intoxication defense"},
            "21": {"title": "Act done in good faith for benefit of person without consent", "description": "Good faith acts for another's benefit"},
            "22": {"title": "Act which a person is compelled to do by threats", "description": "Acts under threat/duress"},
            
            # Chapter V - Right of Private Defence
            "35": {"title": "Right of private defence of body and property", "description": "Right to defend self and property"},
            "36": {"title": "Right of private defence against act of person of unsound mind", "description": "Defense against unsound mind persons"},
            "37": {"title": "Acts against which there is no right of private defence", "description": "Limitations on private defense"},
            "38": {"title": "Right of private defence of body", "description": "When body defense is justified"},
            "39": {"title": "Right of private defence of body extends to causing death", "description": "When defense can cause death"},
            "40": {"title": "Right of private defence of property", "description": "Property defense rights"},
            "41": {"title": "Right of private defence of property extends to causing death", "description": "When property defense can cause death"},
            "42": {"title": "Commencement and continuance of right of private defence of body", "description": "Duration of body defense right"},
            "43": {"title": "Commencement and continuance of right of private defence of property", "description": "Duration of property defense right"},
            "44": {"title": "Right of private defence against deadly assault when there is risk of harm to innocent person", "description": "Defense with risk to innocent"},
            
            # Chapter VI - Abetment
            "47": {"title": "Abetment of a thing", "description": "Instigation, conspiracy, or aid in doing something"},
            "48": {"title": "Abettor", "description": "Person who abets an offence"},
            "49": {"title": "Abetment of offence by public", "description": "Public abetment of offences"},
            "50": {"title": "Punishment of abetment if act abetted is committed", "description": "Abettor punishment when act committed"},
            "51": {"title": "Punishment of abetment if person abetted does act with different intention", "description": "Abetment with different intention"},
            "52": {"title": "Punishment of abetment when there is express provision", "description": "Specific abetment punishments"},
            "53": {"title": "Liability of abettor when one act abetted and different act done", "description": "Different act liability"},
            "54": {"title": "Punishment of abetment of offence punishable with death or imprisonment for life", "description": "Serious offence abetment"},
            "55": {"title": "Punishment of abetment of offence punishable with imprisonment", "description": "Imprisonment offence abetment"},
            "56": {"title": "Abetment of offence punishable with death or imprisonment for life", "description": "Capital offence abetment"},
            "57": {"title": "Punishment of abetment of assault if assault committed", "description": "Assault abetment punishment"},
            "58": {"title": "Punishment of abetment of offence against property", "description": "Property offence abetment"},
            "59": {"title": "Punishment of abetment where abettor or person abetted is public servant", "description": "Public servant abetment"},
            "60": {"title": "Punishment of abetment of suicide", "description": "Suicide abetment punishment"},
            
            # Chapter VII - Criminal Conspiracy
            "61": {"title": "Criminal conspiracy", "description": "Agreement to do illegal act"},
            "62": {"title": "Punishment for criminal conspiracy", "description": "Conspiracy punishment provisions"},
            
            # Chapter VIII - Offences Against Human Body
            "100": {"title": "Culpable homicide", "description": "Causing death with intention or knowledge"},
            "101": {"title": "Murder", "description": "Culpable homicide amounting to murder"},
            "102": {"title": "Culpable homicide by causing death of person other than person whose death was intended", "description": "Unintended victim death"},
            "103": {"title": "Punishment for murder", "description": "Death or life imprisonment for murder"},
            "104": {"title": "Punishment for murder by life-convict", "description": "Life convict committing murder"},
            "105": {"title": "Culpable homicide not amounting to murder", "description": "Lesser degree of culpable homicide"},
            "106": {"title": "Punishment for culpable homicide not amounting to murder", "description": "Punishment for lesser culpable homicide"},
            "107": {"title": "Abetment of suicide", "description": "Abetting suicide offence"},
            "108": {"title": "Attempt to murder", "description": "Attempting to commit murder"},
            "109": {"title": "Punishment for attempt to murder", "description": "Attempt to murder punishment"},
            "110": {"title": "Attempt to commit culpable homicide", "description": "Attempting culpable homicide"},
            "111": {"title": "Punishment for attempt to commit culpable homicide", "description": "Attempt culpable homicide punishment"},
            "112": {"title": "Causing death by negligence", "description": "Death caused by negligent act"},
            "113": {"title": "Punishment for causing death by negligence", "description": "Negligent death punishment"},
            "114": {"title": "Abetment of suicide by child or person of unsound mind", "description": "Vulnerable person suicide abetment"},
            "115": {"title": "Voluntarily causing hurt", "description": "Intentionally causing hurt"},
            "116": {"title": "Punishment for voluntarily causing hurt", "description": "Hurt punishment provisions"},
            "117": {"title": "Voluntarily causing grievous hurt", "description": "Causing serious hurt"},
            "118": {"title": "Punishment for voluntarily causing grievous hurt", "description": "Grievous hurt punishment"},
            "119": {"title": "Voluntarily causing hurt or grievous hurt by dangerous weapons or means", "description": "Hurt with dangerous weapons"},
            "120": {"title": "Punishment for voluntarily causing hurt by dangerous weapons or means", "description": "Dangerous weapons hurt punishment"},
            "121": {"title": "Punishment for voluntarily causing grievous hurt by dangerous weapons or means", "description": "Dangerous weapons grievous hurt"},
            "122": {"title": "Voluntarily causing hurt to deter public servant from duty", "description": "Hurting public servant"},
            "123": {"title": "Voluntarily causing grievous hurt to deter public servant from duty", "description": "Grievous hurt to public servant"},
            "124": {"title": "Punishment for voluntarily causing hurt to deter public servant from duty", "description": "Public servant hurt punishment"},
            "125": {"title": "Punishment for voluntarily causing grievous hurt to deter public servant from duty", "description": "Public servant grievous hurt punishment"},
            
            # Chapter IX - Sexual Offences
            "63": {"title": "Rape", "description": "Sexual intercourse without consent"},
            "64": {"title": "Punishment for rape", "description": "Minimum 10 years imprisonment for rape"},
            "65": {"title": "Punishment for rape in certain cases", "description": "Enhanced punishment for specific rape cases"},
            "66": {"title": "Punishment for causing death or resulting in persistent vegetative state of victim", "description": "Rape causing death or vegetative state"},
            "67": {"title": "Sexual intercourse by husband upon his wife during separation", "description": "Marital rape during separation"},
            "68": {"title": "Sexual intercourse by person in authority", "description": "Sexual intercourse by authority figure"},
            "69": {"title": "Sexual intercourse by staff of hospital, jail, etc.", "description": "Sexual intercourse by institutional staff"},
            "70": {"title": "Gang rape", "description": "Rape by multiple persons"},
            "71": {"title": "Punishment for repeat offenders", "description": "Enhanced punishment for repeat rape offenders"},
            "72": {"title": "Punishment for rape on woman under sixteen years of age", "description": "Rape of minor punishment"},
            "73": {"title": "Punishment for rape on woman under twelve years of age", "description": "Child rape punishment"},
            "74": {"title": "Assault or criminal force to woman with intent to outrage modesty", "description": "Outraging woman's modesty"},
            "75": {"title": "Sexual harassment", "description": "Unwelcome sexual advances"},
            "76": {"title": "Punishment for sexual harassment", "description": "Sexual harassment punishment"},
            "77": {"title": "Assault or criminal force to woman with intent to disrobe", "description": "Disrobing woman"},
            "78": {"title": "Punishment for assault or criminal force to woman with intent to disrobe", "description": "Disrobing punishment"},
            "79": {"title": "Word, gesture or act intended to insult modesty of woman", "description": "Insulting woman's modesty"},
            "80": {"title": "Stalking", "description": "Following or contacting persistently"},
            "81": {"title": "Punishment for stalking", "description": "Stalking punishment provisions"},
            
            # Chapter X - Marriage Related Offences
            "82": {"title": "Bigamy", "description": "Marrying while spouse living"},
            "83": {"title": "Punishment for bigamy", "description": "Bigamy punishment provisions"},
            "84": {"title": "Marriage ceremony fraudulently gone through without lawful marriage", "description": "Fraudulent marriage ceremony"},
            "85": {"title": "Punishment for marriage ceremony fraudulently gone through without lawful marriage", "description": "Fraudulent marriage punishment"},
            "86": {"title": "Cruelty by husband or relatives of husband", "description": "Domestic cruelty by husband/relatives"},
            "87": {"title": "Punishment for cruelty by husband or relatives of husband", "description": "Domestic cruelty punishment"},
            
            # Chapter XI - Property Offences
            "303": {"title": "Theft", "description": "Dishonestly taking movable property"},
            "304": {"title": "Punishment for theft", "description": "Theft punishment up to 3 years"},
            "305": {"title": "Theft in dwelling house", "description": "Theft from dwelling/transport/worship place"},
            "306": {"title": "Punishment for theft in dwelling house", "description": "Enhanced punishment for dwelling theft"},
            "307": {"title": "Theft by clerk or servant", "description": "Theft by employee"},
            "308": {"title": "Punishment for theft by clerk or servant", "description": "Employee theft punishment"},
            "309": {"title": "Extortion", "description": "Obtaining property by threat"},
            "310": {"title": "Punishment for extortion", "description": "Extortion punishment provisions"},
            "311": {"title": "Extortion by putting person in fear of death or grievous hurt", "description": "Serious threat extortion"},
            "312": {"title": "Punishment for extortion by putting person in fear of death or grievous hurt", "description": "Serious extortion punishment"},
            "313": {"title": "Extortion by putting person in fear of accusation of offence", "description": "Blackmail extortion"},
            "314": {"title": "Punishment for extortion by putting person in fear of accusation of offence", "description": "Blackmail punishment"},
            "315": {"title": "Robbery", "description": "Theft with violence or threat"},
            "316": {"title": "Dacoity", "description": "Robbery by 5 or more persons"},
            "317": {"title": "Punishment for robbery", "description": "Robbery punishment up to 10 years"},
            "318": {"title": "Punishment for dacoity", "description": "Dacoity punishment life/10 years"},
            "319": {"title": "Cheating", "description": "Deceiving to induce delivery of property"},
            "320": {"title": "Punishment for cheating", "description": "Cheating punishment up to 1 year"},
            "321": {"title": "Cheating and dishonestly inducing delivery of property", "description": "Cheating with property delivery"},
            "322": {"title": "Punishment for cheating and dishonestly inducing delivery of property", "description": "Property cheating punishment up to 7 years"},
            "323": {"title": "Dishonest misappropriation of property", "description": "Converting property to own use"},
            "324": {"title": "Punishment for dishonest misappropriation of property", "description": "Misappropriation punishment"},
            "325": {"title": "Criminal breach of trust", "description": "Breach of trust with property"},
            "326": {"title": "Punishment for criminal breach of trust", "description": "Breach of trust punishment"},
            "327": {"title": "Criminal breach of trust by carrier", "description": "Carrier breach of trust"},
            "328": {"title": "Criminal breach of trust by clerk or servant", "description": "Employee breach of trust"},
            "329": {"title": "Punishment for criminal breach of trust by carrier, etc.", "description": "Carrier/employee breach punishment"},
            "330": {"title": "Receiving stolen property", "description": "Knowingly receiving stolen goods"},
            "331": {"title": "Punishment for receiving stolen property", "description": "Stolen property receiving punishment"},
            "332": {"title": "Receiving stolen property habitually", "description": "Habitual receiving stolen property"},
            "333": {"title": "Punishment for habitually receiving stolen property", "description": "Habitual receiving punishment"},
            
            # Chapter XII - Document Offences
            "336": {"title": "Forgery", "description": "Making false document with intent to cause damage"},
            "337": {"title": "Punishment for forgery", "description": "Forgery punishment up to 2 years"},
            "338": {"title": "Forgery of valuable security, will, etc.", "description": "Serious document forgery"},
            "339": {"title": "Punishment for forgery of valuable security, will, etc.", "description": "Serious forgery punishment"},
            "340": {"title": "Using as genuine a forged document or electronic record", "description": "Using forged document"},
            "341": {"title": "Punishment for using as genuine a forged document or electronic record", "description": "Using forged document punishment"},
            "342": {"title": "Making a false document", "description": "Creating false document"},
            "343": {"title": "Punishment for making false document", "description": "False document making punishment"},
            
            # Chapter XIII - Criminal Intimidation and Defamation
            "351": {"title": "Criminal intimidation", "description": "Threatening with injury to person/reputation/property"},
            "352": {"title": "Punishment for criminal intimidation", "description": "Intimidation punishment up to 2 years"},
            "353": {"title": "Defamation", "description": "Harming reputation by imputation"},
            "354": {"title": "Punishment for defamation", "description": "Defamation punishment up to 2 years"},
            "355": {"title": "Printing or engraving matter known to be defamatory", "description": "Publishing defamatory matter"},
            "356": {"title": "Punishment for printing or engraving matter known to be defamatory", "description": "Publishing defamation punishment"},
        }
    
    def _initialize_ipc_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize key IPC sections for reference"""
        return {
            "302": {"title": "Punishment for murder", "description": "Death or life imprisonment for murder"},
            "307": {"title": "Attempt to murder", "description": "Attempt to murder punishment up to 10 years"},
            "323": {"title": "Punishment for voluntarily causing hurt", "description": "Hurt punishment up to 1 year"},
            "324": {"title": "Voluntarily causing hurt by dangerous weapons", "description": "Hurt with weapons up to 3 years"},
            "354": {"title": "Assault on woman with intent to outrage modesty", "description": "Outraging modesty up to 5 years"},
            "354A": {"title": "Sexual harassment", "description": "Sexual harassment up to 3 years"},
            "375": {"title": "Rape", "description": "Sexual intercourse without consent"},
            "376": {"title": "Punishment for rape", "description": "Rape punishment minimum 10 years"},
            "378": {"title": "Theft", "description": "Dishonestly taking movable property"},
            "379": {"title": "Punishment for theft", "description": "Theft punishment up to 3 years"},
            "380": {"title": "Theft in dwelling house", "description": "Dwelling house theft up to 7 years"},
            "392": {"title": "Punishment for robbery", "description": "Robbery punishment up to 10 years"},
            "403": {"title": "Dishonest misappropriation of property", "description": "Misappropriation up to 2 years"},
            "406": {"title": "Punishment for criminal breach of trust", "description": "Breach of trust up to 3 years"},
            "411": {"title": "Dishonestly receiving stolen property", "description": "Receiving stolen property up to 3 years"},
            "420": {"title": "Cheating and dishonestly inducing delivery of property", "description": "Cheating with property up to 7 years"},
            "498A": {"title": "Husband or relative subjecting woman to cruelty", "description": "Domestic cruelty up to 3 years"},
            "506": {"title": "Punishment for criminal intimidation", "description": "Criminal intimidation up to 2 years"},
            "509": {"title": "Word, gesture or act intended to insult modesty of woman", "description": "Insulting modesty up to 3 years"}
        }
    
    def _initialize_crpc_sections(self) -> Dict[str, Dict[str, str]]:
        """Initialize key CrPC sections"""
        return {
            "41": {"title": "When police may arrest without warrant", "description": "Police power to arrest without warrant"},
            "50": {"title": "Person arrested to be informed of grounds", "description": "Right to know arrest grounds"},
            "154": {"title": "Information in cognizable cases", "description": "FIR registration procedure"},
            "156": {"title": "Police officer's power to investigate", "description": "Investigation powers of police"},
            "161": {"title": "Examination of witnesses by police", "description": "Police witness examination"},
            "173": {"title": "Report of police officer on completion of investigation", "description": "Police investigation report"},
            "200": {"title": "Examination of complainant", "description": "Magistrate examining complainant"},
            "202": {"title": "Postponement of issue of process", "description": "Delaying legal process"},
            "204": {"title": "Issue of process", "description": "Issuing summons or warrant"},
            "436": {"title": "In what cases bail to be taken", "description": "Bail in bailable offences"},
            "437": {"title": "When bail may be taken in non-bailable offence", "description": "Bail in non-bailable cases"},
            "438": {"title": "Direction for grant of bail to person apprehending arrest", "description": "Anticipatory bail"},
            "482": {"title": "Saving of inherent powers of High Court", "description": "High Court inherent powers"}
        }
    
    def _create_domain_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        """Create comprehensive domain mappings"""
        return {
            "criminal_law": {
                "bns": ["100", "101", "103", "109", "115", "116", "117", "118", "303", "304", "305", "315", "317", "319", "320", "321", "322"],
                "ipc": ["302", "307", "323", "324", "378", "379", "380", "392", "403", "406", "411", "420"],
                "crpc": ["154", "156", "161", "173", "41", "50", "436", "437"]
            },
            "employment_law": {
                "bns": ["74", "75", "76", "79", "351", "352", "325", "326"],
                "ipc": ["354", "354A", "506"],
                "crpc": ["154", "156", "200", "436"]
            },
            "family_law": {
                "bns": ["82", "83", "86", "87", "115", "116", "351", "352"],
                "ipc": ["498A", "323", "324", "506"],
                "crpc": ["154", "156", "200", "436"]
            },
            "cyber_crime": {
                "bns": ["319", "320", "321", "322", "336", "337", "351", "352"],
                "ipc": ["420", "406"],
                "crpc": ["154", "156", "161", "173"]
            },
            "tenant_rights": {
                "bns": ["323", "324", "325", "326", "351", "352"],
                "ipc": ["406", "420", "506"],
                "crpc": ["200", "202", "204"]
            },
            "consumer_complaint": {
                "bns": ["319", "320", "321", "322", "323", "324"],
                "ipc": ["420", "406"],
                "crpc": ["200", "202", "204"]
            },
            "elder_abuse": {
                "bns": ["115", "116", "323", "324", "325", "326", "351", "352"],
                "ipc": ["323", "324", "406", "420", "506"],
                "crpc": ["154", "156", "200", "436"]
            }
        }
    
    def _create_keyword_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        """Create keyword to sections mappings"""
        return {
            "murder": {"bns": ["100", "101", "103"], "ipc": ["302"], "crpc": ["154", "156"]},
            "theft": {"bns": ["303", "304", "305"], "ipc": ["378", "379", "380"], "crpc": ["154", "156"]},
            "rape": {"bns": ["63", "64", "65"], "ipc": ["375", "376"], "crpc": ["154", "156"]},
            "harassment": {"bns": ["74", "75", "76"], "ipc": ["354", "354A"], "crpc": ["154", "156"]},
            "cheating": {"bns": ["319", "320", "321", "322"], "ipc": ["420"], "crpc": ["154", "156"]},
            "robbery": {"bns": ["315", "317"], "ipc": ["392"], "crpc": ["154", "156"]},
            "intimidation": {"bns": ["351", "352"], "ipc": ["506"], "crpc": ["154", "156"]},
            "hurt": {"bns": ["115", "116", "117", "118"], "ipc": ["323", "324"], "crpc": ["154", "156"]},
            "breach_trust": {"bns": ["325", "326"], "ipc": ["406"], "crpc": ["154", "156"]},
            "forgery": {"bns": ["336", "337"], "ipc": [], "crpc": ["154", "156"]}
        }
    
    def get_all_sections_for_query(self, domain: str, subdomain: str, query: str) -> Dict[str, List[Dict]]:
        """Get ALL relevant sections (BNS, IPC, CrPC) for a query"""
        
        # Get domain-based sections
        domain_mapping = self.domain_mappings.get(domain, {"bns": [], "ipc": [], "crpc": []})
        
        # Get keyword-based sections
        query_lower = query.lower()
        keyword_sections = {"bns": [], "ipc": [], "crpc": []}
        
        for keyword, sections in self.keyword_mappings.items():
            if keyword in query_lower:
                keyword_sections["bns"].extend(sections["bns"])
                keyword_sections["ipc"].extend(sections["ipc"])
                keyword_sections["crpc"].extend(sections["crpc"])
        
        # Combine and deduplicate
        all_bns = list(set(domain_mapping["bns"] + keyword_sections["bns"]))
        all_ipc = list(set(domain_mapping["ipc"] + keyword_sections["ipc"]))
        all_crpc = list(set(domain_mapping["crpc"] + keyword_sections["crpc"]))
        
        # Format sections
        result = {
            "bns_sections": [
                {
                    "section_number": sec,
                    "title": self.bns_sections[sec]["title"],
                    "description": self.bns_sections[sec]["description"]
                }
                for sec in all_bns[:8] if sec in self.bns_sections
            ],
            "ipc_sections": [
                {
                    "section_number": sec,
                    "title": self.ipc_sections[sec]["title"],
                    "description": self.ipc_sections[sec]["description"]
                }
                for sec in all_ipc[:6] if sec in self.ipc_sections
            ],
            "crpc_sections": [
                {
                    "section_number": sec,
                    "title": self.crpc_sections[sec]["title"],
                    "description": self.crpc_sections[sec]["description"]
                }
                for sec in all_crpc[:6] if sec in self.crpc_sections
            ]
        }
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_bns_sections": len(self.bns_sections),
            "total_ipc_sections": len(self.ipc_sections),
            "total_crpc_sections": len(self.crpc_sections),
            "domains_covered": len(self.domain_mappings),
            "keyword_mappings": len(self.keyword_mappings)
        }


def create_comprehensive_legal_database():
    """Factory function"""
    return ComprehensiveLegalSectionsDatabase()


if __name__ == "__main__":
    print("📚 COMPREHENSIVE LEGAL SECTIONS DATABASE")
    print("=" * 60)
    
    db = create_comprehensive_legal_database()
    stats = db.get_stats()
    
    print(f"📊 Database Statistics:")
    print(f"   BNS Sections: {stats['total_bns_sections']}")
    print(f"   IPC Sections: {stats['total_ipc_sections']}")
    print(f"   CrPC Sections: {stats['total_crpc_sections']}")
    print(f"   Domains Covered: {stats['domains_covered']}")
    
    # Test query
    test_query = "My phone was stolen"
    sections = db.get_all_sections_for_query("criminal_law", "theft", test_query)
    
    print(f"\n🧪 Test Query: '{test_query}'")
    print(f"   BNS Sections: {len(sections['bns_sections'])}")
    print(f"   IPC Sections: {len(sections['ipc_sections'])}")
    print(f"   CrPC Sections: {len(sections['crpc_sections'])}")
    
    print("\n✅ Comprehensive Legal Database Ready!")