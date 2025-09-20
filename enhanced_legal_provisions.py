#!/usr/bin/env python3
"""
Enhanced Legal Provisions Engine
===============================

Provides detailed legal provisions including IPC sections, CrPC sections,
constitutional articles, and structured legal processes for each query.
"""

import json
from typing import Dict, List, Any, Optional

class EnhancedLegalProvisionsEngine:
    """Enhanced engine for detailed legal provisions and processes"""
    
    def __init__(self):
        """Initialize the enhanced legal provisions engine"""
        self.legal_provisions = self._load_legal_provisions()
        self.process_templates = self._load_process_templates()
        
    def _load_legal_provisions(self) -> Dict[str, Any]:
        """Load comprehensive legal provisions database"""
        return {
            "criminal_law": {
                "constitutional_articles": [
                    {"number": "21", "title": "Protection of life and personal liberty"},
                    {"number": "20", "title": "Protection against conviction for the same offence twice"},
                    {"number": "22", "title": "Protection against arrest and detention"},
                    {"number": "14", "title": "Right to equality before law"}
                ],
                "ipc_sections": {
                    "theft": [
                        {"section": "378", "title": "Theft (defines theft)"},
                        {"section": "379", "title": "Punishment for theft (up to 3 years imprisonment, fine, or both)"},
                        {"section": "380", "title": "Theft in dwelling house (up to 7 years imprisonment)"}
                    ],
                    "robbery": [
                        {"section": "390", "title": "Robbery (defines robbery)"},
                        {"section": "392", "title": "Punishment for robbery (up to 10 years imprisonment)"},
                        {"section": "394", "title": "Voluntarily causing hurt in committing robbery"}
                    ],
                    "cheating": [
                        {"section": "415", "title": "Cheating (defines cheating)"},
                        {"section": "417", "title": "Punishment for cheating (up to 1 year imprisonment)"},
                        {"section": "420", "title": "Cheating and dishonestly inducing delivery of property"}
                    ],
                    "assault": [
                        {"section": "351", "title": "Assault (defines assault)"},
                        {"section": "352", "title": "Punishment for assault (up to 3 months imprisonment)"},
                        {"section": "354", "title": "Assault or criminal force to woman with intent to outrage modesty"}
                    ],
                    "rape": [
                        {"section": "375", "title": "Rape (defines rape)"},
                        {"section": "376", "title": "Punishment for rape (minimum 10 years imprisonment)"},
                        {"section": "376A", "title": "Punishment for causing death or resulting in persistent vegetative state"}
                    ],
                    "murder": [
                        {"section": "300", "title": "Murder (defines murder)"},
                        {"section": "302", "title": "Punishment for murder (death penalty or life imprisonment)"},
                        {"section": "304", "title": "Punishment for culpable homicide not amounting to murder"}
                    ],
                    "kidnapping": [
                        {"section": "359", "title": "Kidnapping (defines kidnapping)"},
                        {"section": "363", "title": "Punishment for kidnapping (up to 7 years imprisonment)"},
                        {"section": "366", "title": "Kidnapping, abducting or inducing woman to compel marriage"}
                    ]
                },
                "crpc_sections": [
                    {"section": "154", "title": "FIR to be filed at nearest police station"},
                    {"section": "156", "title": "Police officer's power to investigate"},
                    {"section": "173", "title": "Submission of police report"},
                    {"section": "451", "title": "Return of property"},
                    {"section": "41", "title": "When police may arrest without warrant"},
                    {"section": "57", "title": "Person arrested not to be detained more than 24 hours"}
                ]
            },
            
            "cyber_crime": {
                "constitutional_articles": [
                    {"number": "21", "title": "Protection of life and personal liberty (Right to Privacy)"},
                    {"number": "19(1)(a)", "title": "Freedom of speech and expression"},
                    {"number": "14", "title": "Right to equality before law"}
                ],
                "it_act_sections": [
                    {"section": "43", "title": "Penalty for damage to computer, computer system, etc."},
                    {"section": "66", "title": "Computer related offences (hacking)"},
                    {"section": "66B", "title": "Punishment for dishonestly receiving stolen computer resource"},
                    {"section": "66C", "title": "Punishment for identity theft"},
                    {"section": "66D", "title": "Punishment for cheating by personation using computer resource"},
                    {"section": "66E", "title": "Punishment for violation of privacy"},
                    {"section": "67", "title": "Punishment for publishing obscene information"},
                    {"section": "72", "title": "Breach of confidentiality and privacy"}
                ],
                "ipc_sections": {
                    "fraud": [
                        {"section": "420", "title": "Cheating and dishonestly inducing delivery of property"},
                        {"section": "468", "title": "Forgery for purpose of cheating"},
                        {"section": "471", "title": "Using as genuine a forged document"}
                    ]
                },
                "crpc_sections": [
                    {"section": "154", "title": "FIR to be filed at cyber crime cell or nearest police station"},
                    {"section": "156", "title": "Police officer's power to investigate"},
                    {"section": "173", "title": "Submission of police report"}
                ]
            },
            
            "employment_law": {
                "constitutional_articles": [
                    {"number": "19(1)(g)", "title": "Right to practice any profession or carry on any trade or business"},
                    {"number": "21", "title": "Protection of life and personal liberty"},
                    {"number": "14", "title": "Right to equality before law"},
                    {"number": "23", "title": "Prohibition of traffic in human beings and forced labour"}
                ],
                "labour_laws": [
                    {"act": "Payment of Wages Act, 1936", "sections": [
                        {"section": "5", "title": "Fixation of wage periods"},
                        {"section": "7", "title": "Time of payment of wages"},
                        {"section": "15", "title": "Penalty for delayed payment"}
                    ]},
                    {"act": "Industrial Disputes Act, 1947", "sections": [
                        {"section": "2A", "title": "Dismissal, discharge or retrenchment of workmen"},
                        {"section": "25F", "title": "Conditions precedent to retrenchment"},
                        {"section": "25G", "title": "Procedure for retrenchment"}
                    ]},
                    {"act": "Employees' Provident Fund Act, 1952", "sections": [
                        {"section": "7A", "title": "Penalty for default in payment of contribution"},
                        {"section": "14", "title": "Damages for default in payment"}
                    ]}
                ],
                "crpc_sections": [
                    {"section": "200", "title": "Examination of complainant"},
                    {"section": "202", "title": "Postponement of issue of process"}
                ]
            },
            
            "family_law": {
                "constitutional_articles": [
                    {"number": "21", "title": "Protection of life and personal liberty"},
                    {"number": "14", "title": "Right to equality before law"},
                    {"number": "15", "title": "Prohibition of discrimination on grounds of religion, race, caste, sex"},
                    {"number": "39(f)", "title": "Children are given opportunities and facilities to develop in a healthy manner"}
                ],
                "personal_laws": [
                    {"act": "Hindu Marriage Act, 1955", "sections": [
                        {"section": "13", "title": "Divorce (grounds for divorce)"},
                        {"section": "24", "title": "Maintenance pendente lite and expenses of proceedings"},
                        {"section": "25", "title": "Permanent alimony and maintenance"}
                    ]},
                    {"act": "Protection of Women from Domestic Violence Act, 2005", "sections": [
                        {"section": "3", "title": "Definition of domestic violence"},
                        {"section": "12", "title": "Application to Magistrate"},
                        {"section": "18", "title": "Protection orders"}
                    ]},
                    {"act": "Hindu Adoption and Maintenance Act, 1956", "sections": [
                        {"section": "18", "title": "Maintenance of wife"},
                        {"section": "20", "title": "Maintenance of children"}
                    ]}
                ],
                "ipc_sections": {
                    "domestic_violence": [
                        {"section": "498A", "title": "Husband or relative subjecting woman to cruelty"},
                        {"section": "323", "title": "Punishment for voluntarily causing hurt"},
                        {"section": "354", "title": "Assault or criminal force to woman with intent to outrage modesty"},
                        {"section": "506", "title": "Punishment for criminal intimidation"},
                        {"section": "307", "title": "Attempt to murder (applicable in severe cases)"}
                    ]
                },
                "crpc_sections": [
                    {"section": "125", "title": "Order for maintenance of wives, children and parents"},
                    {"section": "156", "title": "Police officer's power to investigate"}
                ]
            },
            
            "tenant_rights": {
                "constitutional_articles": [
                    {"number": "21", "title": "Protection of life and personal liberty"},
                    {"number": "300A", "title": "Right to property"},
                    {"number": "14", "title": "Right to equality before law"}
                ],
                "rent_control_acts": [
                    {"act": "Rent Control Act (State-specific)", "sections": [
                        {"section": "10", "title": "Protection against eviction"},
                        {"section": "12", "title": "Standard rent and permitted increases"},
                        {"section": "21", "title": "Deposit of rent in court"}
                    ]},
                    {"act": "Transfer of Property Act, 1882", "sections": [
                        {"section": "105", "title": "Lease defined"},
                        {"section": "108", "title": "Rights and liabilities of lessor and lessee"},
                        {"section": "111", "title": "Determination of lease"}
                    ]}
                ],
                "consumer_laws": [
                    {"act": "Consumer Protection Act, 2019", "sections": [
                        {"section": "2(7)", "title": "Consumer defined"},
                        {"section": "35", "title": "Jurisdiction of District Commission"}
                    ]}
                ],
                "cpc_sections": [
                    {"section": "9", "title": "Courts to try all civil suits"},
                    {"section": "26", "title": "Institution of suits"}
                ]
            },
            
            "consumer_complaint": {
                "constitutional_articles": [
                    {"number": "19(1)(g)", "title": "Right to practice any profession or carry on any trade or business"},
                    {"number": "21", "title": "Protection of life and personal liberty"},
                    {"number": "14", "title": "Right to equality before law"}
                ],
                "consumer_laws": [
                    {"act": "Consumer Protection Act, 2019", "sections": [
                        {"section": "2(7)", "title": "Consumer defined"},
                        {"section": "2(11)", "title": "Deficiency in service defined"},
                        {"section": "2(22)", "title": "Goods defined"},
                        {"section": "35", "title": "Jurisdiction of District Commission"},
                        {"section": "42", "title": "Jurisdiction of State Commission"},
                        {"section": "58", "title": "Jurisdiction of National Commission"}
                    ]},
                    {"act": "Sale of Goods Act, 1930", "sections": [
                        {"section": "14", "title": "Sale by description"},
                        {"section": "16", "title": "Sale by sample"}
                    ]}
                ],
                "ipc_sections": {
                    "cheating": [
                        {"section": "420", "title": "Cheating and dishonestly inducing delivery of property"}
                    ]
                }
            }
        }
    
    def _load_process_templates(self) -> Dict[str, Any]:
        """Load detailed legal process templates"""
        return {
            "criminal_law": {
                "theft": {
                    "process": [
                        "File **First Information Report (FIR)** under _Section 154 CrPC_ at the nearest police station.",
                        "Mention **Sections 378 & 379 IPC** in your complaint for theft.",
                        "Cooperate with the police investigation (Sections 156 & 173 CrPC).",
                        "If property is recovered, apply for return of property (Section 451 CrPC).",
                        "Engage a criminal lawyer for further proceedings."
                    ],
                    "timeline": {
                        "police_station": {"success_rate": 80, "duration": "immediate action expected"},
                        "criminal_court": {"success_rate": 40, "duration": "150–645 days"}
                    }
                },
                "robbery": {
                    "process": [
                        "**Immediately call 100** for emergency police response.",
                        "File **FIR under Sections 390 & 392 IPC** at nearest police station.",
                        "Provide detailed description of incident and perpetrators.",
                        "Cooperate with police investigation and identification parade.",
                        "Engage criminal lawyer for court proceedings.",
                        "Apply for victim compensation if applicable."
                    ],
                    "timeline": {
                        "police_station": {"success_rate": 70, "duration": "immediate action expected"},
                        "criminal_court": {"success_rate": 45, "duration": "180–730 days"}
                    }
                },
                "rape": {
                    "process": [
                        "**URGENT: Call 100 immediately** for police assistance.",
                        "Seek immediate medical attention and preserve evidence.",
                        "File **FIR under Sections 375 & 376 IPC** at nearest police station.",
                        "Request female police officer for statement recording.",
                        "Undergo medical examination by qualified doctor.",
                        "Engage experienced criminal lawyer specializing in sexual offences.",
                        "Apply for victim compensation under state schemes."
                    ],
                    "timeline": {
                        "police_station": {"success_rate": 85, "duration": "immediate action expected"},
                        "fast_track_court": {"success_rate": 60, "duration": "90–365 days"}
                    }
                }
            },
            
            "cyber_crime": {
                "hacking": {
                    "process": [
                        "**Immediately change all passwords** and secure accounts.",
                        "File **FIR under Section 66 IT Act** at cyber crime cell or nearest police station.",
                        "Preserve evidence: screenshots, logs, communication records.",
                        "Report to platform/service provider (bank, social media, etc.).",
                        "Cooperate with cyber crime investigation.",
                        "Engage cyber law expert if case is complex."
                    ],
                    "timeline": {
                        "cyber_cell": {"success_rate": 70, "duration": "30–180 days"},
                        "cyber_court": {"success_rate": 51, "duration": "85–224 days"}
                    }
                },
                "identity_theft": {
                    "process": [
                        "**Immediately secure all accounts** and change passwords.",
                        "File **FIR under Section 66C IT Act** for identity theft.",
                        "Report to credit bureaus and financial institutions.",
                        "Preserve all evidence of misuse of identity.",
                        "File complaint with platform where identity was misused.",
                        "Engage cyber law advocate for legal proceedings."
                    ],
                    "timeline": {
                        "cyber_cell": {"success_rate": 65, "duration": "45–200 days"},
                        "cyber_court": {"success_rate": 55, "duration": "90–300 days"}
                    }
                }
            },
            
            "employment_law": {
                "salary_issues": {
                    "process": [
                        "Send **legal notice** to employer demanding payment within 15-30 days.",
                        "File complaint with **Labour Commissioner** under Payment of Wages Act.",
                        "Approach **Labour Court** if conciliation fails.",
                        "File case under **Section 7 Payment of Wages Act** for delayed payment.",
                        "Claim interest and compensation for delayed payment.",
                        "Engage labour law advocate for court proceedings."
                    ],
                    "timeline": {
                        "labour_commissioner": {"success_rate": 65, "duration": "60–180 days"},
                        "labour_court": {"success_rate": 60, "duration": "192–360 days"}
                    }
                },
                "wrongful_termination": {
                    "process": [
                        "Send **legal notice** challenging termination within 30 days.",
                        "File complaint with **Labour Commissioner** for conciliation.",
                        "Approach **Industrial Tribunal** under Industrial Disputes Act.",
                        "Claim reinstatement with back wages or compensation.",
                        "Gather evidence of unfair termination and service records.",
                        "Engage experienced labour law advocate."
                    ],
                    "timeline": {
                        "labour_commissioner": {"success_rate": 55, "duration": "90–240 days"},
                        "industrial_tribunal": {"success_rate": 50, "duration": "240–540 days"}
                    }
                }
            },
            
            "family_law": {
                "domestic_violence": {
                    "process": [
                        "**URGENT: Call 181 Women Helpline** for immediate assistance.",
                        "File **FIR under Section 498A IPC** at nearest police station.",
                        "Apply for **Protection Order** under DV Act 2005 with Magistrate.",
                        "Seek medical treatment and preserve evidence of injuries.",
                        "Apply for maintenance and residence orders.",
                        "Engage family law advocate specializing in domestic violence.",
                        "Contact local NGOs for support and counseling."
                    ],
                    "timeline": {
                        "police_station": {"success_rate": "Immediate protection usually granted if FIR registered", "duration": "immediate action expected"},
                        "family_court": {"success_rate": 68, "duration": "90–270 days (timelines vary by court backlog)"}
                    }
                },
                "divorce": {
                    "process": [
                        "Attempt **mutual consent divorce** if both parties agree.",
                        "File **divorce petition** in family court under relevant personal law.",
                        "Serve notice to respondent and await response.",
                        "Attend court hearings and mediation sessions.",
                        "Negotiate settlement for alimony, child custody, and property.",
                        "Engage experienced family law advocate.",
                        "Obtain final divorce decree from court."
                    ],
                    "timeline": {
                        "mutual_consent": {"success_rate": 85, "duration": "6–18 months"},
                        "contested_divorce": {"success_rate": 70, "duration": "2–5 years"}
                    }
                }
            },
            
            "tenant_rights": {
                "deposit_issues": {
                    "process": [
                        "Send **legal notice** to landlord demanding deposit return within 15-30 days.",
                        "File complaint with **Rent Tribunal** under Rent Control Act.",
                        "Approach **Consumer Forum** if deposit involves service deficiency.",
                        "File civil suit for recovery of deposit with interest.",
                        "Preserve rental agreement and payment receipts as evidence.",
                        "Engage property law advocate for legal proceedings."
                    ],
                    "timeline": {
                        "rent_tribunal": {"success_rate": 75, "duration": "90–240 days"},
                        "civil_court": {"success_rate": 68, "duration": "180–450 days"}
                    }
                },
                "illegal_eviction": {
                    "process": [
                        "**Immediately file injunction** to stop eviction proceedings.",
                        "File case under **Rent Control Act** for protection against eviction.",
                        "Gather evidence of illegal eviction attempts.",
                        "Deposit rent in court if landlord refuses to accept.",
                        "Claim damages for harassment and illegal eviction.",
                        "Engage property law advocate experienced in tenant rights."
                    ],
                    "timeline": {
                        "rent_tribunal": {"success_rate": 80, "duration": "60–180 days"},
                        "civil_court": {"success_rate": 72, "duration": "120–360 days"}
                    }
                }
            },
            
            "consumer_complaint": {
                "defective_product": {
                    "process": [
                        "**Contact seller/manufacturer** for replacement or refund within warranty period.",
                        "File complaint with **District Consumer Forum** under Consumer Protection Act.",
                        "Preserve product, bill, warranty card, and correspondence as evidence.",
                        "Claim refund, replacement, or compensation for deficiency in goods.",
                        "Attend hearings and provide evidence of defect.",
                        "Engage consumer law advocate if case is complex."
                    ],
                    "timeline": {
                        "district_forum": {"success_rate": 78, "duration": "90–270 days"},
                        "state_commission": {"success_rate": 70, "duration": "180–450 days"}
                    }
                },
                "service_deficiency": {
                    "process": [
                        "**Raise complaint** with service provider's grievance cell first.",
                        "File complaint with **Consumer Forum** for deficiency in service.",
                        "Preserve bills, correspondence, and evidence of poor service.",
                        "Claim compensation for mental agony and financial loss.",
                        "Attend hearings and present evidence of service deficiency.",
                        "Engage consumer law advocate for effective representation."
                    ],
                    "timeline": {
                        "district_forum": {"success_rate": 75, "duration": "120–300 days"},
                        "state_commission": {"success_rate": 68, "duration": "200–480 days"}
                    }
                }
            }
        }
    
    def get_enhanced_legal_analysis(self, domain: str, query: str, confidence: float) -> Dict[str, Any]:
        """Get comprehensive legal analysis with detailed provisions"""
        
        # Determine specific legal category based on query keywords
        legal_category = self._determine_legal_category(domain, query)
        
        # Get domain-specific provisions
        provisions = self.legal_provisions.get(domain, {})
        
        # Get process template
        process_info = self._get_process_info(domain, legal_category)
        
        # Build comprehensive response
        analysis = {
            "domain": domain.replace('_', ' ').title(),
            "confidence": confidence,
            "query": query,
            "legal_category": legal_category,
            "constitutional_articles": provisions.get("constitutional_articles", []),
            "statutory_provisions": self._get_statutory_provisions(domain, legal_category, provisions),
            "legal_process": process_info.get("process", []),
            "timeline_success": process_info.get("timeline", {}),
            "additional_info": self._get_additional_info(domain, legal_category)
        }
        
        return analysis
    
    def _determine_legal_category(self, domain: str, query: str) -> str:
        """Determine specific legal category based on query keywords"""
        query_lower = query.lower()
        
        if domain == "criminal_law":
            if any(word in query_lower for word in ["stolen", "theft", "stole"]):
                return "theft"
            elif any(word in query_lower for word in ["robbed", "robbery", "robber"]):
                return "robbery"
            elif any(word in query_lower for word in ["raped", "rape", "sexual"]):
                return "rape"
            elif any(word in query_lower for word in ["murdered", "murder", "killed"]):
                return "murder"
            elif any(word in query_lower for word in ["kidnapped", "kidnap", "abducted"]):
                return "kidnapping"
            elif any(word in query_lower for word in ["cheated", "fraud", "scam"]):
                return "cheating"
            elif any(word in query_lower for word in ["assault", "beaten", "hit"]):
                return "assault"
            else:
                return "general_crime"
                
        elif domain == "cyber_crime":
            if any(word in query_lower for word in ["hacked", "hacking", "hack"]):
                return "hacking"
            elif any(word in query_lower for word in ["identity", "impersonation", "fake profile"]):
                return "identity_theft"
            elif any(word in query_lower for word in ["online fraud", "cyber fraud", "phishing"]):
                return "online_fraud"
            else:
                return "general_cyber"
                
        elif domain == "employment_law":
            if any(word in query_lower for word in ["salary", "wages", "payment", "pay"]):
                return "salary_issues"
            elif any(word in query_lower for word in ["fired", "terminated", "dismissed"]):
                return "wrongful_termination"
            elif any(word in query_lower for word in ["harassment", "discrimination"]):
                return "workplace_harassment"
            else:
                return "general_employment"
                
        elif domain == "family_law":
            # Enhanced detection for domestic violence with higher confidence
            if any(word in query_lower for word in ["beats", "violence", "abuse", "domestic", "hitting", "hurting", "threatening"]):
                return "domestic_violence"
            elif any(word in query_lower for word in ["divorce", "separation"]):
                return "divorce"
            elif any(word in query_lower for word in ["custody", "child", "maintenance"]):
                return "child_custody"
            else:
                return "general_family"
                
        elif domain == "tenant_rights":
            if any(word in query_lower for word in ["deposit", "security"]):
                return "deposit_issues"
            elif any(word in query_lower for word in ["eviction", "evict", "vacate"]):
                return "illegal_eviction"
            elif any(word in query_lower for word in ["rent", "increase"]):
                return "rent_issues"
            else:
                return "general_tenant"
                
        elif domain == "consumer_complaint":
            if any(word in query_lower for word in ["defective", "faulty", "broken", "damaged"]):
                return "defective_product"
            elif any(word in query_lower for word in ["service", "poor", "bad"]):
                return "service_deficiency"
            else:
                return "general_consumer"
        
        return "general"
    
    def _get_statutory_provisions(self, domain: str, category: str, provisions: Dict) -> Dict[str, List]:
        """Get relevant statutory provisions based on domain and category"""
        statutory = {}
        
        if domain == "criminal_law":
            # Add relevant IPC sections
            if category in provisions.get("ipc_sections", {}):
                statutory["IPC Sections (Indian Penal Code, 1860)"] = provisions["ipc_sections"][category]
            
            # Add CrPC sections
            if "crpc_sections" in provisions:
                statutory["CrPC Sections (Code of Criminal Procedure, 1973)"] = provisions["crpc_sections"]
                
        elif domain == "cyber_crime":
            # Add IT Act sections
            if "it_act_sections" in provisions:
                statutory["IT Act Sections (Information Technology Act, 2000)"] = provisions["it_act_sections"]
            
            # Add relevant IPC sections for cyber crimes
            if "ipc_sections" in provisions and "fraud" in provisions["ipc_sections"]:
                statutory["IPC Sections (Indian Penal Code, 1860)"] = provisions["ipc_sections"]["fraud"]
            
            # Add CrPC sections
            if "crpc_sections" in provisions:
                statutory["CrPC Sections (Code of Criminal Procedure, 1973)"] = provisions["crpc_sections"]
                
        elif domain == "employment_law":
            # Add labour law sections
            if "labour_laws" in provisions:
                for law in provisions["labour_laws"]:
                    statutory[law["act"]] = law["sections"]
                    
        elif domain == "family_law":
            # Add personal law sections
            if "personal_laws" in provisions:
                for law in provisions["personal_laws"]:
                    statutory[law["act"]] = law["sections"]
            
            # Add relevant IPC sections
            if "ipc_sections" in provisions and category == "domestic_violence":
                statutory["IPC Sections (Indian Penal Code, 1860)"] = provisions["ipc_sections"]["domestic_violence"]
                
        elif domain == "tenant_rights":
            # Add rent control and property law sections
            if "rent_control_acts" in provisions:
                for law in provisions["rent_control_acts"]:
                    statutory[law["act"]] = law["sections"]
                    
        elif domain == "consumer_complaint":
            # Add consumer protection law sections
            if "consumer_laws" in provisions:
                for law in provisions["consumer_laws"]:
                    statutory[law["act"]] = law["sections"]
        
        return statutory
    
    def _get_process_info(self, domain: str, category: str) -> Dict[str, Any]:
        """Get detailed legal process information"""
        templates = self.process_templates.get(domain, {})
        
        if category in templates:
            return templates[category]
        
        # Return default process if specific category not found
        return {
            "process": [
                "Consult with a qualified legal advocate specializing in this area.",
                "Gather all relevant documents and evidence.",
                "File appropriate legal proceedings in competent court/forum.",
                "Attend hearings and follow court procedures.",
                "Seek appropriate legal remedy as per applicable law."
            ],
            "timeline": {
                "general_court": {"success_rate": 60, "duration": "180–540 days"}
            }
        }
    
    def _get_additional_info(self, domain: str, category: str) -> Dict[str, Any]:
        """Get additional helpful information"""
        info = {
            "important_notes": [],
            "emergency_contacts": [],
            "helpful_resources": []
        }
        
        if domain == "criminal_law":
            info["important_notes"] = [
                "File FIR immediately - delay may weaken your case",
                "Preserve all evidence and avoid tampering with crime scene",
                "Engage experienced criminal lawyer for serious offences",
                "Victim compensation may be available under state schemes"
            ]
            info["emergency_contacts"] = [
                "Police Emergency: 100",
                "Women Helpline: 181",
                "Child Helpline: 1098"
            ]
            
        elif domain == "cyber_crime":
            info["important_notes"] = [
                "Act quickly to secure accounts and preserve evidence",
                "Report to cyber crime cell for specialized investigation",
                "Keep screenshots and digital evidence safe",
                "Inform banks/financial institutions immediately if money involved"
            ]
            info["emergency_contacts"] = [
                "Cyber Crime Helpline: 1930",
                "Police Emergency: 100"
            ]
            
        elif domain == "family_law":
            info["important_notes"] = [
                "Safety is paramount in domestic violence cases",
                "Seek counseling and support from NGOs",
                "Document all incidents with dates and evidence",
                "Consider mutual consent for faster resolution"
            ]
            info["emergency_contacts"] = [
                "Women Helpline: 181",
                "Domestic Violence Helpline: 181"
            ]
        
        return info
    
    def format_enhanced_response(self, analysis: Dict[str, Any]) -> str:
        """Format the enhanced legal analysis into a structured response"""
        
        response = f"**Domain:** {analysis['domain']} (Confidence: {analysis['confidence']:.3f})\n"
        response += f"**Query:** _{analysis['query']}_\n\n"
        response += "* * *\n\n"
        
        # Constitutional Articles
        response += "### 🏛️ Applicable Legal Provisions\n\n"
        response += "*   **Constitutional Articles**\n"
        for article in analysis['constitutional_articles']:
            response += f"    *   Article {article['number']}: {article['title']}\n"
        response += "\n"
        
        # Statutory Provisions
        for act_name, sections in analysis['statutory_provisions'].items():
            response += f"*   **Relevant {act_name}**\n"
            for section in sections:
                response += f"    *   **Section {section['section']}** – {section['title']}\n"
            response += "\n"
        
        response += "* * *\n\n"
        
        # Legal Process
        response += "### 📋 Detailed Legal Process\n\n"
        for i, step in enumerate(analysis['legal_process'], 1):
            response += f"{i}.  {step}\n"
        response += "\n"
        
        response += "* * *\n\n"
        
        # Timeline & Success Rate
        response += "### ⏱️ Timeline & Success Rate\n\n"
        for route, info in analysis['timeline_success'].items():
            route_name = route.replace('_', ' ').title()
            response += f"*   **{route_name} Route:** {info['success_rate']}% success rate, {info['duration']}.\n"
        
        # Additional Information
        if analysis['additional_info']['important_notes']:
            response += "\n* * *\n\n"
            response += "### 💡 Important Notes\n\n"
            for note in analysis['additional_info']['important_notes']:
                response += f"*   {note}\n"
        
        if analysis['additional_info']['emergency_contacts']:
            response += "\n### 🚨 Emergency Contacts\n\n"
            for contact in analysis['additional_info']['emergency_contacts']:
                response += f"*   {contact}\n"
        
        return response

# Test the enhanced legal provisions engine
if __name__ == "__main__":
    engine = EnhancedLegalProvisionsEngine()
    
    # Test with phone theft query
    analysis = engine.get_enhanced_legal_analysis("criminal_law", "My phone is stolen", 3.728)
    formatted_response = engine.format_enhanced_response(analysis)
    
    print("🧪 ENHANCED LEGAL PROVISIONS ENGINE TEST")
    print("=" * 50)
    print(formatted_response)